import cv2
from PIL import Image as Image

def create_gif_from_images(image_paths, gif_path, duration):
    """
    Create a GIF from a series of images.

    Parameters:
    - image_paths: List of file paths to images.
    - gif_path: Path where the GIF will be saved.
    - duration: Duration of each frame in milliseconds.
    """
    print("Compiling and assembling gif (this may take a while)")

    images = []

    # Load images using OpenCV and convert to Pillow Image format
    for image_path in image_paths:
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is not None:
            # Convert BGR (OpenCV) to RGB (Pillow)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Convert numpy array to PIL Image
            pil_img = Image.fromarray(img_rgb)
            images.append(pil_img)
        else:
            print(f"Error loading image from {image_path}")

    # Save images as GIF using Pillow
    if images:
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0  # 0 means infinite loop
        )
        return gif_path
    else:
        print("No images to create GIF")
        