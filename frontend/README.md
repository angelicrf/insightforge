# InsightForge Frontend

This frontend is now Streamlit-only. All Vite, React, and TypeScript assets are intended to be removed so the UI runs entirely as a Python application.

## Setup

1. Create or activate a Python virtual environment.
2. Install frontend dependencies:

   ```bash
   pip install -r frontend/requirements.txt
   ```

3. Optional: set `INSIGHTFORGE_BACKEND_URL` if your FastAPI service is not running at the default local endpoint.

## Run

From the repository root:

```bash
streamlit run frontend/streamlit_app.py
```

The backend service must be running for audio submissions to succeed.
