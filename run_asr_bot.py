import argparse
import telebot
import yaml
import nemo.collections.asr as nemo_asr
from pydub import AudioSegment
import os
from datetime import datetime

# Load configuration
config_dir = 'config'
config_path = os.path.join(config_dir, 'workpc_config.yaml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

def load_asr_model(model_path=None, hf_model_name=None):
    if model_path and os.path.exists(model_path):
        return nemo_asr.models.EncDecHybridRNNTCTCBPEModel.restore_from(model_path)
    elif hf_model_name:
        return nemo_asr.models.EncDecHybridRNNTCTCBPEModel.from_pretrained(model_name=hf_model_name)
    else:
        raise ValueError("Neither model path nor HF model name provided.")

# Initialize parser and add arguments
parser = argparse.ArgumentParser(description='Telegram Bot for ASR using a NeMo model.')
parser.add_argument(
    '--model_path', 
    type=str, 
    help='The file path to the NeMo ASR model.', 
    default=config.get('model_path')
)
parser.add_argument(
    '--hf_model_name', 
    type=str, 
    help='The Hugging Face model name.', 
    default=config.get('hf_model_name')
)
parser.add_argument(
    '--token', 
    type=str, 
    help='The Telegram bot token.', 
    default=config.get('telegram_token')
)
args = parser.parse_args()

# Load ASR model
asr_model = load_asr_model(model_path=args.model_path, hf_model_name=args.hf_model_name)

# Initialize bot with the given token
bot = telebot.TeleBot(args.token)

# Create a workspace directory to store user files
workspace_dir = 'workspace'
if not os.path.exists(workspace_dir):
    os.makedirs(workspace_dir)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Send me a voice message and I will transcribe it.')

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    # Retrieve file info and download the voice message
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Create a directory for the user based on their ID
    user_id = message.from_user.id
    user_dir = os.path.join(workspace_dir, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    # Create timestamped file names
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ogg_path = os.path.join(user_dir, f'voice_{timestamp}.ogg')
    wav_path = os.path.join(user_dir, f'voice_{timestamp}.wav')
    
    # Save the downloaded OGG file
    with open(ogg_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Convert OGG to WAV
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format='wav')

    # Delete the original OGG file
    os.remove(ogg_path)

    # Transcribe the WAV file using the specified model
    transcription = asr_model.transcribe([wav_path])[0][0]
    bot.send_message(message.chat.id, f'Transcribed text: {transcription}')

def main():
    bot.polling()

if __name__ == '__main__':
    main()
