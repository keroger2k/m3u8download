#!/bin/bash
# Install Python dependencies
. /opt/venv/bin/activate && pip install --no-cache-dir -r backend/requirements.txt
# Install frontend dependencies
(cd frontend && npm install)
# Run the application
(cd frontend && npm run dev) &
(cd backend && . /opt/venv/bin/activate && flask run --host=0.0.0.0 --port=5001) &
wait -n
exit $?
