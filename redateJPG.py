import piexif, os
from PIL import Image

# make sure your input filenames are time sortable, whatever their format is, and end with '.jpg' 
# example: scanner1-MM-DD-####.jpg
# please, someone from the future; 
# there is better ways to handle dates (with module datetime)
# also you need to implement the MONTH increment if you need 
def increment30mins(datestring): 
    date,time = datestring.split(' ')
    h,m,s = time.split(':')
    Y,M,D = date.split(':')
    m=str(int(m)+30).zfill(2)
    if m=='60': 
        h=str(int(h)+1).zfill(2)
        m='00'
    if h=='24':
        h='00'
        D=str(int(D)+1).zfill(2)
    return f'{Y}:{M}:{D} {h}:{m}:{s}'

imageslist = [f for f in os.listdir(".") if f.endswith(".jpg")]
imageslist.sort()
current_time = f'2025:01:01 00:00:00'
for idx, img in enumerate(imageslist):
    img = Image.open(img)
    exif_dict = piexif.load(img.info.get('exif', b""))
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = current_time.encode()
    exif_bytes = piexif.dump(exif_dict)
    img.save(f"new_{str(idx+1).zfill(4)}.jpg", exif=exif_bytes)
    current_time=increment30mins(current_time)
