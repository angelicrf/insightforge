# InsightForge

InsightForge is an enterprise-grade, multi-agent support platform.

This repository is split into dedicated frontend and backend folders.

## Repository Layout

- `backend/` Python FastAPI backend, workers, integrations, tests, and deployment assets.
- `frontend/` Streamlit frontend workspace for the operator UI and assistant interactions.
- `.github/workflows/` CI/CD pipelines at repository root.

## Backend Structure

- `backend/app/` backend application source.
- `backend/docs/` backend architecture and operational documentation.
- `backend/docker/` backend container assets and local compose support.
- `backend/kubernetes/` backend deployment manifests.
- `backend/tests/` backend automated tests.

## Running Backend Locally

1. Change directory into `backend`.
2. Install dependencies from `requirements.txt`.
3. Run `python run_dev.py`.

## Running Frontend Locally

1. Install frontend dependencies from `frontend/requirements.txt`.
2. Run `streamlit run frontend/streamlit_app.py` from the repository root.
