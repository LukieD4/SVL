import cv2
import os
import re
import time
import math
import shutil
from tkinter import filedialog as FileDialogue
from numpy import ndarray as nda # Used for type detecting
from PIL import Image as Image

##
# Settings
DEBUG_MODE                  = False
CLI_FLOAT_DPs               = 3
CLOSE_WHEN_FINISHED         = False
RMDIR_WHEN_FINISHED         = True

# Streamline Settings, set to None for defaults
DEFAULT_MEDIA_FILE              = None #"wave.webm"
DEFAULT_STARTOFFSET             = None #2.5
DEFAULT_ENDOFFSET               = None #3
DEFAULT_FRAME_QUALITY_FORMAT    = None #"PNG"
DEFAULT_FRAME_IGNORE_AMOUNT     = None #11
DEFAULT_QUERY_FILEFORMAT        = None #"VIDEO"
DEFAULT_QUERY_FILETYPE          = None #"mp4"

# Careful! There's an issue that I can't find a workaround,
# -The output file will spawn inside the current working directory, *THEN* move to 'converted'
# -changing the suffix to "" could result in your original file getting OVERWRITTEN!
OUTPUT_SUFFIX = "-trim"



# Dev-tracking (Don't change please)
Version = "v1.3"






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


if DEFAULT_MEDIA_FILE == None:
    SelectedVideo = FileDialogue.askopenfile(defaultextension=".*",filetypes=supported_file_types,initialdir=os.getcwd())
    SelectedVideo = SelectedVideo.name
else:
    SelectedVideo = os.path.abspath(DEFAULT_MEDIA_FILE)



VideoName, VideoPath = os.path.basename(SelectedVideo), os.path.normpath(SelectedVideo)
VideoNameWithoutExtension, VideoExtension = os.path.splitext(VideoName)[0], os.path.splitext(VideoName)[1] # Output: .mp4 (Don't worry, it outputs the '.')
SelectedVideo = cv2.VideoCapture( VideoName )









##
# Global variables
frames_per_second, frames_of_media, duration_of_media, start_offset, start_frame, end_offset, end_frame, quality_format, best_frame, error_frames,  = None,None,None,None,None,None,None,None,None,0
video_path = VideoName





def ReferDirectory(path:os.path,dirname:str):
    # Create the full path for the directory
    full_path = os.path.join(path, dirname)
    
    # Check if the directory exists
    if os.path.isdir(full_path):
        return full_path
    else:
        # If it doesn't exist, create the directory
        os.mkdir(full_path)
        return full_path
    



current_time = time.localtime()
formatted_time = time.strftime("%H%M%p/%d/%m/%Y", current_time).replace('/', '')
def DisplayMessage(message:str):
    # Whilst debugmode is true, write all messages to txt.
    if DEBUG_MODE == True:
        with open(fr"debug_{formatted_time}.txt","a+") as dbgfile:
            dbgfile.write(f"{message} ::: {formatted_time}")
    
    # Output the message onto CLI
    print(message)
            



def OutputCurrentData():
    # Clear CLI interface
    os.system("cls")

    # Output the metadata and media data to the user
    CurrentData = f"SVL ({Version}) Seamless Video Looper\nCurrent Data:\n Path:{VideoPath}\n Media:{VideoName}\n  FPS:{frames_per_second}\n   Total:{frames_of_media}\n   Duration:{duration_of_media}\n  Soffset:{start_offset}\n   SoF:{start_frame}\n  Eoffset:{end_offset}\n   EoF:{end_frame}\n  Foutput:{quality_format}\n   MFrame:{start_frame}\n   BFrame:{best_frame}\n   Errors:{error_frames}\n"
    
    # If DEBUG enabled
    if DEBUG_MODE == True:
        CurrentData = f"{CurrentData}\n**DEBUG MODE ENABLED**"

    # Display CurrentData to the CLI
    DisplayMessage(CurrentData)
    return CurrentData



