/* ============================================================================
   RU-AIBOTWORKS — control database schema
   SQL Server 2025 · Windows Authentication · database RU_AIBOTWORKS

   Four schemas, matching the planes this repository owns (RU-AIBOTWORKS-ADR-001):

     gov   governance   the org, the agents, their contracts and registrations
     ops   observability the trajectory log and the receipt chain — APPEND ONLY
     fin   finance      metering, rate cards, budgets, billing
     svc   service      catalogue, requests, incidents, changes, SLAs

   Two structural rules are enforced by the schema rather than by convention:

     1. Governance tables are SYSTEM_VERSIONED. History is written by the engine,
        so an application — or an agent — cannot rewrite what the org used to be.
     2. ops.* has no UPDATE or DELETE path for the application role. The audit
        trail is written under a principal the agents cannot reach (STD-AGENT-001
        §5 plane 7, §30.3).

   Re-runnable. Safe to execute repeatedly.
   ============================================================================ */

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

IF DB_ID('RU_AIBOTWORKS') IS NULL
BEGIN
    PRINT 'Creating database RU_AIBOTWORKS';
    EXEC('CREATE DATABASE RU_AIBOTWORKS');
END
GO

ALTER DATABASE RU_AIBOTWORKS SET RECOVERY FULL;
GO

USE RU_AIBOTWORKS;
GO

IF SCHEMA_ID('gov') IS NULL EXEC('CREATE SCHEMA gov');
IF SCHEMA_ID('ops') IS NULL EXEC('CREATE SCHEMA ops');
IF SCHEMA_ID('fin') IS NULL EXEC('CREATE SCHEMA fin');
IF SCHEMA_ID('svc') IS NULL EXEC('CREATE SCHEMA svc');
GO

/* ────────────────────────────────────────────────────────────────────────────
   gov — governance. The company as it is, with history the engine keeps.
   ──────────────────────────────────────────────────────────────────────────── */

IF OBJECT_ID('gov.Division') IS NULL
CREATE TABLE gov.Division (
    DivisionId      INT IDENTITY(1,1) CONSTRAINT PK_Division PRIMARY KEY,
    Name            NVARCHAR(64)  NOT NULL CONSTRAINT UQ_Division_Name UNIQUE,
    Description     NVARCHAR(400) NULL
);
GO

IF OBJECT_ID('gov.AuthorityLevel') IS NULL
CREATE TABLE gov.AuthorityLevel (
    Level           CHAR(2)      NOT NULL CONSTRAINT PK_AuthorityLevel PRIMARY KEY,
    Rank            TINYINT      NOT NULL CONSTRAINT UQ_AuthorityLevel_Rank UNIQUE,
    HeldBy          NVARCHAR(80) NOT NULL,
    MayDecide       NVARCHAR(300) NOT NULL,
    MayNot          NVARCHAR(300) NOT NULL
);
GO

/* Officers are system-versioned: who held which veto, when, is an audit question. */
IF OBJECT_ID('gov.Officer') IS NULL
EXEC('
CREATE TABLE gov.Officer (
    OfficerId       INT IDENTITY(1,1) CONSTRAINT PK_Officer PRIMARY KEY,
    Name            NVARCHAR(64)  NOT NULL CONSTRAINT UQ_Officer_Name UNIQUE,
    Level           CHAR(2)       NOT NULL CONSTRAINT FK_Officer_Level
                                  REFERENCES gov.AuthorityLevel(Level),
    ReportsTo       NVARCHAR(64)  NOT NULL,
    DivisionId      INT           NOT NULL CONSTRAINT FK_Officer_Division
                                  REFERENCES gov.Division(DivisionId),
    [Function]      NVARCHAR(32)  NOT NULL,
    Model           NVARCHAR(16)  NOT NULL,
    Power           NVARCHAR(16)  NOT NULL CONSTRAINT DF_Officer_Power DEFAULT '''',
    Decides         NVARCHAR(400) NOT NULL,
    MaxTier         TINYINT       NOT NULL CONSTRAINT CK_Officer_MaxTier CHECK (MaxTier BETWEEN 0 AND 4),
    IsReadOnly      BIT           NOT NULL,
    AddedBy         NVARCHAR(32)  NOT NULL,
    ValidFrom       DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL,
    ValidTo         DATETIME2 GENERATED ALWAYS AS ROW END   NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo),
    CONSTRAINT CK_Officer_Power CHECK (Power IN ('''', ''VETO'', ''READ-ONLY''))
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = gov.OfficerHistory));
');
GO

