# preprocess-tedlium
Preprocess TED-LIUM datasets for DeepSpeech training.

### What does this repository do?
  - removes the tags (such as {NOISE}, < sil>, {BREATH}, etc.) left behind in the transcriptions
  - removes the occasional space between a word and apostraphe 's' (e.g. "men 's" -> "men's")
  - converts each sph file into segments in wav format with corresponding transcriptions
  - writes data (wav_filename, wav_filesize, transcript) to a csv file required for DeepSpeech 
  
  
### Dependencies & Prerequisites:
  - Python 3.6+
  - pydub
    

### Setup:
   - copy preprocess_data.py into the TED-LIUM base folder
   - give the function, "preprocess", its first argument (options: "train", "dev", or "test")
   - give the function, "preprocess", its second argument, which is the folder name where the preprocessed data will be outputted
   - run the script
   - you should end up with a folder containing a csv file and all of the segments in wav format
