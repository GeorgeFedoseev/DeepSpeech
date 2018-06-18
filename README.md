# DeepSpeech for Russian language

Project DeepSpeech is an open source Speech-To-Text engine [implemented by Mozilla](https://github.com/mozilla/DeepSpeech), 
based on [Baidu's Deep Speech research paper](https://arxiv.org/abs/1412.5567)
using [TensorFlow](https://www.tensorflow.org/).

This particular repository is focused on creating big vocabulary ASR system for Russian language.

Big datasets for training are being crawled
using [developed method](https://github.com/GeorgeFedoseev/YouTube-Captions-Based-Speech-Dataset-Parser) 
from YouTube videos with captions.

Developed speech recognition system for Russian language achieves 21% WER on custom
dataset crawled from [voxforge.com](http://www.repository.voxforge1.org/downloads/Russian/Trunk/Audio/Main/16kHz_16bit/).


Created ASR system was applied to speech search task in big collection of video files. Implemented search service allows to jump to a particular moment in video where requested text is being spoken.


Here is a demo:  


![search-demo-5](demo/gifs/search-demo-5.gif)

# Using [released files](https://github.com/georgefedoseev/DeepSpeech/releases)
## Using released files for inference
You will need Mac OS or Linux  
1. Follow [this Mozilla's DeepSpeech guide](https://github.com/mozilla/DeepSpeech#using-the-python-package) to install pip3 deepspeech package.
2. Go to [releases](https://github.com/georgefedoseev/DeepSpeech/releases) and download `tensorflow_pb_models.tar.gz` and `language_model.tar.gz`.  
2. Unpack all files (`output_graph.pb`, `lm.binary`, `trie` and `alphabet.txt`) to some folder. And run inference:
```
deepspeech output_graph.pb alphabet.txt lm.binary trie my_russian_speech_audio_file.wav
```
## Continue training from released checkpoint
Checkpoint is a directory that you specify as `--checkpoint_dir` parameter when training with `DeepSpeech.py`. You can continue training TensorFlow acoustic model from released checkpoint with your own datasets.  
Released checkpoints are using `--n_hidden=2048` (number of neurons in hidden layers in neural network), and it cannot be modified if you want to use this released checkpoint (for values other than 2048 it will throw an error).
  
To use released checkpoint in your training:  
1. Follow [Training setup guide](#training-setup)
2. Extract `checkpoint_dir.tar.gz` archive downloaded from [release](https://github.com/georgefedoseev/DeepSpeech/releases) somewhere in your `/network/checkpoints` directory (or any other). Change absolute paths to main checkpoint file in `checkpoint` text file. Example of `checkpoint` file contents:
```
model_checkpoint_path: "/network/DeepSpeech-ru-v1.0-checkpoint_dir/model.ckpt-126656"
all_model_checkpoint_paths: "/network/DeepSpeech-ru-v1.0-checkpoint_dir/model.ckpt-126656"
```
3. Train with your own datasets setting `--checkpoint_dir` parameter to directory that you extracted checkpoint to.

# Training setup

* [Requirements](#requirements)
* [Setting up training environment](#setting-up-training-environment)
* [Define alphabet in `alphabet.txt`](#define-alphabet-in-alphabettxt)
* [Generate language model](#generate-language-model-using-kenlm-toolkit-and-generate_trie-under-the-hood)
* [Training on sample dataset](#training-on-sample-dataset-datatiny-dataset)
* [Setup Telegram notifications](#setup-telegram-notifications)



### Requirements:  
- Good NVIDIA GPU with at least 8GB of VRAM
- Linux OS
- `cuda-command-line-tools`
- `docker`
- `nvidia-docker` (for CUDA support)


## Setting up training environment

1. Check `nvidia-smi` command is working before moving to the next step
2. Clone this repo `git clone https://github.com/GeorgeFedoseev/DeepSpeech` and `cd DeepSpeech`
3. Build docker image based on `Dockerfile` from clone repo: 
```
nvidia-docker build -t deep-speech-training-image -f Dockerfile .
```
4. Run container as daemon. Link folders from host machine to docker container using `-v <host-dit>:<container-dir>` flags. We will need `/datasets` and `/network` folders in container to get access to datasets and to store Neural Network checkpoints. `-d` parameter runs container as daemon (we will connect to container on next step):
```
docker run --runtime=nvidia -d --name deep-speech-training-container -v /<path-to-some-assets-folder-on-host>:/assets -v /<path-to-datasets-folder-on-host>:/datasets -v /<path-to-some-folder-to-store-NN-checkpoints-on-host>:/network deep-speech-training-image
```
5. Connect to running container (`bash -c` command is used to sync width and height of console window).
```
docker exec -it deep-speech-training-container bash -c "stty cols $COLUMNS rows $LINES && bash"

```
Done! We are now inside training docker container.

## Define alphabet in `alphabet.txt`
All training samples should have transcript consisting of characters defined in `data/alphabet.txt` file. In this repository `alphabet.txt` consists of `space character`, `dash character` and russian letters. If sample transcriptions in dataset will contain out-of-alphabet characters then DeepSpeech will throw an error.

## Generate language model (using KenLM toolkit and generate_trie under the hood)
Run python script with first parameter being some long text file from where language model will be estimated (for example some Wikipedia dump txt file)
```
python /DeepSpeech/maintenance/create_language_model.py /assets/big-vocabulary.txt
```
This script also has parameters:  
- o:int - maximum length of word sequences in language model
- prune:int - minimum number of occurences for sequence in vocabulary to be in language model
  
Example with extra parameters:  
```
python /DeepSpeech/maintenance/create_language_model.py /assets/big-vocabulary.txt 3 2
```
It will create 3 files in `data/lm` folder: `lm.binary`, `trie` and `words.arpa`. `words.arpa` is intermediate file, DeepSpeech is using `trie` and `lm.binary` files for language modelling. Trie is a tree, representing all prefixes of words in LM. Each node (leaf) is a prefix and child-nodes are prefixes with one letter added.

## Training on sample dataset `data/tiny-dataset`
Dataset consists of 3 sets: train, dev and test. For each set there is CSV file and folder, containing wave files. In csv each row contains *full* path to audio, filesize in bytes and text transcription. For saving-space-in-repo purposes sample dataset has only 9 audio recordings (which is enough for demo and **not enough for good WER**). CSV file for train set repeats same 3 rows 7 times to simulate more data.  
To run demonstration of training process execute:
```
bash bin/train-tiny-dataset.sh
```
You should see **training** and **validation** progressbars running for each epoch. Training process stops when validaton error stops decreasing (early stopping). Then starts **testing** phase that uses language model (LM is not used during trainig), thats why it takes longer time for each sample to process (beam search implementation that uses language model is one-threaded and CPU only).  

Obviously with so tiny dataset good WER is not achievable. To achieve good WER (at least < 20%) use datasets with > 500hrs of speech.

You can examine which parameters are passed to `DeepSpeech.py` script by checking contents of `train-tiny-dataset.sh` file.

## Setup Telegram notifications
Because training big RNNs like in DeepSpeech takes time (from few hours to days and even weeks on weak hardware), its good to be notified about training results and not to check manually all the time.  
You can use Telegram Bot to send you log messages. Create bot in Telegram and get `accessToken`, start chatting with bot and get `chatId`. Then create `telegram_credentials.json` file in the root folder of the project with following contents:
```
{
  "accessToken": "<your-access-token>",
  "chatId": "<your-chat-id>"
}
```
To tell `DeepSpeech.py` to send you log messages through your Telegram Bot to specified chat add flag `--log_telegram=1` when running training.
