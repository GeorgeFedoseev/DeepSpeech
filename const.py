import os

curr_dir_path = os.path.dirname(os.path.realpath(__file__))


DATA_DIR = os.path.join(curr_dir_path, "data/")

VIDEO_DATA_DIR = os.path.join(DATA_DIR, "media_data/")

# DeepSpeech Model Setup
DEEP_SPEECH_N_HIDDEN = 2048
DEEP_SPEECH_CHECKPOINT_DIR = "/home/gosha/Projects/DeepSpeech/data/yt-vad-1k-2048-checkpoints/"
DEEP_SPEECH_ALPHABET_PATH = os.path.join(DATA_DIR, "alphabet.txt")

DEEP_SPEECH_LM_PATH = os.path.join(DATA_DIR, "lm", "lm.binary")
DEEP_SPEECH_TRIE_PATH = os.path.join(DATA_DIR, "lm", "trie")

TRANSCRIBED_DATA_PATH  = os.path.join(DATA_DIR, "transcribed_data/")
TRANSCRIBED_SPEECH_SQLITE_DB_PATH = os.path.join(TRANSCRIBED_DATA_PATH, "transcribed_speech.sqlite3")
TRANSCRIBED_WHOOSH_INDEX_DIR_PATH = os.path.join(TRANSCRIBED_DATA_PATH, "whoosh_index")



# audio related
SAMPLE_RATE = 16000
BYTE_WIDTH = 2