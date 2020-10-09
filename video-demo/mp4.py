# Import everything needed to edit video clips
from moviepy.editor import *

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip("1.mp4").subclip(30,60)

video = CompositeVideoClip([clip])

# Write the result to a file (many options available !)
video.write_videofile("2.mp4")