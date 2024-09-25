import cv2
import os

def create_video_from_images(image_paths, video_path, frame_rate, encoder):
    """
    Create a video from a series of images.

    Parameters:
    - image_paths: List of file paths to images.
    - video_path: Path where the video will be saved.
    - frame_rate: Frame rate of the video in frames per second (fps).
    """
    print("Compiling and assembling video (this may take a while)")

    if not image_paths:
        print("No images to create video")
        return
    
    # Read the first image to get the frame size
    first_image = cv2.imread(image_paths[0])
    if first_image is None:
        print(f"Error loading image from {image_paths[0]}")
        return
    
    height, width, layers = first_image.shape
    video_writer = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*encoder), frame_rate, (width, height))
    
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



def correspond_encoders(FileFormat):
    Encoders = []
    match FileFormat:
        case "mp4":
            # Common codec for MP4 is 'mp4v' or 'avc1' (H.264)
            Encoders = ["mp4v", "avc1", "h264"]
            
        case "webm":
            # Common codec for WEBM is VP8 or VP9
            Encoders = ["VP80", "VP90"]  # VP8 and VP9

        case "avi":
            # Common codec for AVI is XVID, DIVX, or MJPG (Motion JPEG)
            Encoders = ["XVID", "DIVX", "MJPG"]

        case "mov":
            # MOV can use 'mp4v', 'avc1', or 'MJPG'
            Encoders = ["mp4v", "avc1", "MJPG"]

        case "mkv":
            # MKV supports VP8, VP9, and H.264
            Encoders = ["VP80", "VP90", "X264"]  # VP8, VP9, H.264

        case "wmv":
            # WMV format uses its own codec 'WMV1', 'WMV2', or 'WMV3'
            Encoders = ["WMV1", "WMV2", "WMV3"]

        case "flv":
            # FLV typically uses 'FLV1' or 'H264'
            Encoders = ["FLV1", "H264"]

        case "mpg":
            # MPEG-1 and MPEG-2 codecs for MPG
            Encoders = ["MPEG", "MP2V"]

        case "mpeg":
            # Same as MPG, supports 'MPEG' or 'MP2V'
            Encoders = ["MPEG", "MP2V"]

        case "3gp":
            # 3GP format uses 'H263', 'H264', or 'MP4V'
            Encoders = ["H263", "H264", "mp4v"]

        case "mts":
            # MTS format (AVCHD) uses 'H264' or 'MPEG'
            Encoders = ["H264", "MPEG"]

        case "m2ts":
            # M2TS (Blu-ray container) uses 'H264' or 'MPEG'
            Encoders = ["H264", "MPEG"]

        case "ogv":
            # OGV uses Theora ('THEO') and sometimes VP8 ('VP80')
            Encoders = ["THEO", "VP80"]

        case "rm":
            # RealMedia uses 'RV10' or 'RV20' codecs
            Encoders = ["RV10", "RV20"]

        case "divx":
            # DivX codec (DIVX)
            Encoders = ["DIVX"]

        case "mxf":
            # MXF can use a variety of codecs, such as 'MPEG' or 'H264'
            Encoders = ["MPEG", "H264"]

    return Encoders