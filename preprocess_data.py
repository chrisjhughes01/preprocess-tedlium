import os
import re
import csv
from pydub import AudioSegment


def preprocess(dataset_name, processed_folder):
    transcript_files = os.listdir(dataset_name+"/stm/")

    if not os.path.isdir(processed_folder):
        os.mkdir(processed_folder)

    if not os.path.isfile(processed_folder+"/"+dataset_name+".csv"):
        with open(processed_folder+"/"+dataset_name+".csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["wav_filename", "wav_filesize", "transcript"])

    for file in transcript_files:
        filebase = file[:-4]
        print("Processing", filebase)

        convert_sph_to_wav = AudioSegment.from_file(dataset_name+"/sph/"+filebase+".sph")
        convert_sph_to_wav.export(processed_folder+"/"+filebase+".wav", format="wav")

        with open(dataset_name+"/stm/"+file) as f:
            segments = f.readlines()

        for i in range(0, len(segments)):
            segments[i] = (segments[i].strip().split(" ", 6))

        for i in range(0, len(segments)):
            #removes tags
            while "<" in segments[i][6]:
                segments[i][6] = segments[i][6][:segments[i][6].index("<")] + segments[i][6][segments[i][6].index(">")+1:]
            while "{" in segments[i][6]:
                segments[i][6] = segments[i][6][:segments[i][6].index("{")] + segments[i][6][segments[i][6].index("}")+1:]
            while "(" in segments[i][6]:
                segments[i][6] = segments[i][6][:segments[i][6].index("(")] + segments[i][6][segments[i][6].index(")")+1:]
            while "[" in segments[i][6]:
                segments[i][6] = segments[i][6][:segments[i][6].index("[")] + segments[i][6][segments[i][6].index("]")+1:]
            #removes extra and unneccessary spaces
            segments[i][6] = re.sub(" +", " ", segments[i][6]).strip(" ").replace(" '", "'")

        for i in range(0, len(segments)):
            transcript = segments[i][6]
            if transcript != 'ignore_time_segment_in_scoring':
                segment = AudioSegment.from_file(processed_folder+"/"+filebase+".wav")
                segment = segment[float(segments[i][3])*1000 : float(segments[i][4]) * 1000]
                segment.export(processed_folder+"/" + str(i) + filebase + ".wav", format="wav")

                wav_filename = str(i) + filebase + ".wav"
                wav_filesize = os.path.getsize(processed_folder+"/" +str(i) + filebase + ".wav")

                with open(processed_folder+"/"+dataset_name+".csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([wav_filename, wav_filesize, transcript])

    os.remove(processed_folder+"/"+filebase+".wav")


preprocess("train", "processed_train")