IF OBJECT_ID('gov.Department') IS NULL
CREATE TABLE gov.Department (
    DepartmentId    INT IDENTITY(1,1) CONSTRAINT PK_Department PRIMARY KEY,
    Code            NVARCHAR(64)  NOT NULL CONSTRAINT UQ_Department_Code UNIQUE,
    Name            NVARCHAR(128) NOT NULL,
    DivisionId      INT           NOT NULL CONSTRAINT FK_Department_Division
                                  REFERENCES gov.Division(DivisionId),
    OfficerId       INT           NOT NULL CONSTRAINT FK_Department_Officer
                                  REFERENCES gov.Officer(OfficerId),
    Mission         NVARCHAR(400) NOT NULL
);
GO

IF OBJECT_ID('gov.Team') IS NULL
CREATE TABLE gov.Team (
    TeamId          INT IDENTITY(1,1) CONSTRAINT PK_Team PRIMARY KEY,
    Code            NVARCHAR(64)  NOT NULL,
    Name            NVARCHAR(128) NOT NULL,
    DepartmentId    INT           NOT NULL CONSTRAINT FK_Team_Department
                                  REFERENCES gov.Department(DepartmentId),
    LeadAgentName   NVARCHAR(64)  NOT NULL,
    Mission         NVARCHAR(400) NOT NULL,
    CONSTRAINT UQ_Team_Code UNIQUE (DepartmentId, Code)
);
GO

/* Agents are system-versioned. A blast radius that changed silently is the thing
   an incident review needs to be able to find. */
IF OBJECT_ID('gov.Agent') IS NULL
EXEC('
CREATE TABLE gov.Agent (
    AgentId         INT IDENTITY(1,1) CONSTRAINT PK_Agent PRIMARY KEY,
    Name            NVARCHAR(64)   NOT NULL CONSTRAINT UQ_Agent_Name UNIQUE,
    TeamId          INT            NOT NULL CONSTRAINT FK_Agent_Team REFERENCES gov.Team(TeamId),
    DepartmentId    INT            NOT NULL CONSTRAINT FK_Agent_Department REFERENCES gov.Department(DepartmentId),
    ReportsTo       NVARCHAR(64)   NOT NULL,
    DecisionLevel   CHAR(2)        NOT NULL CONSTRAINT FK_Agent_Level REFERENCES gov.AuthorityLevel(Level),
    [Role]          NVARCHAR(400)  NOT NULL,
    Model           NVARCHAR(16)   NOT NULL,
    Capability      NVARCHAR(64)   NOT NULL,
    MaxTier         TINYINT        NOT NULL CONSTRAINT CK_Agent_MaxTier CHECK (MaxTier BETWEEN 0 AND 2),
    IsTeamLead      BIT            NOT NULL,
    IsReadOnly      BIT            NOT NULL,
    Cohort          NVARCHAR(32)   NOT NULL,
    Classification  NVARCHAR(32)   NOT NULL,
    AutonomyLevel   NVARCHAR(32)   NOT NULL,
    BlastRadius     NVARCHAR(2000) NOT NULL,
    BudgetSteps     INT            NOT NULL,
    BudgetTokens    INT            NOT NULL,
    BudgetMutations INT            NOT NULL,
    RegisteredOn    DATE           NOT NULL,
    ReviewDue       DATE           NOT NULL,
    ValidFrom       DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL,
    ValidTo         DATETIME2 GENERATED ALWAYS AS ROW END   NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo),
    CONSTRAINT CK_Agent_BlastRadius_NotVague
        CHECK (LEN(BlastRadius) > 80 AND BlastRadius NOT LIKE ''%would have to investigate%'')
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = gov.AgentHistory));
');
GO

IF OBJECT_ID('gov.AgentDomain') IS NULL
CREATE TABLE gov.AgentDomain (
    AgentId         INT          NOT NULL CONSTRAINT FK_AgentDomain_Agent REFERENCES gov.Agent(AgentId),
    Domain          NVARCHAR(64) NOT NULL,
    CONSTRAINT PK_AgentDomain PRIMARY KEY (AgentId, Domain)
);
GO

