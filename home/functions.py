# Importing necessary libraries.

import PyPDF2
import ffmpeg
import shlex, subprocess
import pyttsx3
from gtts import gTTS
import os
from IPython.display import HTML
from base64 import b64encode
from os import startfile

# Removing existing uploaded/generated files from the folder so that name conflicting errors
# do not occur while running the code multiple times.
def remove_files():
    try:
        os.remove('uploads/input_audio.mp3')
    except:
        print("No input_audio file found!")
    try:    
        os.remove('outputs/final_op_video.mp4')
    except:
        print("No final_op_video file found!")
    try:
        os.remove('outputs/output_audio.mp3')
    except:
        print("No output_audio file found!")
    try:
        os.remove('uploads/input_transcript.pdf')
    except:
        print("No input_transcript file found!")
    try:
        os.remove('uploads/input_video.mp4')
    except:
        print("No input_video file found!")
    try:
        os.remove('uploads/input_video_without_sound.mp4')
    except:
        print("No input_video_without_sound file found!")
    try:
        os.remove('outputs/final_compressed.mp4')
    except:
        print("No final_compressed file found!")
    
    return "Files deleted."


# Generating speech from text in female voice using GTTS.
def female_voice_output(input_text):
    language = 'en'
    output_audio = gTTS(text=input_text, lang=language, slow=False)
    output_audio.save('outputs/output_audio.mp3')


# Generating speech from text in male voice using pyttsx3.
def male_voice_output(input_text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)
    engine.save_to_file('{}'.format(input_text), 'outputs/output_audio.mp3')
    engine.runAndWait()


# Removing audio from user input video using ffmpeg. 
def remove_audio():
    cmd = "ffmpeg -i uploads/input_video.mp4 -vcodec copy -an 'uploads/input_video_without_sound.mp4'"
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    

# Compressing the video using ffmpeg
def compress():
    cmd = "ffmpeg -i outputs/final_op_video.mp4 'outputs/final_compressed.mp4'"
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


# Merging audio(generated from text to speech) and video using ffmpeg.
def merge_with_generated_audio():
    cmd = "ffmpeg -i uploads/input_video_without_sound.mp4 -i outputs/output_audio.mp3 -vcodec copy 'outputs/final_op_video.mp4'"
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


# Merging user uploaded audio and video using ffmpeg.
def merge_with_uploaded_audio():
    cmd = "ffmpeg -i uploads/input_video_without_sound.mp4 -i uploads/input_audio.mp3 -vcodec copy 'outputs/final_op_video.mp4'"
    p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    

# Extracting text from uploaded transcript.
def extract_from_pdf(pdf_name):
    pdf_file = open('uploads/{}'.format(pdf_name), 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    read_pdf.getIsEncrypted()
    read_pdf.numPages
    page1 = read_pdf.getPage(0)
    
    return page1.extractText().split("\n")


# Saving the uploaded file 1 (transcript) in uploads folder.
def handle_uploaded_file(f):  
    with open('uploads/input_transcript.pdf', 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  
    return f.name


# Saving the uploaded file 2 (video) in uploads folder.
def handle_second_uploaded_file(f):  
    with open('uploads/input_video.mp4', 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  
    return f.name


# Saving the uploaded file 3 (audio) in uploads folder.
def handle_third_uploaded_file(f):  
    with open('uploads/input_audio.mp3', 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  
    return f.name


# Playing the video using inbuilt media player.
def play_video():
    cwd = os.getcwd()
    os.chdir(cwd)
    os.system("start " + "outputs/final_compressed.mp4")

    
