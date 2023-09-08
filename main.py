from pytube import YouTube
import moviepy.editor as medit
import torchaudio
import torch
from pathlib import Path
import streamlit as st


# link of the video to be downloaded
link="https://www.youtube.com/watch?v=xWOoBJUqlbI"

def download_yt_video(url):
	try:
		yt = YouTube(url)
	except:
		print("Connection Error")
		return False

	try:
		yt.title = "target_clip"
		yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
	except:
		print("Issue in downloading Youtube video")
		return False
	return True

def extract_audio(video_file = "target_clip.mp4"):
	video = medit.VideoFileClip(video_file)
	video.audio.write_audiofile("extracted_audio.wav")


def s2st_yt_audio(audio_file = "./extracted_audio.wav"):
	audio_input, _ = torchaudio.load(audio_file, format="mp3")
	s2st_model = torch.jit.load("models/unity_on_device.ptl")

	with torch.no_grad():
		text, units, waveform = s2st_model(audio_input, tgt_lang="eng-hin") # S2ST model also returns waveform

	print(text)
	torchaudio.save(f"result.wav", waveform.unsqueeze(0), sample_rate=16000) # Save output waveform to local file

def combine_video_with_audio(video_file = "target_clip.mp4", audio_file = "result.wav"):
	video_clip = VideoFileClip(video_file)
	audio_clip = AudioFileClip(audio_file)
	translated_clip = video_clip.set_audio(audio_clip)
	final_clip.write_videofile("translated.mp4")	

st.title("YTube Trans")
st.write("Translate YouTube videos into your desired language!")

youtube_url = st.text_input("Enter YouTube URL:")

target_language = st.selectbox("Select Target Language:", ["Select Language", "Spanish", "French", "German"])

if st.button("Translate"):
    if youtube_url:
        st.video(youtube_url)

        if target_language != "Select Language":
            try:
                if download_yt_video(youtube_url):
                    print("Downloaded video")
                    extract_audio()
                    s2st_yt_audio()
                    combine_video_with_audio()
                    st.video("translated.mp4")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please select a target language.")
    else:
        st.warning("Please enter a valid YouTube URL.")

# FAQ section
st.sidebar.title("Frequently Asked Questions (FAQ)")
st.sidebar.write("Q: How does this app work?")
st.sidebar.write("A: This app allows you to enter a YouTube URL, select a target language, and translate the video title and audio into the chosen language.")

st.sidebar.write("Q: What libraries are used?")
st.sidebar.write("A: This app uses PyTube for downloading YouTube videos, MoviePy for video processing, and Google Translate for text translation.")

st.sidebar.write("Q: What video formats are supported?")
st.sidebar.write("A: Currently, this app supports videos that can be processed by the MoviePy library. Common formats like MP4 should work well.")

st.sidebar.write("Q: Is there a limit to the video length?")
st.sidebar.write("A: The processing time and feasibility depend on the length and quality of the video. Longer videos may take more time to translate.")

st.sidebar.write("Q: Can I download the translated video?")
st.sidebar.write("A: Yes, the translated video will be available for download after translation.")

st.sidebar.write("Q: Is there any cost for using this app?")
st.sidebar.write("A: No, this app is provided free of charge, but it uses external services like YouTube and Google Translate, which may have their own usage policies.")

st.sidebar.write("Q: Who created this app?")
st.sidebar.write("A: This app was created by a Python developer: Tharun G.")