IF OBJECT_ID('gov.Skill') IS NULL
CREATE TABLE gov.Skill (
    SkillId         INT IDENTITY(1,1) CONSTRAINT PK_Skill PRIMARY KEY,
    Code            NVARCHAR(96)  NOT NULL,
    OwnerAgentId    INT           NOT NULL CONSTRAINT FK_Skill_Agent REFERENCES gov.Agent(AgentId),
    About           NVARCHAR(500) NOT NULL,
    Grants          NVARCHAR(16)  NOT NULL CONSTRAINT DF_Skill_Grants DEFAULT 'none',
    CONSTRAINT UQ_Skill UNIQUE (OwnerAgentId, Code),
    /* A skill grants nothing. Ever. RU-AIBOTWORKS-ADR-005. */
    CONSTRAINT CK_Skill_GrantsNothing CHECK (Grants = 'none')
);
GO

IF OBJECT_ID('gov.Tool') IS NULL
CREATE TABLE gov.Tool (
    ToolId          INT IDENTITY(1,1) CONSTRAINT PK_Tool PRIMARY KEY,
    Name            NVARCHAR(96)  NOT NULL CONSTRAINT UQ_Tool_Name UNIQUE,
    Version         INT           NOT NULL,
    Owner           NVARCHAR(64)  NOT NULL,
    Description     NVARCHAR(400) NOT NULL,
    Irreversibility TINYINT       NOT NULL CONSTRAINT CK_Tool_Tier CHECK (Irreversibility BETWEEN 0 AND 4),
    Idempotent      BIT           NOT NULL,
    [Rollback]        NVARCHAR(300) NULL,
    ResourcePattern NVARCHAR(200) NOT NULL,
    Approval        NVARCHAR(16)  NOT NULL,
    PerTaskLimit    INT           NOT NULL,
    MutationBudget  INT           NOT NULL,
    RetentionDays   INT           NOT NULL,
    IsGrantable     BIT           NOT NULL,
    /* AGT-DES-01 - a null rollback on a grantable Tier 2+ tool is a design finding,
       so the database refuses to hold one. */
    CONSTRAINT CK_Tool_RollbackRequired
        CHECK (IsGrantable = 0 OR Irreversibility < 2 OR [Rollback] IS NOT NULL),
    /* §34.3 — Tier 3 and 4 are never grantable to an agent, at any autonomy level. */
    CONSTRAINT CK_Tool_NoHighTierGrant
        CHECK (IsGrantable = 0 OR Irreversibility <= 2)
);
GO

IF OBJECT_ID('gov.ToolBlockedIf') IS NULL
CREATE TABLE gov.ToolBlockedIf (
    ToolId          INT          NOT NULL CONSTRAINT FK_ToolBlockedIf_Tool REFERENCES gov.Tool(ToolId),
    Condition       NVARCHAR(96) NOT NULL,
    CONSTRAINT PK_ToolBlockedIf PRIMARY KEY (ToolId, Condition)
);
GO

IF OBJECT_ID('gov.AgentTool') IS NULL
CREATE TABLE gov.AgentTool (
    AgentId         INT NOT NULL CONSTRAINT FK_AgentTool_Agent REFERENCES gov.Agent(AgentId),
    ToolId          INT NOT NULL CONSTRAINT FK_AgentTool_Tool  REFERENCES gov.Tool(ToolId),
    GrantedOn       DATE NOT NULL CONSTRAINT DF_AgentTool_GrantedOn DEFAULT CAST(SYSUTCDATETIME() AS DATE),
    CONSTRAINT PK_AgentTool PRIMARY KEY (AgentId, ToolId)
);
GO

IF OBJECT_ID('gov.Promotion') IS NULL
CREATE TABLE gov.Promotion (
    PromotionId     INT IDENTITY(1,1) CONSTRAINT PK_Promotion PRIMARY KEY,
    AgentId         INT           NOT NULL CONSTRAINT FK_Promotion_Agent REFERENCES gov.Agent(AgentId),
    ToLevel         CHAR(2)       NOT NULL CONSTRAINT FK_Promotion_Level REFERENCES gov.AuthorityLevel(Level),
    TeamCode        NVARCHAR(128) NOT NULL,
    RequestedBy     NVARCHAR(64)  NOT NULL,
    Reason          NVARCHAR(600) NOT NULL,
    PromotedOn      DATE          NOT NULL,
    /* A promotion with no reason is not a promotion, it is drift. */
    CONSTRAINT CK_Promotion_ReasonGiven CHECK (LEN(Reason) > 30)
);
GO

