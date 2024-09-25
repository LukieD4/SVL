# SVL
Seamless Video Looper    

A puddle of python scripts used to query the user with a set basis of parameters to curate a Seamless Video.

A relatively short CLI project that may recieve updates periodically.
This project was designed for fun and ease to trim short form content used for GIF repetition / loops.

> I hope this documentation helps shed light on the on-going progress. Not all ideas will be implemented  
> and may only come in further updates.

-----------------------------------------------  
# Future Features -> v1.5+  
- Shift the main reference frame with an offset. *potentially not to be implemented*.
- Option to 'bounce' media
- Option to speed up media
- Threaded frame dissection
- Improve documentation

## Known Issues ##  
- Encoders throw errors, usually because of files missing or they were in the wrong use case. Using first initial prompt should work 100% of the time
-----------------------------------------------  
# Changelog 25D/09M/24Y -> v1.4  
- Proper media encoding for formats other than MP4.  
- GIF exporting.
- Accurate texts for start and end offset input requirements.
- Improve documentation
- Hopefully clearer use instructions via program

## Fixed Issues ##  
- Selecting a video outside current working directory crashes the program.  
- USER-CLI inputs are not sanitised, resulting in creating possible erroneous values (i.e: start offset + end offset)  
- Display shows 1 error, usually the last frame of media. It's okay but maybe we should fix the video duration variable.  
- Selecting GIF as an export format is no longer available. Awaiting reimplementation.  
- Selecting VIDEO and choosing an export does not cater for the correct encoder, resulting in a possible crash and media not exporting.  
- Dissected frames could be recycled instead of deleted if the user wants to fine tune the same selected media.  
- Duration floating point should follow the DecimalPlace variable.  
- "SVL (v1.3)" via the program should be updated to match current SVL version to avoid confusion.  
- CLI interface should clear the command-line when printing frame export messages.
- Program doesn't cater for a full loop, it should remove last frame at end_offset
-----------------------------------------------  