# Import everything needed to edit video clips
import sys

from moviepy.editor import *

# loading video dsa gfg intro video
clip = VideoFileClip(sys.argv[1])
clip.write_videofile("movie2.mp4", fps=int(sys.argv[2]))