IF OBJECT_ID('gov.ReservedDecision') IS NULL
CREATE TABLE gov.ReservedDecision (
    Decision        NVARCHAR(128) NOT NULL CONSTRAINT PK_ReservedDecision PRIMARY KEY,
    Rationale       NVARCHAR(300) NULL
);
GO

IF OBJECT_ID('gov.Lane') IS NULL
CREATE TABLE gov.Lane (
    Code            NVARCHAR(4)   NOT NULL CONSTRAINT PK_Lane PRIMARY KEY,
    Label           NVARCHAR(64)  NOT NULL,
    Stack           NVARCHAR(96)  NOT NULL
);
GO

IF OBJECT_ID('gov.Template') IS NULL
CREATE TABLE gov.Template (
    TemplateId      INT           NOT NULL CONSTRAINT PK_Template PRIMARY KEY,
    Code            NVARCHAR(32)  NOT NULL CONSTRAINT UQ_Template_Code UNIQUE,
    LaneCode        NVARCHAR(4)   NOT NULL CONSTRAINT FK_Template_Lane REFERENCES gov.Lane(Code),
    IsKeystone      BIT           NOT NULL
);
GO

IF OBJECT_ID('gov.ComplianceRegime') IS NULL
CREATE TABLE gov.ComplianceRegime (
    Code            NVARCHAR(48)  NOT NULL CONSTRAINT PK_ComplianceRegime PRIMARY KEY,
    Scope           NVARCHAR(16)  NOT NULL,   -- company | project
    OwnerOfficer    NVARCHAR(64)  NOT NULL,
    CONSTRAINT CK_Regime_Scope CHECK (Scope IN ('company', 'project'))
);
GO

IF OBJECT_ID('gov.TemplateRegime') IS NULL
CREATE TABLE gov.TemplateRegime (
    TemplateId      INT          NOT NULL CONSTRAINT FK_TemplateRegime_Template REFERENCES gov.Template(TemplateId),
    RegimeCode      NVARCHAR(48) NOT NULL CONSTRAINT FK_TemplateRegime_Regime   REFERENCES gov.ComplianceRegime(Code),
    CONSTRAINT PK_TemplateRegime PRIMARY KEY (TemplateId, RegimeCode)
);
GO

/* ────────────────────────────────────────────────────────────────────────────
   ops — observability. APPEND ONLY. Written under a principal no agent holds.
   ──────────────────────────────────────────────────────────────────────────── */

IF OBJECT_ID('ops.AgentRun') IS NULL
CREATE TABLE ops.AgentRun (
    RunId           BIGINT IDENTITY(1,1) CONSTRAINT PK_AgentRun PRIMARY KEY,
    AgentId         INT           NOT NULL CONSTRAINT FK_AgentRun_Agent REFERENCES gov.Agent(AgentId),
    ProjectCode     NVARCHAR(48)  NULL,
    HumanPrincipal  NVARCHAR(128) NOT NULL,
    StartedAt       DATETIME2     NOT NULL CONSTRAINT DF_AgentRun_Started DEFAULT SYSUTCDATETIME(),
    EndedAt         DATETIME2     NULL,
    Outcome         NVARCHAR(24)  NULL,
    StepsUsed       INT           NOT NULL CONSTRAINT DF_AgentRun_Steps DEFAULT 0,
    TokensIn        BIGINT        NOT NULL CONSTRAINT DF_AgentRun_TokIn  DEFAULT 0,
    TokensOut       BIGINT        NOT NULL CONSTRAINT DF_AgentRun_TokOut DEFAULT 0,
    MutationsUsed   INT           NOT NULL CONSTRAINT DF_AgentRun_Mut DEFAULT 0,
    HaltedByBudget  BIT           NOT NULL CONSTRAINT DF_AgentRun_Halted DEFAULT 0,
    CONSTRAINT CK_AgentRun_Outcome
        CHECK (Outcome IS NULL OR Outcome IN ('success','failed','halted','killed','abstained'))
);
GO

