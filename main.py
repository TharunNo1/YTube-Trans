import os
os.environ["STREAMLIT_WATCHED_MODULES"] = "[]"  # Prevent torch module watcher crash

from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip
import torchaudio
import torch
import streamlit as st
from lang_list import (
    LANGUAGE_NAME_TO_CODE,
    S2ST_TARGET_LANGUAGE_NAMES,
)

def sanitize_url(url):
    return url.strip().split("&")[0]


def download_yt_video(url):
    try:
        yt = YouTube(url)
        yt.title = "target_clip"
        stream = yt.streams.get_highest_resolution()
        # stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(filename="target_clip.mp4")
        return True
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return False


def extract_audio(video_file="target_clip.mp4"):
    try:
        video = VideoFileClip(video_file)
        video.audio.write_audiofile("extracted_audio.wav")
        return "extracted_audio.wav"
    except Exception as e:
        st.error(f"Audio extraction failed: {str(e)}")
        return None


def s2st_yt_audio(audio_file="extracted_audio.wav", target_language="English",  source_language="English"):
    try:
        audio_input, _ = torchaudio.load(audio_file)
        s2st_model = torch.jit.load("models/unity_on_device.ptl")  # Ensure this model exists
        tgt_lang_code = LANGUAGE_NAME_TO_CODE[target_language]
        src_lang_code = LANGUAGE_NAME_TO_CODE[source_language]
        with torch.no_grad():
            text, units, waveform = s2st_model(input=audio_input,tgt_lang=tgt_lang_code)

        torchaudio.save("result.wav", waveform.unsqueeze(0), sample_rate=16000)
        return "result.wav"
    except Exception as e:
        st.error(f"S2ST failed: {str(e)}")
        return None


def combine_video_with_audio(video_file="target_clip.mp4", audio_file="result.wav"):
    try:
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("translated.mp4", codec='libx264', audio_codec='aac')
        return "translated.mp4"
    except Exception as e:
        st.error(f"Combining video failed: {str(e)}")
        return None


# Streamlit UI
st.set_page_config(page_title="YTube Trans", layout="centered")
st.title("🎬 YTube Trans")
st.write("Translate YouTube videos into your desired language!")

youtube_url = st.text_input("🔗 Enter YouTube URL:")

target_language = st.selectbox("🌐 Select Target Language:", ["Select Language", "Hindi", "Spanish", "French", "German"])

if st.button("🚀 Translate"):
    if not youtube_url:
        st.warning("Please enter a valid YouTube URL.")
    elif target_language == "Select Language":
        st.warning("Please select a target language.")
    else:
        url = sanitize_url(youtube_url)
        st.info("📥 Downloading video...")
        if download_yt_video(url):
            st.success("Video downloaded!")
            st.info("🎧 Extracting audio...")
            audio_file = extract_audio()
            if audio_file:
                st.success("Audio extracted!")
                st.info("🧠 Running S2ST model...")
                translated_audio = s2st_yt_audio(audio_file, target_language)
                if translated_audio:
                    st.success("Translation complete!")
                    st.info("🎞 Combining video with translated audio...")
                    final_video = combine_video_with_audio(audio_file=translated_audio)
                    if final_video:
                        st.success("Translation done!")
                        st.video(final_video)

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
