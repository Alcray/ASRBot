# Telegram ASR Bot

This repository contains a Python script for a Telegram bot that uses NVIDIA's NeMo ASR models to transcribe voice messages. The bot can handle both locally stored models and pre-trained Hugging Face models.

## Overview
- **Purpose**: Transcribe voice messages sent to the Telegram bot.
- **Key Features**:
  - Supports local NeMo ASR models and Hugging Face models.
  - Converts `.ogg` voice messages to `.wav` format for transcription.
  - Deletes temporary `.ogg` files after processing.

## Prerequisites
### 1. Docker Environment
To ensure all dependencies are met, start a Docker environment:

```bash
docker run --gpus all -it -v /home:/home -v /mnt/data:/mnt/data --shm-size=8g \
-p 8888:8888 -p 6006:6006 --ulimit memlock=-1 --ulimit \
stack=67108864 --device=/dev/snd --name nemodockergpu nvcr.io/nvidia/nemo:24.09
```

### 2. Install Required Python Packages
After starting the Docker container, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
The bot requires a configuration file in the `config/` directory. Use `config.yaml` as the default configuration file. Below is an example configuration:

### `config/config.yaml`
```yaml
# Path to the local model file. This will be used first if it exists.
model_path: '/path/to/alternate/model/if/needed.nemo'

# Name of the Hugging Face model to fall back on if the local model is not available.
hf_model_name: 'nvidia/stt_hy_fastconformer_hybrid_large_pc'

# Token for the Telegram bot to interact with your work PC.
telegram_token: 'your_bot_token'
```

**Notes:**
- Replace `/path/to/alternate/model/if/needed.nemo` with the actual path to your local NeMo ASR model.
- Replace `your_bot_token` with the Telegram bot token.
- If you want to use a different configuration file (e.g., for another environment), create it in the `config/` directory and update the `config_path` in the script accordingly.

### `.gitignore`
To ensure sensitive information is not committed:

```bash
# Ignore sensitive configuration files
config/workpc_config.yaml

# Ignore workspace directory
workspace/

# Ignore Python virtual environment
asrdemo/

# Ignore other temporary or log files
*.log
*.pyc
__pycache__/
```

## How to Run
1. Ensure the Docker environment is running.
2. Verify the configuration file (`config/config.yaml`) is correctly set up.
3. Start the bot using the following command:

```bash
python ArmenianASRbot.py
```

## Functionality
- **Starting the Bot**:
  - Send `/start` to the bot to begin.
- **Sending a Voice Message**:
  - Send a voice message, and the bot will:
    1. Download the `.ogg` file.
    2. Convert it to `.wav`.
    3. Transcribe the message using the NeMo ASR model.
    4. Respond with the transcribed text.

## Workspace
The `workspace/` directory is used to store temporary user files (e.g., `.ogg` and `.wav` files). Subdirectories are created for each user based on their Telegram ID.

## Cleaning Up
The bot automatically deletes `.ogg` files after conversion to `.wav`.

## Support
For issues or questions, please contact the repository maintainer.
