import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk


# Function to play MP4 video in a loop inside the Tkinter window
def play_video_loop(video_path, label):
    # Open the video file using OpenCV
    cap = cv2.VideoCapture(video_path)

    def update_frame():
        # Read the next frame from the video
        ret, frame = cap.read()

        if ret:
            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a PIL image and then to a Tkinter-compatible format
            img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

            # Update the label with the new image
            label.config(image=img)
            label.image = img
        else:
            # Restart the video once it's done playing
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Call this function again after a short delay to keep updating the frame
        label.after(10, update_frame)  # Adjust the delay (in milliseconds) as needed

    update_frame()  # Start the video playback

# Initialize the Tkinter window
root = tk.Tk()
root.title("MP4 Video Loop in Tkinter")

# Set the window size
root.geometry("640x480")

# Create a label widget to display the video frames
video_label = Label(root)
video_label.pack()

# Start playing the video in a loop
play_video_loop(fr"converted\plappy-trim.mp4", video_label)

# Start the Tkinter main loop
root.mainloop()




# Made with ChatGPT, I got too lazy.