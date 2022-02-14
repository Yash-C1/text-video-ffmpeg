# Importing necessary libraries and functions.

from distutils.command.upload import upload
from django.shortcuts import render, HttpResponse
from flask import request
from home.functions import play_video, remove_audio, handle_uploaded_file, handle_second_uploaded_file, handle_third_uploaded_file, remove_files, female_voice_output, male_voice_output, merge_with_generated_audio, merge_with_uploaded_audio, extract_from_pdf, compress 


# Create your views here.

# This index function deletes all the earlier uploaded/generated files and displays the index.html page.
def index(request):
    # Removing files.
    files_removed = remove_files()
    print(files_removed)
    return render(request,'index.html')


# The next_page function is called when the form of index.html page is submitted.
# This function records the input from user, saves them in the appropriate folders and then displays the next page.
def next_page(request):
    if request.method == "POST":
        # Getting user input text
        user_input_text = request.POST.get('input_text')
        
        # If the text is not entered, it means user will upload the transcript.
        if user_input_text == "":
            # Saving the uploaded file in the uploads folder.
            uploaded_file = handle_uploaded_file(request.FILES['fileupload'])
            # The extract_from_pdf function returns a list of text.
            text_list = extract_from_pdf('input_transcript.pdf')
            
            # Converting list into string.
            for i in text_list:
                user_input_text += i

        # Getting gender choice.    
        op_voice = request.POST.get('gender')
        
        # Text to speech according to the gender choice.
        if(op_voice) == "Male":
            male_voice_output(user_input_text)
        else:
            female_voice_output(user_input_text)
    
    return render(request, 'next_page.html')
    

# The next_page_data_submit function is called after submitting the form on next_page.html
# It records and saves the uploaded files in appropriate folders.
def next_page_data_submit(request):
    if request.method == "POST":
        uploaded_video_file = handle_second_uploaded_file(request.FILES['videoupload'])
        
        try:
            uploaded_audio_file = handle_third_uploaded_file(request.FILES['audioupload'])
        except:
            uploaded_audio_file = "None"

    # Removing audio from uploaded video.    
    try:
        uploaded_video_file_without_audio = remove_audio()    
    except:
        print("The video has no sound.")

    # Generating time delay so that the next piece of code doesn't execute before the video without sound is saved.
    counter = 0
    for i in range(5000):
        for j in range(5000):
            counter+=j

    # If the user wants to upload new audio, he can upload new audio file. If he doesnt upload
    # anything, the auto generated audio file will be used.
    if uploaded_audio_file == "None":
        print("Using auto generated audio")
        output_video = merge_with_generated_audio()
    else:
        print("Using new audio")
        output_video = merge_with_uploaded_audio()

    # Generating time delay. 
    counter = 0
    for i in range(10000):
        for j in range(5000):
            counter+=j
    
    # Compressing the video.
    compress_video = compress()
    
    return render(request, 'last_page.html')


# Playing video using inbuilt media player.
def preview_video(request):
    
    # Playing the video.
    play_video()
    return HttpResponse("Playing video... If in case the video is not visible, please go back and click on preview again!")