def AskForValue(message: str, datatype: type):
    # Print the media data to the user (this can also returns the current data string)
    OutputCurrentData()

    # To prevent a bug with it already being declared once the user inputs an invalid response.
    global GetInputValue
    GetInputValue = None

    # Using try catch to avoid fatal erroring.
    # - If the datatype doesn't match, kill the process with an undeclared function
    try:

        # Ask the user to respond to the scenario
        GetInputValue = datatype(input(message))

        # Display message? Should it though?
        if DEBUG_MODE == True:
            DisplayMessage(f"{GetInputValue},{type(GetInputValue)}")
        if datatype != type(GetInputValue):
           die() # type: ignore
    except:
        # Alerts the user as their response is invalid 
        DisplayMessage("\nInvalid response\n")
        time.sleep(.5)

        # Re-run the function so the user can try again.
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


def ReferOrAsk(ReferenceVariable, FunctionToRun):
    if ReferenceVariable == None:
        return FunctionToRun()
    else:
        return ReferenceVariable
    
    

## 
# Metadata variables
media_round_dp = 10**CLI_FLOAT_DPs
frames_per_second = SelectedVideo.get(cv2.CAP_PROP_FPS)
frames_of_media   = SelectedVideo.get(cv2.CAP_PROP_FRAME_COUNT)
frame_millisecond = float(f"{(1/frames_per_second):.6f}")
duration_of_media = frames_of_media / frames_per_second
#
start_offset = ReferOrAsk(DEFAULT_STARTOFFSET,lambda:AskForValue("Start offset in seconds (type '0' or higher) ",float))
end_offset = ReferOrAsk(DEFAULT_ENDOFFSET,lambda:AskForValue(f"End offset in seconds (type '{math.ceil(duration_of_media % 60 * media_round_dp) / media_round_dp}' or lower) ",float))
#
start_frame  = int(start_offset * frames_per_second)
end_frame    = int(end_offset * frames_per_second)
starting_frame = SelectedVideo.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
# Quality Format
quality_whitelist = ["GIF","JPG","JPEG","WEBP","JP2","PNG","TIFF","EXR","HDR","PPM","PGM","PBM"]
quality_format = ReferOrAsk(DEFAULT_FRAME_QUALITY_FORMAT,lambda:AskForValueFromList(quality_format,quality_whitelist,"\nSelect:\n Low quality, but fast:\n  [1] GIF\n  [2] JPG\n  [3] JPEG\n  [4] WEBP\n Normal quality, runs fine:\n  [5] JP2\n  [6] PNG\n  [7] TIFF\n High quality, but slow:\n  [8] EXR\n  [9] HDR\n  [10] PPM\n  [11] PGM\n  [12] PBM\n",int)) # Time wasted solving 5 doesn't come after 3: 1+1/2hrs 


OutputCurrentData()







##
# Process video
from skimage.metrics import structural_similarity as ssim



# Variables for globals
FileIsValid, ExtractedImage = SelectedVideo.read()
indexFrame = starting_frame+0
indexFrame_Original = indexFrame
end_frame = end_frame-start_frame
iterationFrame = 0
main_reference_grayscale = None
#
best_frame = None
global best_frame_score
best_frame_score = -1
frame_ignore_amount = ReferOrAsk(DEFAULT_FRAME_IGNORE_AMOUNT,lambda:AskForValue(f"\nHow many frames should be ignored, before assigning a score rating.\n  This to make sure that the script doesn't assume the best frame is\n   barely when the video began, resulting in probably 1 nano-second of video time\n\n Tip: Pinpoint half-way in between an action in the video.\n  (type lower than '{end_frame}')",int))


# Creates a folder if one doesn't already exist. References to the path
processing_folder = ReferDirectory(os.getcwd(),"processing")
converted_folder = ReferDirectory(os.getcwd(),"converted")