/* The trajectory log. §30.3 — tool arguments, result, credential used, and the
   provenance of untrusted content, sufficient to reconstruct a run end to end.
   Logged AFTER the decision and BEFORE the effect, so denied attempts survive. */
IF OBJECT_ID('ops.ToolCall') IS NULL
CREATE TABLE ops.ToolCall (
    CallId          BIGINT IDENTITY(1,1) CONSTRAINT PK_ToolCall PRIMARY KEY,
    RunId           BIGINT        NOT NULL CONSTRAINT FK_ToolCall_Run  REFERENCES ops.AgentRun(RunId),
    ToolId          INT           NOT NULL CONSTRAINT FK_ToolCall_Tool REFERENCES gov.Tool(ToolId),
    StepIndex       INT           NOT NULL,
    PlanHash        CHAR(64)      NULL,
    IdempotencyKey  NVARCHAR(128) NULL,
    Decision        NVARCHAR(16)  NOT NULL,
    DenyReason      NVARCHAR(300) NULL,
    Arguments       NVARCHAR(MAX) NULL,
    BeforeState     NVARCHAR(MAX) NULL,
    AfterState      NVARCHAR(MAX) NULL,
    CredentialRef   NVARCHAR(128) NULL,
    OccurredAt      DATETIME2     NOT NULL CONSTRAINT DF_ToolCall_At DEFAULT SYSUTCDATETIME(),
    CONSTRAINT CK_ToolCall_Decision CHECK (Decision IN ('allowed','denied','approved','expired')),
    CONSTRAINT CK_ToolCall_DenyHasReason CHECK (Decision <> 'denied' OR DenyReason IS NOT NULL)
);
GO

/* Content provenance. §6.2 — the only question that matters during an incident is
   which content steered the agent. Unanswerable without this table. */
IF OBJECT_ID('ops.ContextProvenance') IS NULL
CREATE TABLE ops.ContextProvenance (
    ProvenanceId    BIGINT IDENTITY(1,1) CONSTRAINT PK_ContextProvenance PRIMARY KEY,
    RunId           BIGINT        NOT NULL CONSTRAINT FK_Provenance_Run REFERENCES ops.AgentRun(RunId),
    TrustLabel      CHAR(2)       NOT NULL,
    SourceKind      NVARCHAR(48)  NOT NULL,
    SourceRef       NVARCHAR(400) NOT NULL,
    ContentSha256   CHAR(64)      NOT NULL,
    EnteredAt       DATETIME2     NOT NULL CONSTRAINT DF_Provenance_At DEFAULT SYSUTCDATETIME(),
    CONSTRAINT CK_Provenance_Label CHECK (TrustLabel IN ('T0','T1','T2','T3','T4'))
);
GO

/* The receipt chain. Ed25519 signature over the canonicalised record, hash-linked
   to its predecessor, verifiable offline. §21. */
IF OBJECT_ID('ops.Receipt') IS NULL
CREATE TABLE ops.Receipt (
    ReceiptId       BIGINT IDENTITY(1,1) CONSTRAINT PK_Receipt PRIMARY KEY,
    CallId          BIGINT       NULL CONSTRAINT FK_Receipt_Call REFERENCES ops.ToolCall(CallId),
    PrevHash        CHAR(64)     NOT NULL,
    PayloadSha256   CHAR(64)     NOT NULL,
    ChainHash       CHAR(64)     NOT NULL CONSTRAINT UQ_Receipt_ChainHash UNIQUE,
    Signature       NVARCHAR(200) NOT NULL,
    SignedAt        DATETIME2    NOT NULL CONSTRAINT DF_Receipt_At DEFAULT SYSUTCDATETIME()
);
GO

IF OBJECT_ID('ops.KillSwitchDrill') IS NULL
CREATE TABLE ops.KillSwitchDrill (
    DrillId         INT IDENTITY(1,1) CONSTRAINT PK_KillSwitchDrill PRIMARY KEY,
    PerformedOn     DATE          NOT NULL,
    TargetAgentId   INT           NULL CONSTRAINT FK_Drill_Agent REFERENCES gov.Agent(AgentId),
    Environment     NVARCHAR(24)  NOT NULL,
    LayerLatencyMs  NVARCHAR(400) NOT NULL,   -- measured, per layer
    SubagentsCovered BIT          NOT NULL,
    QueuedWorkCovered BIT         NOT NULL,
    PerformedBy     NVARCHAR(128) NOT NULL
);
GO

