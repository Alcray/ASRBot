# Telegram ASR Bot

This repository contains a Python script for a Telegram bot that uses NVIDIA's NeMo ASR models to transcribe voice messages. The bot can handle both locally stored models and pre-trained Hugging Face models.

## Overview
- **Purpose**: Transcribe voice messages sent to the Telegram bot.
- **Key Features**:
  - Supports local NeMo ASR models and Hugging Face models.
  - Converts `.ogg` voice messages to `.wav` format for transcription.
  - Deletes temporary `.ogg` files after processing.

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

## How to Run the Bot

### **Running with `run.sh`**
1. Use the `run.sh` script to automatically set up the Docker environment, build the Docker image, and start the container:
   ```bash
   ./run.sh
   ```
   This script will:
   - Build the Docker image.
   - Stop and remove any existing containers with the same name.
   - Start a new container for the bot.

2. Monitor the logs to ensure the bot is running:
   ```bash
   docker logs -f armenian-asr-bot
   ```

3. Interact with the bot via Telegram:
   - Send `/start` to the bot.
   - Send a voice message, and the bot will transcribe it.

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
