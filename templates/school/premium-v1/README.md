# School template — premium v1

Reference school template: Lane A (Django + React). Client projects in this
domain are built by copying this template's structure into
`projects/school/<client-project-name>/`, then diverging — never by editing
this template in place for one client.

- `backend/` contains the Django public API.
- `frontend/` contains the React public site.
- Portal authentication and private student, parent, teacher, or administrator
  records are intentionally out of scope for this release.
- See [`DESIGN.md`](DESIGN.md) for the design standard and brief this
  template must satisfy.

Run the backend with:

```text
cd templates/school/premium-v1/backend
uv run python manage.py runserver 127.0.0.1:8000
```

Run the frontend with:

```text
cd templates/school/premium-v1/frontend
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```