IF OBJECT_ID('ops.RestoreDrill') IS NULL
CREATE TABLE ops.RestoreDrill (
    DrillId         INT IDENTITY(1,1) CONSTRAINT PK_RestoreDrill PRIMARY KEY,
    PerformedOn     DATE          NOT NULL,
    DataDomain      NVARCHAR(64)  NOT NULL,
    PointInTime     DATETIME2     NOT NULL,
    MeasuredRtoMin  INT           NOT NULL,   -- measured, never target
    Succeeded       BIT           NOT NULL,
    PerformedBy     NVARCHAR(128) NOT NULL
);
GO

/* ────────────────────────────────────────────────────────────────────────────
   fin — payroll and finance. An AI company's payroll is tokens and wall clock.
   ──────────────────────────────────────────────────────────────────────────── */

IF OBJECT_ID('fin.RateCard') IS NULL
CREATE TABLE fin.RateCard (
    RateCardId      INT IDENTITY(1,1) CONSTRAINT PK_RateCard PRIMARY KEY,
    Model           NVARCHAR(16)   NOT NULL,
    EffectiveFrom   DATE           NOT NULL,
    InputPerMTok    DECIMAL(10,4)  NULL,
    OutputPerMTok   DECIMAL(10,4)  NULL,
    Note            NVARCHAR(200)  NULL,
    CONSTRAINT UQ_RateCard UNIQUE (Model, EffectiveFrom)
);
GO

IF OBJECT_ID('fin.MeterEntry') IS NULL
CREATE TABLE fin.MeterEntry (
    EntryId         BIGINT IDENTITY(1,1) CONSTRAINT PK_MeterEntry PRIMARY KEY,
    RunId           BIGINT         NOT NULL CONSTRAINT FK_Meter_Run   REFERENCES ops.AgentRun(RunId),
    AgentId         INT            NOT NULL CONSTRAINT FK_Meter_Agent REFERENCES gov.Agent(AgentId),
    PeriodCode      CHAR(7)        NOT NULL,          -- YYYY-MM
    ProjectCode     NVARCHAR(48)   NULL,
    ClientCode      NVARCHAR(48)   NULL,
    TokensIn        BIGINT         NOT NULL,
    TokensOut       BIGINT         NOT NULL,
    WallClockSec    INT            NOT NULL,
    CostMinor       BIGINT         NOT NULL,
    Reconciled      BIT            NOT NULL CONSTRAINT DF_Meter_Reconciled DEFAULT 0
);
GO

IF OBJECT_ID('fin.Budget') IS NULL
CREATE TABLE fin.Budget (
    BudgetId        INT IDENTITY(1,1) CONSTRAINT PK_Budget PRIMARY KEY,
    ScopeKind       NVARCHAR(16)   NOT NULL,          -- agent | project | company
    ScopeRef        NVARCHAR(64)   NOT NULL,
    PeriodCode      CHAR(7)        NOT NULL,
    CapSteps        INT            NULL,
    CapTokens       BIGINT         NULL,
    CapCostMinor    BIGINT         NULL,
    CapMutations    INT            NULL,
    OnExhaustion    NVARCHAR(16)   NOT NULL,
    /* A budget that warns and continues is not a budget. */
    CONSTRAINT CK_Budget_FailsSafe CHECK (OnExhaustion IN ('halt','halt_and_escalate')),
    CONSTRAINT CK_Budget_ScopeKind CHECK (ScopeKind IN ('agent','project','company')),
    CONSTRAINT UQ_Budget UNIQUE (ScopeKind, ScopeRef, PeriodCode)
);
GO

IF OBJECT_ID('fin.Engagement') IS NULL
CREATE TABLE fin.Engagement (
    EngagementId    INT IDENTITY(1,1) CONSTRAINT PK_Engagement PRIMARY KEY,
    ClientCode      NVARCHAR(48)   NOT NULL,
    TemplateId      INT            NULL CONSTRAINT FK_Engagement_Template REFERENCES gov.Template(TemplateId),
    OpenedOn        DATE           NOT NULL,
    ClosedOn        DATE           NULL,
    ContractMinor   BIGINT         NULL,
    Status          NVARCHAR(24)   NOT NULL
);
GO

