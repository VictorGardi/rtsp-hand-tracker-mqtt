import streamlit as st

def main():
    path_to_video = "/Users/victor/Documents/Programmering/rtsp-tracker/temp.mp4"
    video_file = open(path_to_video, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

if __name__ == "__main__":
    main()


