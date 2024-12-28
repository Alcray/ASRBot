# Use the NVIDIA base image for GPU support
FROM nvcr.io/nvidia/nemo:24.09

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update the system and install required tools
RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg \
    libsndfile1 \
    && apt-get clean

# Set up the workspace
WORKDIR /app

# Copy your bot code and requirements file
COPY . /app

# Install Python dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Expose ports if needed (not required for Telegram bot polling)
EXPOSE 8888 6006

# Command to run the bot
CMD ["python3", "run_asr_bot.py"]
