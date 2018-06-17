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


### Requirements:  
- Linux OS
- docker
- nvidia-docker (for CUDA support)

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

## Define alphabet alphabet.txt
All training samples should have transcript consisting of characters defined in `data/alphabet.txt` file. In this repository alphabet.txt consists of space character, dash character and russian letters. If sample transcriptions in dataset will contain out-of-alphabet characters then DeepSpeech will throw an error.

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