while indexFrame <= end_frame:
    iterationFrame += 1

    # Runs only once
    # (Grabs the first frame in 'processing', we select '2' so it doesn't crash when an image isn't created)
    if iterationFrame == 2:
        main_reference_grayscale = cv2.imread(os.path.abspath( fr"{processing_folder}\frame{indexFrame-1}.{quality_format}" ), cv2.IMREAD_GRAYSCALE)
    

    # Update the video frame to allow new frames to be processed
    FileIsValid, ExtractedImage = SelectedVideo.read()

    # Saves into the processing directory under the name of the frame
    frame_file_path = os.path.join(processing_folder, fr"frame%d.{quality_format}" % int(indexFrame + 0))
    try:
        cv2.imwrite(frame_file_path, ExtractedImage)

        # Compare numbers to see if it can find a better frame
        if isinstance(main_reference_grayscale, nda):
            score, diff = ssim(main_reference_grayscale, cv2.imread(frame_file_path, cv2.IMREAD_GRAYSCALE), full=True)
            if frame_ignore_amount < indexFrame and best_frame_score < score:
                best_frame_score = score
                best_frame = indexFrame
            #print(score, diff)


    except:
        error_frames += 1

    DisplayMessage(f"{OutputCurrentData()}\nProcessing: {iterationFrame}/{end_frame}\nBest frame: {best_frame} | {best_frame_score}")
    if DEBUG_MODE == True:
        DisplayMessage(f"DEBUG:\nstartframe:{start_frame}, offset{start_offset}\nindexframe:{indexFrame}\niterationframe:{iterationFrame}\nframefilepath:{frame_file_path}\n\n")
    
    indexFrame += 1 # Forward onto next frame  







# Gets the current directory for processing to seek the frame contents
files = sorted(os.listdir(processing_folder))
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
    







# Ask user for which file format they want their video converted to
global New_Media
QueryFileFormatToUser, QueryFileType = None,None
QueryFileFormatToUser = ReferOrAsk(DEFAULT_QUERY_FILEFORMAT,lambda:AskForValueFromList(QueryFileFormatToUser,["VIDEO","GIF"],"\nSelect a desired output:\n [1] VIDEO\n [2] GIF\n",int))

if f"{2}" in QueryFileFormatToUser:
    from CreateGIF import create_gif_from_images as CreateGIF
    QueryFileType = ReferOrAsk(DEFAULT_QUERY_FILETYPE,lambda:AskForValueFromList(QueryFileType,["gif","webp"],"\nSelect animated export format:\n [1] GIF\n [2] WEBP",int))
    New_Media = CreateGIF(files_to_collate,f"{VideoNameWithoutExtension}{OUTPUT_SUFFIX}.{QueryFileType}", duration=frame_millisecond*100)#frame_millisecond)

else:
    from CreateVID import create_video_from_images as CreateVideo
    ValidFileTypes = ["mp4","webm","avi","mov","mkv","wmv","flv","mpg","mpeg","3gp","mts","m2ts","ogv","rm","divx","mxf"]
    QueryFileType = ReferOrAsk(DEFAULT_QUERY_FILETYPE,lambda:AskForValueFromList(QueryFileType,ValidFileTypes,"\nSelect video export format:\n Common filetypes:\n  [1] MP4\n  [2] WEBM\n  [3] AVI\n  [4] MOV\n  [5] MKV\n  [6] WMV\n  [7] FLV\n  [8] MPG\n  [9] MPEG\n Misc filetypes:\n  [10] 3GP\n  [11] MTS\n  [12] M2TS\n  [13] OGV\n  [14] RM\n  [15] DIVX\n  [16] MXF\n",int))
    New_Media = CreateVideo(files_to_collate, f"{VideoNameWithoutExtension}{OUTPUT_SUFFIX}.{QueryFileType}", frame_rate=frames_per_second)


# Move final product to the converted folder.
# avoided doing it via cv2 since it throws an error.
New_Media = os.path.abspath(New_Media)
Expected_Media = os.path.join(converted_folder, os.path.basename(New_Media))

# Remove the existing file if it exists
if os.path.exists(Expected_Media):
    os.remove(Expected_Media)

# Clean up Processing folder
if RMDIR_WHEN_FINISHED == True:
    shutil.rmtree(processing_folder,ignore_errors=True)


# Post-finishing remedies
DisplayMessage(f"{OutputCurrentData()}\n** NEW MEDIA COMPLETE **")
shutil.move(New_Media, Expected_Media)
# Asks the user via visual confirmation before closing
if CLOSE_WHEN_FINISHED == False:
    input("\nPress any key to close..\n")
exit()