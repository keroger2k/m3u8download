FROM node:18

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv ffmpeg

# Set up the working directory
WORKDIR /workspace

# Copy application files
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

# Create a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r backend/requirements.txt

# Install frontend dependencies
RUN cd frontend && npm install && npm install concurrently
