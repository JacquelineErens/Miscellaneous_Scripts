import csv
import os

''' Code to take transcription lines from a csv and make text files for them: necessary for use of the Montreal Forced Aligner '''

''' Set global variables before running code as this will depend on what you used as labels for your CSV column headers
    CSV_NAME is the name of your data file
    PARTICIPANT_LABEL is what you used for your participant codes
    TRANSCRIPTION_COLUMN is the column you have your transcription in
    ITEM_IDENTIFIER is a variable for your item numbers so you can keep track of which transcription goes with which item. '''

CSV_NAME = "Dative_Data.csv"
PARTICIPANT_LABEL = '\ufeffFolderCode'
TRANSCRIPTION_COLUMN = 'Transcription'
ITEM_IDENTIFIER = 'ItemNum'

def make_participant_folders(csv_in):
    participant_codes = set()

    #read through csv to get participant files and put them in set so no duplicates
    with open(csv_in, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant_codes.add(row[PARTICIPANT_LABEL])

    #cast set as list, iterate through it, make a folder for each participant ID
    for code in (list(participant_codes)):
        if not os.path.exists(os.getcwd()+"/Dative_Timing/"+code):
            os.chdir(os.getcwd()+"/Dative_Timing/")
            os.mkdir(code)
            os.chdir("..")

    #return the list for future use
    print(list(participant_codes))
    return(list(participant_codes))

def make_transcription_text_files(files_list, csv_in_path):
    current_path = os.getcwd()+"/Dative_Data.csv"
    print(current_path)
    for f in files_list: #for the participant code you're working on out of all participants you have transcripts for
        os.chdir(os.getcwd()+"/Dative_Timing/"+f) #go into their folder
        with open(current_path, newline='') as csvfile: #open the data csv
            reader = csv.DictReader(csvfile)
            for row in reader: #iterate row by row
                if row[PARTICIPANT_LABEL] == f: #make sure you're only getting transcripts for that participant
                    with open(str(row[PARTICIPANT_LABEL]) + "_" + str(row[ITEM_IDENTIFIER]) + ".txt", "w") as t: #write a text file with participant & item number identifiers
                        text = str(row[TRANSCRIPTION_COLUMN])
                        t.write(text) #only write the transcription though
        os.chdir("../..")

participant_folders = make_participant_folders('Dative_Data.csv')
make_transcription_text_files(participant_folders, 'Dative_Data.csv')
