from typing import Dict

from numpy import sort
from Clarinet.search import similarity
from Clarinet.evaluation import analyse
from Clarinet.converter import midi2text
from os import listdir,path
import os
import json
from tqdm import tqdm
import miditoolkit


def midiFolderToDict(folder:str,num_files:int,num_notes=-1,channel=0)->Dict: # Returns a dict of form {filelocation:text_representation}
    file_locations=sort([f"{folder}/{filename}" for filename in listdir(folder)])
    
    output_dict={}
    if num_files==-1:
        for file in tqdm(file_locations):
            if file.endswith(".mid"):
                output_dict[file]=midi2text(file,channel=channel,num_notes=num_notes)
        return(output_dict)
    else:
        for file in tqdm(file_locations[:num_files]):
            if file.endswith(".mid"):
                output_dict[file]=midi2text(file,channel=channel,num_notes=num_notes)
        return(output_dict)


def generateText(folder,num_files=-1,output_folder="Text",num_notes=-1,channel=0):
    out_dict=midiFolderToDict(folder,num_files,num_notes=num_notes,channel=channel)
    for file,text in out_dict.items():
        foldername=f"{output_folder}/{file.split('/')[-2]}"
        if not path.exists(foldername):
            os.mkdir(foldername)
        filename=f"{file.split('/')[-1]}".replace(".mid",".txt")
        with open(f"{foldername}/{filename}","w") as f:
            f.write(text)


midi_folder="Data/Noisy Queries"
num_files=-1
num_notes=8
channel=0

for folder in tqdm(os.listdir(midi_folder)):
    folder_location=f"{midi_folder}/{folder}"
    generateText(folder_location,output_folder="Text/Noisy Queries",num_files=num_files,num_notes=num_notes,channel=channel)