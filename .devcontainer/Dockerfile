# syntax=docker/dockerfile:1

FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install Node.js, npm, and npx
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Set working directory to project root
WORKDIR /workspace

# Expose frontend and backend ports
EXPOSE 3000 5000
