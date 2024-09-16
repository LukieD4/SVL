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
        
       
What does the batch file install?   
-python libraries including...
> numpy   
> pillow (PIL)   
> scikit-image (+skimage)   
> opencv-python (cv2)   

References to all dependencies (do not install, if you're on Windows then you're all good):  
> tkinter   (pre-installed w/ Python on Windows)   
> os        (possibly varied outcome)   
> re        (pre-installed w/ Python)   
> math      (pre-installed w/ Python)   
> time      (pre-installed w/ Python)   
-----------------------------------------------    
# Usage Guide    
Upon using the program, a CLI window will appear and this will be all there is to it.    
## To begin,
   [1] a file dialogue window will appear   
   > Find a suitable video file, and import it via the tkinter window  
## Start offset,  
   [2] in the CLI, input a start time for where you want to start frame scanning.  
   > This will be the frame that will be used as a reference to DETERMINE the best suitable frame.
## End offset,  
   [3] next, input an end time for where you want the frame scanning to stop.   
   > This doesn't mean the end frame you choose is the last frame of the to-be-exported video!!   
## Frame export format,   
   [4] from a select range, choose how you would like to export each frame.   
   > This will impact video quality and file size. Preferably I pick PNG.   
## Ignore frames,  
   [5] a buffer zone; insert a number to skip early decisions made by the program. Perferably I use 30.  
   > this is to prevent the best frame from being chosen too early, resulting in an extremely short duration of video.
#  
#  
## Processing data,  
   [i] TBD  
