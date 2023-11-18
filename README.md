# CloneXTTSv2

This only works with WSL2. Windows not supported and I suggest not even attempting. If you ignore this and get stuck trying to use windows, you're on your own. I wont help you as it is a massive waste of time.#

--CREATE AND ACTIVATE ENV--
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
conda create --name xtts python==3.10
conda activate xtts
```

--INSTALL TORCH--
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 (Dont use "conda install" use "pip install" conda with these repos and libraries it just doesnt work, I didnt look into it)
```
--INSTALL FMMPEG/RUST
```
sudo apt update && sudo apt install ffmpeg
pip install setuptools-rust
```
--INSTALL WHISPERX--
```
git clone https://github.com/m-bain/whisperX.git
cd whisperX
pip install -e .

--INSTALL COQUII TTS--
sudo apt-get install g++
git clone https://github.com/coqui-ai/TTS
cd TTS
pip install -e .[all,dev,notebooks]
make system-deps  (Do all three, doesnt work without it, dont know why, ask coquii)
make install

===========================================================================================================================

We need to edit Trainer.py Lines 759 - 763

   @staticmethod
    def setup_training_environment(args, config, gpu):
        if platform.system() != "Windows":
            pass                                                                               # pass
            # https://github.com/pytorch/pytorch/issues/973                                    comment out these four lines in the setup_training_environment function (759 - 763)
            # import resource  # pylint: disable=import-outside-toplevel                                   "

            # rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)                                          "
            # resource.setrlimit(resource.RLIMIT_NOFILE, (4096, rlimit[1]))                                "

========================================================================================================================

- get data set, 1 48khz wav file, MONO

- Get reference audio (length and amount unknown. Experiment)

- use segmenter.py, point it at your single 48khz audio file

- use transcriber.py, pointing it at segments folder
       The format of metadata.csv follows ljspeech. "audio1.wav|transcription|validation" or if you have no validation repeat transcription "audio1.wav|transcription|transcription"
       The script will remove any audio it doesnt understand and put it in the badAudio folder
       You have the option to validate the text. In this case the validation would come after transcription. "audio1.wav|transcription|validation"

- Convert your new segmented audio into 20500 khz audio files for training
- Go through train_gpt_xtts.py and fill out the file paths that will be unique to you

- * Change any parameters according to hardware. Pay attention to learning rate, its set to a very slow rate by default.

- in train_gpt_xtts.py/GPTTrainerConfig script the eval split was missing. It defaults to .01 by which is would'nt be enough for smaller datasets. Adjust other parameters as needed.
   config = GPTTrainerConfig(
           output_path=OUT_PATH,
           model_args=model_args,
           run_name=RUN_NAME,
           project_name=PROJECT_NAME,
           run_description="""
               GPT XTTS training
               """,
           dashboard_logger=DASHBOARD_LOGGER,
           logger_uri=LOGGER_URI,
           audio=audio_config,
           batch_size=BATCH_SIZE,
           batch_group_size=22,
           eval_batch_size=BATCH_SIZE,
           num_loader_workers=8,
           eval_split_max_size=256,
           eval_split_size=0.11,      # This line right here. If it is missing, add it. For my 151 audio files, using .11 got me to 16 eval samples. Normal number is between 15-30.
           print_step=50,
           plot_step=100,
           log_model_step=100,
           save_step=150,
           save_n_checkpoints=1,
           save_checkpoints=True,

- The segmenter is a very delicate script/process. A lot of things can go wrong very easily. It's important to just match these requirements. 
              A) 1 .wav file
              B) 48khz
              C) Mono (Do not use stereo!)
              D) Clarity (When it comes to voice cloning, dataset is a very important factor. Make sure its audible, clear of any excess background noise and a single speaker)
              E) 16bit PCM

- This is a very finnicky process with a lot of points of possible failure. Expect some trial and error. I tried to remove as much possibilty for human error as possible with transcriber.py and segmenter.py. I would still advise you to manually check at least some of the output.

- Again, and I cannot reiterate this enough. Dataset is everything, if your model comes out sounding like crap its because your dataset is crap. That would be where I go to first.

Run python3 train_gpt_xtts.py
