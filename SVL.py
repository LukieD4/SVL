import cv2
import os
import re
from tkinter import filedialog as FileDialogue
from numpy import ndarray as nda # Used for type detecting
from PIL import Image as Image

##
# Ask user which file they want to select
supported_file_types = filetypes = [
        ('All Files', '*.*'),
        ('GIF Files', '*.gif'),
        ('AVI Files', '*.avi'),
        ('MP4 Files', '*.mp4'),
        ('MOV Files', '*.mov'),
        ('MKV Files', '*.mkv'),
        ('FLV Files', '*.flv'),
        ('WMV Files', '*.wmv'),
        ('WEBM Files', '*.webm')
    ]

SelectedVideo = FileDialogue.askopenfile(defaultextension=".*",filetypes=supported_file_types,initialdir=os.getcwd())
VideoName, VideoPath = os.path.basename(SelectedVideo.name), os.path.normpath(SelectedVideo.name)
VideoNameWithoutExtension, VideoExtension = os.path.splitext(VideoName)[0], os.path.splitext(VideoName)[1] # Output: .mp4 (Don't worry, it outputs the '.')
SelectedVideo = cv2.VideoCapture( SelectedVideo.name )




##
# Global variables
frames_per_second, frames_of_media, start_offset, start_frame, end_offset, end_frame, quality_format = None,None,None,None,None,None,None
video_path = VideoName







def OutputCurrentData():
    os.system("cls")
    print(f"Current Data:\n Path:{VideoPath}\n Media:{VideoName}\n  FPS:{frames_per_second}\n   Total:{frames_of_media}\n  Soffset:{start_offset}\n   SoF:{start_frame}\n  Eoffset:{end_offset}\n   EoF:{end_frame}\n  Foutput:{quality_format}")


def AskForValue(message: str, datatype: type):
    OutputCurrentData()
    try:
        GetInputValue = datatype(input(message))
        print(GetInputValue,type(GetInputValue))
        if datatype != type(GetInputValue):
           die() # type: ignore
    except:
        print("Invalid\n")
        AskForValue(message,datatype)
    
    return GetInputValue


def AskForValueFromList(returnVariable, referenceList, message: str, datatype: type):
    returnVariable = None
    while returnVariable == None:
        returnVariable = AskForValue(message,datatype)-1 #Minus 1 to fit within python lists, heh this aint Lua, Lukie!
        if 0 <= returnVariable < len(referenceList)+1:
            # Passed checks, is valid
            returnVariable = referenceList[returnVariable]#referenceList[returnVariable-2]
        else:
            # Failed checks, invalid
            os.system("cls")
            returnVariable = None
    return returnVariable


## 
# Metadata variables
import math
media_round_dp = 1000
frames_per_second = SelectedVideo.get(cv2.CAP_PROP_FPS)
frames_of_media   = SelectedVideo.get(cv2.CAP_PROP_FRAME_COUNT)
frame_millisecond = float(f"{(1/frames_per_second):.6f}")
duration_of_media = frames_of_media / frames_per_second
start_offset    = AskForValue("Start offset in seconds (type '0') ",float)
start_frame      = int(start_offset * frames_per_second)
end_offset      = AskForValue(f"End offset in seconds (type '{math.ceil(duration_of_media % 60 * media_round_dp) / media_round_dp}' or lower) ",float)
end_frame        = int(end_offset * frames_per_second)
starting_frame = SelectedVideo.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
# Quality format
quality_whitelist = ["GIF","JPG","JPEG","WEBP","JP2","PNG","TIFF","EXR","HDR","PPM","PGM","PBM"]
quality_format = AskForValueFromList(quality_format,quality_whitelist,"\nSelect:\n Low quality, but fast:\n  [1] GIF\n  [2] JPG\n  [3] JPEG\n  [4] WEBP\n Normal quality, runs fine:\n  [5] JP2\n  [6] PNG\n  [7] TIFF\n High quality, but slow:\n  [8] EXR\n  [9] HDR\n  [10] PPM\n  [11] PGM\n  [12] PBM\n",int) # Time wasted solving 5 doesn't come after 3: 1+1/2hrs 




#time.sleep(5)
OutputCurrentData()







##
# Process video
from skimage.metrics import structural_similarity as ssim
import time


