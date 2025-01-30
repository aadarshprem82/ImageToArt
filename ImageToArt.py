import os
import io
import base64
import tempfile
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


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

def GetIMGBase64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    imgStr = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return imgStr

def main():
    st.title("Image to Art🎨!!")

    if "canReset" not in st.session_state:
        st.session_state.canReset = False
    # print("Start: ",st.session_state)

    file = st.file_uploader("Upload an Image: ", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)

    if st.button("Create Art!",icon="🎨", use_container_width=True):
        st.session_state.canReset = True
        # st.image("image.png", "Just an Image")

    if file and st.session_state.canReset:
        try:
            imageToShow, imageToDownload = GetArtImage(file)
            imageBase64 = GetIMGBase64(imageToShow)
            # imageComponent = st.image(imageToShow, "Generated Art Image", use_container_width=True)
            st.markdown(
                f"""
                <style>
                @keyframes zoom-in-out{{
                    0% {{
                        transform: scale(0.9);
                    }}
                    50% {{
                        transform: scale(0.2);
                    }}
                    100% {{
                        transform: scale(0.9);
                    }}
                }}
                .zoom-image {{
                    animation: zoom-in-out 5s 3 ease-in-out;
                    transform: scale(0.9);
                    width: 100%;
                    height: auto;
                }}
                </style>
                <img id="zoom-image" src="data:image/png;base64,{imageBase64}" class="zoom-image"/>
                """, 
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([1,1], vertical_alignment="center")
            with col1:
                st.download_button("Download Art Image", imageToDownload, "artImage.jpg", "image/jpeg", icon="⏬")
            with col2:
                # zoomLevel = st.slider("Zoom In and Out", 0.1, 1.0, 1.0, step=0.1)
                # print(zoomLevel)
                # st.markdown(
                #     f"""
                #     <script>
                #     const image = document.getElementById('zoom-image');
                #     image.style.transform = 'scale({zoomLevel})';
                #     </script>
                #     """,
                #     unsafe_allow_html=True
                # )
                st.info("Zoom in and out is just for show-off. You can still downlod the image as a normal file.")
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
