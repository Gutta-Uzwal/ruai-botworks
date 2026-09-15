#!/usr/bin/env python3
"""
ru_aibotworks_names.py — give every agent a personal name.

Each agent has two identities:

    handle        python-pro              what the system dispatches
    name          Ravi                    what a person calls it

The handle says what it does and must stay machine-stable. The name is how the CEO
and the client refer to an employee, and it must stay *personally* stable: nobody's
name should change because somebody else was hired.

So assignment happens once, into REGISTRY/names.yaml,
which is then authoritative. Re-running only fills gaps for new hires. Removing an
agent retires its name rather than recycling it — a retired name is never reissued,
because a name that has meant two different things in an audit trail is worse than
no name at all.

    python ru_aibotworks_names.py           # assign names to anyone missing one
    python ru_aibotworks_names.py --check   # fail if anyone is unnamed
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ru_aibotworks_registry import Company  # noqa: E402

NAMES_FILE = (
    Path(__file__).resolve().parent.parent
    / "REGISTRY"
    / "names.yaml"
)

# One word each. Pronounceable, varied, and distinct enough to be told apart at a
# glance in a list of several hundred.
POOL: list[str] = [
    # ── a ──
    "Aarav", "Aditya", "Arjun", "Ayaan", "Advik", "Akash", "Amit", "Ajay", "Alok",
    "Ashwin", "Anil", "Ansh", "Aryan", "Atharv", "Aanya", "Aadhya", "Anika", "Ananya",
    "Anjali", "Asha", "Adam", "Alice", "Alfie", "Amelia", "Alexander", "Archie",
    "Arthur", "Astrid", "Ava", "Amara", "Amir", "Anton", "Anya", "Ade", "Aiko",
    # ── b–c ──
    "Benjamin", "Bharat", "Bhavna", "Bisi", "Bo", "Caleb", "Camille", "Carmen",
    "Charlie", "Charlotte", "Chen", "Chetan", "Chike", "Chitra", "Clara", "Cora",
    # ── d–e ──
    "Daisy", "Daniel", "Dayo", "Deepa", "Deepak", "Diego", "Divya", "Diya", "Dmitri",
    "Dhruv", "Edward", "Ekta", "Elena", "Eli", "Ella", "Elsie", "Emi", "Emily",
    "Erik", "Ethan", "Eun", "Evie",
    # ── f–h ──
    "Falguni", "Farid", "Felix", "Femi", "Feng", "Florence", "Freddie", "Freya",
    "Gaurav", "Geeta", "George", "Gita", "Grace", "Greta", "Hana", "Haru", "Harry",
    "Harsh", "Hazel", "Hema", "Henry", "Hugo", "Hui", "Hyun",
    # ── i–k ──
    "Idris", "Indira", "Ingrid", "Iris", "Isaac", "Isha", "Ishaan", "Isla", "Ivy",
    "Ira", "Jack", "Jacob", "James", "Javier", "Jaya", "Ji", "Jin", "Jing", "Joon",
    "Jun", "June", "Kabir", "Kai", "Kamala", "Karim", "Karthik", "Katya", "Kavya",
    "Kemi", "Kenji", "Kiaan", "Kiara", "Klaus", "Kofi", "Krishna",
    # ── l–n ──
    "Lakshmi", "Lars", "Latha", "Layla", "Lei", "Leila", "Lena", "Leo", "Lily",
    "Logan", "Louis", "Luca", "Lucas", "Lucia", "Maeve", "Mala", "Manish", "Marco",
    "Mason", "Mateo", "Matthew", "Max", "Mei", "Meera", "Miguel", "Min", "Ming",
    "Mia", "Mohit", "Myra", "Nadia", "Nandini", "Nathan", "Naveen", "Navya", "Neha",
    "Nia", "Nikhil", "Nikolai", "Nils", "Nisha", "Noah", "Noor", "Nora",
    # ── o–r ──
    "Olivia", "Oliver", "Omar", "Oscar", "Owen", "Padma", "Paula", "Pablo", "Pierre",
    "Pooja", "Poppy", "Pranav", "Praveen", "Prisha", "Radha", "Rahul", "Rajesh",
    "Ramon", "Rani", "Rania", "Ravi", "Rekha", "Ren", "Reyansh", "Riya", "Rohan",
    "Rosa", "Rosie", "Ruby", "Rudra", "Rufus", "Ryo",
    # ── s–t ──
    "Saanvi", "Sachin", "Sadie", "Saga", "Salma", "Sami", "Samuel", "Sanjay",
    "Savita", "Segun", "Seo", "Shaurya", "Shreya", "Siddharth", "Silas", "Simi",
    "Sita", "Sneha", "Sofia", "Sophia", "Sora", "Sunita", "Suresh", "Tae", "Tanvi",
    "Tara", "Tariq", "Theo", "Thomas", "Tunde", "Tarun",
    # ── u–z ──
    "Uday", "Uma", "Usha", "Varun", "Veena", "Veer", "Vihaan", "Vikram", "Vinay",
    "Vivaan", "Wei", "Willa", "William", "Yash", "Yemi", "Yoon", "Yuki", "Yun",
    "Yusuf", "Zara", "Zuri",
    # ── reserve, for hires beyond the current roster ──
    "Abel", "Bela", "Cyrus", "Dara", "Esme", "Faye", "Gil", "Hugh", "Imre", "Jonas",
    "Kira", "Liv", "Milo", "Nina", "Otto", "Pia", "Quinn", "Rune", "Suvi", "Tove",
    "Ulla", "Vera", "Wren", "Xavi", "Yara", "Zane", "Ada", "Bram", "Cleo", "Dov",
    "Enid", "Finn", "Gwen", "Halle", "Ines", "Joss", "Kit", "Lior", "Mira", "Noam",
]


def load_existing() -> dict:
    if NAMES_FILE.exists():
        with NAMES_FILE.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return {}


def assign(check_only: bool = False) -> int:
    company = Company.load()
    doc = load_existing()
    assigned: dict[str, str] = dict(doc.get("assigned", {}))
    retired: list[str] = list(doc.get("retired", []))

    # Everyone who needs a name: officers first, so the leadership keeps the
    # earliest names across regenerations, then the workforce in registry order.
    handles = [o.name for o in company.officers] + [a.name for a in company.agents]

    taken = set(assigned.values()) | set(retired)
    missing = [h for h in handles if h not in assigned]

    if check_only:
        if missing:
            print(f"DEFECT  {len(missing)} agent(s) have no name:", file=sys.stderr)
            for h in missing[:10]:
                print(f"        {h}", file=sys.stderr)
            print("        run: python ru_aibotworks_names.py", file=sys.stderr)
            return 1
        dupes = [n for n in set(assigned.values()) if list(assigned.values()).count(n) > 1]
        if dupes:
            print(f"DEFECT  duplicate names: {sorted(dupes)}", file=sys.stderr)
            return 1
        print(f"all {len(assigned)} agents are named, every name unique")
        return 0

    pool = [n for n in POOL if n not in taken]
    if len(pool) < len(missing):
        print(
            f"DEFECT  {len(missing)} agents need names but only {len(pool)} remain in "
            f"the pool. Extend POOL in {NAMES_FILE.name}'s generator.",
            file=sys.stderr,
        )
        return 1

    for handle, name in zip(missing, pool):
        assigned[handle] = name

    # Anyone in the file who is no longer in the registry has left the company.
    current = set(handles)
    departed = [h for h in assigned if h not in current]
    for handle in departed:
        retired.append(assigned.pop(handle))

    out = {
        "_note": (
            "Personal names. Assigned once and authoritative thereafter: nobody's name "
            "changes because somebody else was hired. Retired names are never reissued, "
            "because a name that has meant two different things in an audit trail is "
            "worse than no name at all."
        ),
        "assigned": dict(sorted(assigned.items())),
        "retired": sorted(set(retired)),
    }
    NAMES_FILE.write_text(
        yaml.safe_dump(out, sort_keys=False, width=88, allow_unicode=True), encoding="utf-8"
    )

    print(f"named {len(missing)} new agent(s); {len(assigned)} named in total")
    if departed:
        print(f"retired {len(departed)} name(s) from departed agents")
    print(f"  pool remaining: {len(POOL) - len(assigned) - len(retired)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if any agent is unnamed")
    args = parser.parse_args()
    return assign(check_only=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