# Variables for globals
FileIsValid, ExtractedImage = SelectedVideo.read()
indexFrame = starting_frame
indexFrame_Original = indexFrame
iterationFrame = 0
main_reference_grayscale = None
#
global best_frame
global best_frame_score
best_frame = None
best_frame_score = -1
frame_ignore_amount = AskForValue(f"\nHow many frames should be ignored, before assigning a score rating.\n  This to make sure that the script doesn't assume the best frame is\n   barely when the video began, resulting in probably 1 nano-second of video time\n\n Tip: Pinpoint half-way in between an action in the video.\n  (type lower than '{end_frame}')",int)


# Creates a folder if one doesn't already exist. References to the path
processing_folder = fr"{os.getcwd()}\processing"
converted_folder = fr"{os.getcwd()}\converted"




while FileIsValid and indexFrame <= end_frame:
    #print(indexFrame+0)
    iterationFrame += 1

    # Runs only once
    # (Grabs the first frame in 'processing', we select '2' so it doesn't crash when an image isn't created)
    if iterationFrame == 2:
        main_reference_grayscale = cv2.imread(os.path.abspath( fr"{processing_folder}\frame{iterationFrame-1}.{quality_format}" ), cv2.IMREAD_GRAYSCALE)
    

    # Update the video frame to allow new frames to be processed
    FileIsValid, ExtractedImage = SelectedVideo.read()

    # Saves into the processing directory under the name of the frame
    frame_file_path = os.path.join(processing_folder, fr"frame%d.{quality_format}" % int(indexFrame + 0))
    cv2.imwrite(frame_file_path, ExtractedImage)

    # Compare numbers to see if it can find a better frame
    #print(f"thing: {main_reference_grayscale}")
    #print(f"type {type(main_reference_grayscale)}")
    if isinstance(main_reference_grayscale, nda):
        score, diff = ssim(main_reference_grayscale, cv2.imread(frame_file_path, cv2.IMREAD_GRAYSCALE), full=True)
        if frame_ignore_amount < indexFrame and best_frame_score < score:
            best_frame_score = score
            best_frame = indexFrame
        #print(score, diff)

    OutputCurrentData()
    print(f"Processing: {iterationFrame}/{end_frame}\nBest frame: {best_frame} | {best_frame_score}")
    indexFrame += 1 # Forward onto next frame
    
    #time.sleep(1)  







# Gets the current directory for processing to seek the frame contents
files = sorted(os.listdir("processing"))
files_to_collate = []  # Initialize an empty list
#filler_durations = []
file_index = -1


# Function to extract numbers from file names for sorting
# Fixes stupid issues where files will be gathered like: image1, image11, image12, image2, image20
def extract_number(file_name):
    match = re.search(r'\d+', file_name)
    return int(match.group()) if match else float('inf')

# Sort files based on the extracted number
files.sort(key=extract_number)

# Gathers the files, to ready to send to gif maker
for file in files:
    file_index += 1
    if file_index <= end_frame:
        files_to_collate.append(os.path.abspath(os.path.join("processing", file)))
        #filler_durations.append(10)
        #print(files_to_collate[file_index])
    







# Ask user for which file format they want their video converted to
QueryFileFormatToUser, QueryFileType = None,None
QueryFileFormatToUser = AskForValueFromList(QueryFileFormatToUser,["VIDEO","GIF"],"\nSelect a desired output:\n [1] VIDEO\n [2] GIF\n",int)
if f"{2}" in QueryFileFormatToUser:
    from CreateGIF import create_gif_from_images as CreateGIF
    QueryFileType = AskForValueFromList(QueryFileType,["gif","webp"],"\nSelect animated export format:\n [1] GIF\n [2] WEBP",int)
    GIF = CreateGIF(files_to_collate,f"{VideoNameWithoutExtension}-trim.{QueryFileType}", duration=frame_millisecond*100)#frame_millisecond)

else:
    from CreateVID import create_video_from_images as CreateVideo
    ValidFileTypes = ["mp4","webm","avi","mov","mkv","wmv","flv","mpg","mpeg","3gp","mts","m2ts","ogv","rm","divx","mxf"]
    QueryFileType = AskForValueFromList(QueryFileType,ValidFileTypes,"\nSelect video export format:\n Common filetypes:\n  [1] MP4\n  [2] WEBM\n  [3] AVI\n  [4] MOV\n  [5] MKV\n  [6] WMV\n  [7] FLV\n  [8] MPG\n  [9] MPEG\n Misc filetypes:\n  [10] 3GP\n  [11] MTS\n  [12] M2TS\n  [13] OGV\n  [14] RM\n  [15] DIVX\n  [16] MXF\n",int)
    print(QueryFileType,type(QueryFileType))
    CreateVideo(files_to_collate, f"{VideoNameWithoutExtension}-trim.{QueryFileType}", frame_rate=frames_per_second)





exit()