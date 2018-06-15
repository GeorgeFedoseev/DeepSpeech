import os

DEEP_SPEECH_PROJECT_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


DATA_DIR = os.path.join(DEEP_SPEECH_PROJECT_ROOT_PATH, "data/")

VIDEO_DATA_DIR = os.path.join(DATA_DIR, "media_data/")

# DeepSpeech Model Setup
DEEP_SPEECH_N_HIDDEN = 2048

DEEP_SPEECH_CHECKPOINT_DIR = "/network/yt-vad-1k-2048/yt-vad-1k-2048-checkpoints/"

DEEP_SPEECH_ALPHABET_PATH = os.path.join(DATA_DIR, "alphabet.txt")

DEEP_SPEECH_LM_DIR_PATH = os.path.join(DATA_DIR, "lm")
DEEP_SPEECH_ARPA_PATH = os.path.join(DEEP_SPEECH_LM_DIR_PATH, "words.arpa")
DEEP_SPEECH_LM_PATH = os.path.join(DEEP_SPEECH_LM_DIR_PATH, "lm.binary")
DEEP_SPEECH_TRIE_PATH = os.path.join(DEEP_SPEECH_LM_DIR_PATH, "trie")

TRANSCRIBED_DATA_PATH  = os.path.join(DATA_DIR, "transcribed_data/")
TRANSCRIBED_SPEECH_SQLITE_DB_PATH = os.path.join(TRANSCRIBED_DATA_PATH, "transcribed_speech.sqlite3")
TRANSCRIBED_WHOOSH_INDEX_DIR_PATH = os.path.join(TRANSCRIBED_DATA_PATH, "whoosh_index")



# audio related
SAMPLE_RATE = 16000
BYTE_WIDTH = 2