# SVL
Seamless Video Looper    

A puddle of python scripts used to query the user with a set basis of parameters to curate a Seamless Video.

A relatively short CLI project that may recieve updates periodically.
This project was designed for fun and ease to trim short form content used for GIF repetition / loops.

Sample video was found at random and taken from:
https://www.furaffinity.net/view/52184319/
(I do not own this video, nor is it condemned under the liscense for this project)  

# Supported platforms  
> Windows ✅  
> Linux ❓  
> MacOS ❓
   
Will there be support outside of windows? Ideally no,
  everything that may be supported is merely coincidental,
    but I'll be glad if it does magically work on other platforms. 

-----------------------------------------------   
# Installation  
  
>[1] Run the batch file ('pre-req') provided to fulfill all pre-requirements.  
>-?>[1a] If it fails to work, try installing Python: https://www.python.org/downloads/    
>-?>[1b] Run the installer (tested with 3.12.6) + make sure to tick ['ADD to PATH'](https://miro.medium.com/v2/resize:fit:1344/0*7nOyowsPsGI19pZT.png)  
>[2] Run 'SVL.py'  
>[3] Give yourself a pat on the back and proceed to Usage Guide below.    
        
-----------------------------------------------    
# Usage Guide    
Upon using the program, a CLI window will appear and this will be all there is to it.    
### Media Insertion Window
   > Find a suitable video file, and import it via the tkinter window  
### Start Offset  
   > Input a start time for where you want to begin scanning frames of your chosen media.  
   > ( This is **the main reference frame that determines** the **similarity** rating **of all the other frames** )
### End Offset  
   > Input an end time for where you want the frame scanning to stop.   
   > ( This **doesn't mean** the **end frame** you choose **is the last frame of the to-be-exported video**!!   
### Frame Export Format   
   > Choose how you would like to export each individual frames ( this is the stage before compiling a new video )   
   > ( This **impacts** **video quality** and **file size**. *Preferably I pick PNG*.   
### Ignore Frames
   > A buffer zone. Insert a number to skip early decisions made by the program.  
   > ( This is **to prevent** the **best frame** from **being chosen too early** with a bias frame score, **resulting** in an **extremely short video** )
### Desired Output and Media Export Format  
   > Pick how you would like the finale piece to format as.
-----------------------------------------------
# Current Data Descriptions  
**Path**: *Filepath directing to where your selected media is located*  
**Media**: *Name of your selected media, with file extension attached*  
 **FPS**: *Frames per second of the selected media*  
  **Total**: *Total number of frames in the selected media*  
  **Duration**: *How long the media lasts*  
 **Soffset**: *A float for the media start offset*  
  **SoF**: *Start of frame*  
 **Eoffset**: *A float for the media end offset*  
  **EoF**: *End of frame*  
 **Foutput**: *Frame output choice*   
  **MFrame**: *Main (reference) frame*  
  **BFrame**: *Best frame*  
  **Errors**: *Number of media compile errors*  
> Errors usually occur if the end-offset was too high, resulting in the program reading **past** the bounds of the video, resulting in reading null data. Or in worse case scenario, your media wasn't encoded properly and is or corrupted.
