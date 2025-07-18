#!/bin/bash
# Install Python dependencies
. /opt/venv/bin/activate && pip install --no-cache-dir -r backend/requirements.txt
# Install frontend dependencies
(cd frontend && npm install && npm install concurrently)
# Run the application
(cd frontend && npm run start:dev) &
wait -n
exit $?
