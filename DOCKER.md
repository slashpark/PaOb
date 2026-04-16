# Docker Setup for PaOb

This Docker stack provides both backend (FastAPI) and frontend (Svelte) services.

## Files Created

- **`src/backend/Dockerfile`** - Production backend image
- **`src/frontend/PaOb/Dockerfile`** - Production frontend image  
- **`src/frontend/PaOb/Dockerfile.dev`** - Development frontend image
- **`docker-compose.yml`** - Production stack
- **`docker-compose.dev.yml`** - Development stack with hot-reload
- **`.dockerignore`** - Files to exclude from Docker build context

## Quick Start

### Production Mode
Build and run the production stack:

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173 (built and served via preview)

### Development Mode
Build and run with hot-reload:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

- Backend: http://localhost:8000 (with volume mount for live changes)
- Frontend: http://localhost:5173 (with Vite dev server, hot-reload, and HMR)

## Common Commands

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild images
```bash
docker-compose up --build
```

### Remove images and volumes
```bash
docker-compose down --volumes --rmi all
```

## Services

### Backend (FastAPI)
- **Container Name**: `paob-backend`
- **Port**: 8000
- **Image**: Python 3.11 slim
- **Features**: CORS enabled, auto-reload in dev mode

### Frontend (Svelte/SvelteKit)
- **Container Name**: `paob-frontend`
- **Port**: 5173
- **Image**: Node.js 20 Alpine
- **Dev Features**: Hot-reload with Vite

## Network

Both services connect via the `paob-network` bridge network, allowing them to communicate using service names (e.g., `http://backend:8000` from frontend).

### API Configuration
The frontend connects to the backend via the `VITE_API_URL` environment variable which defaults to `http://backend:8000`. This is configured in both docker-compose files and used in `src/frontend/PaOb/vite.config.ts` for the development proxy.

**Important**: Inside Docker containers, services communicate using their service names (not localhost). The Vite dev server uses `--host` flag to accept connections from outside the container.

## Notes

- Backend uses `PYTHONUNBUFFERED=1` to ensure real-time logs
- Frontend dev server uses `--host` flag to accept connections from outside the container
- Frontend proxy correctly targets `backend:8000` (service name) instead of `127.0.0.1:8000`
- Database and config files are persisted in the workspace volumes in dev mode
