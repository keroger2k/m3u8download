FROM node:18

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip ffmpeg

# Set up the working directory
WORKDIR /workspace

# Copy application files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r backend/requirements.txt

# Install frontend dependencies
RUN cd frontend && npm install
