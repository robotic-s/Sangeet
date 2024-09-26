# Use Ubuntu 23.04 as the base image
FROM ubuntu:23.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Update and upgrade the system, install dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-venv python3-pip ffmpeg curl gnupg2 software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up auto-updates
RUN apt-get install -y unattended-upgrades && \
    echo 'APT::Periodic::Update-Package-Lists "1";' >> /etc/apt/apt.conf.d/20auto-upgrades && \
    echo 'APT::Periodic::Unattended-Upgrade "1";' >> /etc/apt/apt.conf.d/20auto-upgrades

# Create and activate virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Set working directory
WORKDIR /app

# Create sangeetpro directory
RUN mkdir /app/sangeetpro

# Copy all files from current directory and subdirectories to sangeetpro
COPY . /app/sangeetpro/

# Set working directory to sangeetpro
WORKDIR /app/sangeetpro

# Upgrade pip and install dependencies in the virtual environment
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Gunicorn, gevent, and python-dotenv in the virtual environment
RUN pip install --no-cache-dir gunicorn gevent python-dotenv

# Script to update FFmpeg, load environment variables, and start the application
RUN echo '#!/bin/bash\n\
source $VIRTUAL_ENV/bin/activate\n\
apt-get update && apt-get install -y ffmpeg &\n\
if [ -f .env ]; then\n\
    set -a\n\
    . ./.env\n\
    set +a\n\
fi\n\
gunicorn --bind 0.0.0.0:${PORT:-80} --workers ${WORKERS:-4} --threads ${THREADS:-2} --worker-class gevent app2:app' > /app/sangeetpro/start.sh && \
    chmod +x /app/sangeetpro/start.sh

# Expose port (default to 80, but can be overridden)
EXPOSE ${PORT:-80}

# Command to run on container start
CMD ["/bin/bash", "/app/sangeetpro/start.sh"]