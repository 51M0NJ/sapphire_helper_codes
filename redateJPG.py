# make sure your input filenames are time sortable, whatever their format is, and end with '.jpg' 
# example: scanner1-MM-DD-####.jpg
# please, someone from the future; 
# there is better ways to handle dates (with module datetime)
# also you need to implement the MONTH increment if you need 
### Followings comments are GPT-generated

import piexif, os
from PIL import Image

# The script updates EXIF timestamps in .jpg images sequentially,
# assigning each image a timestamp 30 minutes later than the previous one.
# It also renames the images with zero-padded indices (e.g., 0001.jpg).

def increment30mins(datestring):
    """
    Adds 30 minutes to a timestamp string in the format 'YYYY:MM:DD HH:MM:SS'.
    NOTE:
      - Does not handle month/year rollovers properly.
      - Designed for simple sequential increments (e.g., simulated timeline).
    """
    date, time = datestring.split(' ')
    h, m, s = time.split(':')
    Y, M, D = date.split(':')
    # Increment minutes by 30
    m = str(int(m) + 30).zfill(2)
    # If minutes overflow to 60, increase hour by 1
    if m == '60':
        h = str(int(h) + 1).zfill(2)
        m = '00'
    # If hours overflow to 24, reset to 00 and increment day by 1
    if h == '24':
        h = '00'
        D = str(int(D) + 1).zfill(2)
    return f'{Y}:{M}:{D} {h}:{m}:{s}'

# Get all .jpg files in the current directory
# Assumes filenames are sortable in chronological order
imageslist = [f for f in os.listdir(".") if f.endswith(".jpg")]
imageslist.sort()
# Starting timestamp (arbitrary)
current_time = f'2025:01:01 00:00:00'
# Loop through all images
for idx, img in enumerate(imageslist):
    # Open the image
    img = Image.open(img)
    # Load existing EXIF data
    exif_dict = piexif.load(img.info.get('exif', b""))
    # Update the "DateTimeDigitized" EXIF tag
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = current_time.encode()
    # Convert modified EXIF data back to bytes
    exif_bytes = piexif.dump(exif_dict)
    # Save the image with new name and updated EXIF timestamp
    img.save(f"{str(idx+1).zfill(4)}.jpg", exif=exif_bytes)
    # Increment timestamp by 30 minutes for next image
    current_time = increment30mins(current_time)
