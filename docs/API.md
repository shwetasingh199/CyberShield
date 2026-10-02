# REST API

The application exposes a local Flask REST API.

All data is synthetic/demo data.

## Health

### GET /api/health

Returns application health.

Example:

```json
{
  "status": "ok",
  "mode": "SYNTHETIC / DEMO ONLY"
}