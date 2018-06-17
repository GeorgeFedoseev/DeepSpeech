import os


### CONSTANTS ###

# Number of neurons in hidden layers of the neural network
DEEP_SPEECH_N_HIDDEN = 2048

# WAVE audio format settings (for reading training samples from datasets)
# DeepSpeech supports only this values for now.
# Each second will be encoded with 16000 samples each one taking 2 bytes.
# Which gives 32KB per second.
SAMPLE_RATE = 16000  # 16000 Hz
BYTE_WIDTH = 2  # 2 bytes per wave value


### PATHS ###

# Main Paths
DEEP_SPEECH_PROJECT_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(DEEP_SPEECH_PROJECT_ROOT_PATH, "data/")

# Alphabet path
DEEP_SPEECH_ALPHABET_PATH = os.path.join(DATA_DIR, "alphabet.txt")

# Language Model paths
DEEP_SPEECH_LM_DIR_PATH = os.path.join(DATA_DIR, "lm")
DEEP_SPEECH_ARPA_PATH = os.path.join(DEEP_SPEECH_LM_DIR_PATH, "words.arpa")
DEEP_SPEECH_LM_PATH = os.path.join(DEEP_SPEECH_LM_DIR_PATH, "lm.binary")
DEEP_SPEECH_TRIE_PATH = os.path.join(DEEP_SPEECH_LM_DIR_PATH, "trie")



# Folder containing DeepSpeech model checkpoint to use for inference (by infer.py script)
DEEP_SPEECH_CHECKPOINT_DIR = "/network/yt-vad-1k-2048/yt-vad-1k-2048-checkpoints/"

# Video trainscriber
VIDEO_DATA_DIR = os.path.join(DATA_DIR, "media_data/")
TRANSCRIBED_DATA_PATH  = os.path.join(DATA_DIR, "transcribed_data/")
TRANSCRIBED_SPEECH_SQLITE_DB_PATH = os.path.join(TRANSCRIBED_DATA_PATH, "transcribed_speech.sqlite3")
TRANSCRIBED_WHOOSH_INDEX_DIR_PATH = os.path.join(TRANSCRIBED_DATA_PATH, "whoosh_index")



