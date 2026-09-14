# School project

This is the root-level Lane A School project.

- `backend/` contains the Django public API.
- `frontend/` contains the React public site.
- Portal authentication and private student, parent, teacher, or administrator
  records are intentionally out of scope for this release.

Run the backend with:

```text
cd projects/school/backend
uv run python manage.py runserver 127.0.0.1:8000
```

Run the frontend with:

```text
cd projects/school/frontend
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```
