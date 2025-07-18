#!/bin/sh

# Start the frontend
cd /workspace/frontend && npm run dev &

# Start the backend
. /opt/venv/bin/activate && cd /workspace/backend && flask run --host=0.0.0.0 --port=5001