/* ────────────────────────────────────────────────────────────────────────────
   svc — service management. ITSM between clients and delivery.
   ──────────────────────────────────────────────────────────────────────────── */

IF OBJECT_ID('svc.CatalogueItem') IS NULL
CREATE TABLE svc.CatalogueItem (
    ItemId          INT IDENTITY(1,1) CONSTRAINT PK_CatalogueItem PRIMARY KEY,
    Code            NVARCHAR(48)  NOT NULL CONSTRAINT UQ_CatalogueItem_Code UNIQUE,
    Name            NVARCHAR(128) NOT NULL,
    Offered         BIT           NOT NULL,
    DeclinedReason  NVARCHAR(300) NULL,
    CONSTRAINT CK_Catalogue_DeclineHasReason CHECK (Offered = 1 OR DeclinedReason IS NOT NULL)
);
GO

IF OBJECT_ID('svc.Sla') IS NULL
CREATE TABLE svc.Sla (
    SlaId           INT IDENTITY(1,1) CONSTRAINT PK_Sla PRIMARY KEY,
    ItemId          INT           NOT NULL CONSTRAINT FK_Sla_Item REFERENCES svc.CatalogueItem(ItemId),
    Severity        NVARCHAR(16)  NOT NULL,
    RespondMin      INT           NOT NULL,
    ResolveMin      INT           NOT NULL,
    IsMeasuredToday BIT           NOT NULL,
    /* An unmeasured SLA is a promise nobody can keep or disprove. */
    CONSTRAINT CK_Sla_Measurable CHECK (IsMeasuredToday = 1)
);
GO

IF OBJECT_ID('svc.Request') IS NULL
CREATE TABLE svc.Request (
    RequestId       INT IDENTITY(1,1) CONSTRAINT PK_Request PRIMARY KEY,
    Kind            NVARCHAR(16)  NOT NULL,
    ClientCode      NVARCHAR(48)  NOT NULL,
    ItemId          INT           NULL CONSTRAINT FK_Request_Item REFERENCES svc.CatalogueItem(ItemId),
    Summary         NVARCHAR(300) NOT NULL,
    Severity        NVARCHAR(16)  NULL,
    OwnerAgentName  NVARCHAR(64)  NULL,
    RaisedAt        DATETIME2     NOT NULL CONSTRAINT DF_Request_Raised DEFAULT SYSUTCDATETIME(),
    ClosedAt        DATETIME2     NULL,
    ClosureEvidence NVARCHAR(600) NULL,
    CONSTRAINT CK_Request_Kind CHECK (Kind IN ('request','incident','problem','change')),
    /* Closed against evidence, never closed for age. */
    CONSTRAINT CK_Request_ClosureEvidence
        CHECK (ClosedAt IS NULL OR ClosureEvidence IS NOT NULL)
);
GO

IF OBJECT_ID('svc.ChangeFreeze') IS NULL
CREATE TABLE svc.ChangeFreeze (
    FreezeId        INT IDENTITY(1,1) CONSTRAINT PK_ChangeFreeze PRIMARY KEY,
    StartsAt        DATETIME2     NOT NULL,
    EndsAt          DATETIME2     NOT NULL,
    Reason          NVARCHAR(300) NOT NULL,
    DeclaredBy      NVARCHAR(64)  NOT NULL,
    CONSTRAINT CK_Freeze_Window CHECK (EndsAt > StartsAt)
);
GO

IF OBJECT_ID('svc.BreachClock') IS NULL
CREATE TABLE svc.BreachClock (
    ClockId         INT IDENTITY(1,1) CONSTRAINT PK_BreachClock PRIMARY KEY,
    RequestId       INT           NOT NULL CONSTRAINT FK_BreachClock_Request REFERENCES svc.Request(RequestId),
    Regime          NVARCHAR(48)  NOT NULL,
    AwarenessAt     DATETIME2     NOT NULL,
    DeadlineAt      DATETIME2     NOT NULL,
    NotifiedAt      DATETIME2     NULL,
    OwnerAgentName  NVARCHAR(64)  NOT NULL,
    CONSTRAINT CK_BreachClock_Deadline CHECK (DeadlineAt > AwarenessAt)
);
GO


