# School architecture

The School template uses Django for the public content API, contact boundary,
administrative workflow, and server-side controls. React provides the public
presentation layer.

Public endpoints return published content only and use explicit response
objects. Contact submissions are validated and return a generic success
response. A future portal must use a separate authenticated namespace,
authorization policy, serializers, and database boundary.

Production uses PostgreSQL. SQLite is permitted only for local development and
tests. The first release stores no minor personal information in public content
or contact responses.
