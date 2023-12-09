import os
import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, WebRtcMode, webrtc_streamer

class FaceEmotion(VideoTransformerBase):
    def __init__(self, output_folder):
        super().__init__()
        self.video_writer = None
        self.is_recording = False
        self.output_folder = output_folder

    def start_recording(self):
        if not self.is_recording:
            codec = cv2.VideoWriter_fourcc(*"mp4v")
            output_file = os.path.join(self.output_folder, "recorded_video.mp4")
            height, width = 854, 480  # Adjust as needed
            self.video_writer = cv2.VideoWriter(output_file, codec, 30, (width, height))
            self.is_recording = True
            st.write("Recording started...")


    def stop_and_save_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.video_writer:
                self.video_writer.release()
                st.success(f"Video saved in {self.output_folder}/recorded_video.mp4")
                st.write("Recording stopped and video saved.")

def main():
    st.title("Real-Time Face Emotion Detection")

    output_folder = st.text_input("Enter the folder path to save the video")
    recorder = FaceEmotion(output_folder)

    webrtc_ctx = webrtc_streamer(
        key="face-emotion",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_processor_factory=lambda: recorder
    )

    if webrtc_ctx.video_processor and webrtc_ctx.state.playing:
        if st.button("Start Recording"):
            recorder.start_recording()

        if st.button("Stop Recording"):
            recorder.stop_and_save_recording()

if __name__ == "__main__":
    main()