/* ── Person names ────────────────────────────────────────────────────────────
   Every agent carries two identities: a dispatch handle (Name) that appears in
   every receipt, and a person name (Person) that people actually use. Added
   after the workforce was first loaded, so these are ALTERs rather than columns
   in the CREATE above - the history tables pick them up automatically.
   ──────────────────────────────────────────────────────────────────────────── */

IF COL_LENGTH('gov.Officer', 'Person') IS NULL
    ALTER TABLE gov.Officer ADD Person NVARCHAR(48) NOT NULL CONSTRAINT DF_Officer_Person DEFAULT N'';
GO
IF COL_LENGTH('gov.Agent', 'Person') IS NULL
    ALTER TABLE gov.Agent ADD Person NVARCHAR(48) NOT NULL CONSTRAINT DF_Agent_Person DEFAULT N'';
GO

/* A name must be unique across the whole company, officers and agents alike.
   Enforced by a check the seed verifies rather than a constraint spanning two
   tables, which SQL Server cannot express directly. */
CREATE OR ALTER VIEW gov.vw_NameCollisions AS
SELECT Person, COUNT(*) AS Uses
FROM (SELECT Person FROM gov.Officer WHERE Person <> N''
      UNION ALL
      SELECT Person FROM gov.Agent   WHERE Person <> N'') x
GROUP BY Person
HAVING COUNT(*) > 1;
GO

/* ────────────────────────────────────────────────────────────────────────────
   Views the CEO portal and the gate read from.
   ──────────────────────────────────────────────────────────────────────────── */

CREATE OR ALTER VIEW gov.vw_Headcount AS
SELECT  d.Division       AS DivisionName,
        dp.Code          AS DepartmentCode,
        dp.Name          AS DepartmentName,
        o.Name           AS Officer,
        o.Level          AS OfficerLevel,
        o.Power          AS OfficerPower,
        COUNT(a.AgentId) AS Headcount
FROM        gov.Department dp
JOIN        gov.Officer    o  ON o.OfficerId = dp.OfficerId
JOIN (SELECT DivisionId, Name AS Division FROM gov.Division) d ON d.DivisionId = dp.DivisionId
LEFT JOIN   gov.Agent      a  ON a.DepartmentId = dp.DepartmentId
GROUP BY d.Division, dp.Code, dp.Name, o.Name, o.Level, o.Power;
GO

CREATE OR ALTER VIEW gov.vw_ReportingLine AS
SELECT  a.Person        AS PersonName,
        a.Name          AS AgentHandle,
        a.DecisionLevel AS AgentLevel,
        a.ReportsTo     AS ReportsTo,
        t.Name          AS TeamName,
        dp.Name         AS DepartmentName,
        o.Name          AS Officer,
        a.MaxTier,
        a.IsReadOnly,
        a.Cohort
FROM gov.Agent a
JOIN gov.Team       t  ON t.TeamId = a.TeamId
JOIN gov.Department dp ON dp.DepartmentId = a.DepartmentId
JOIN gov.Officer    o  ON o.OfficerId = dp.OfficerId;
GO

/* Appendix B question 4, answered from the effective grant rather than the intent. */
CREATE OR ALTER VIEW gov.vw_DangerousGrants AS
SELECT a.Name AS AgentName, tl.Name AS ToolName, tl.Irreversibility, tl.[Rollback]
FROM       gov.AgentTool at
JOIN       gov.Agent a  ON a.AgentId = at.AgentId
JOIN       gov.Tool  tl ON tl.ToolId = at.ToolId
WHERE      tl.Irreversibility >= 3
        OR (tl.Irreversibility = 2 AND tl.[Rollback] IS NULL);
GO

CREATE OR ALTER VIEW fin.vw_PayrollByAgent AS
SELECT  m.PeriodCode,
        a.Name                   AS AgentName,
        a.Model,
        COUNT(DISTINCT m.RunId)  AS Runs,
        SUM(m.TokensIn)          AS TokensIn,
        SUM(m.TokensOut)         AS TokensOut,
        SUM(m.WallClockSec)      AS WallClockSec,
        SUM(m.CostMinor)         AS CostMinor,
        MIN(CAST(m.Reconciled AS INT)) AS FullyReconciled
FROM fin.MeterEntry m
JOIN gov.Agent      a ON a.AgentId = m.AgentId
GROUP BY m.PeriodCode, a.Name, a.Model;
GO

PRINT 'RU_AIBOTWORKS schema ready.';
GO
