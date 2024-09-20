import cv2
import os

def create_video_from_images(image_paths, video_path, frame_rate):
    """
    Create a video from a series of images.

    Parameters:
    - image_paths: List of file paths to images.
    - video_path: Path where the video will be saved.
    - frame_rate: Frame rate of the video in frames per second (fps).
    """
    if not image_paths:
        print("No images to create video")
        return
    
    # Read the first image to get the frame size
    first_image = cv2.imread(image_paths[0])
    if first_image is None:
        print(f"Error loading image from {image_paths[0]}")
        return
    
    height, width, layers = first_image.shape
    video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))
    
    for image_path in image_paths:
        img = cv2.imread(image_path)
        if img is not None:
            # Resize image to match the frame size, if necessary
            img_resized = cv2.resize(img, (width, height))
            video_writer.write(img_resized)
        else:
            print(f"Error loading image from {image_path}")

    
    # Complete video writing
    video_writer.release()

    # Return the newly made video
    return video_path