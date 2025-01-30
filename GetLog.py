import smtplib
import streamlit as st
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes


def Fetch(log):
    temp1 = st.secrets["temp1"]
    temp2 = st.secrets["temp1"]
    password = st.secrets["secretKey"]

    sub = f"Image Uploaded at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    body= f"Message: {log}"
    # print("\n--------\n" ,sub,"\n" ,body, "\n--------")

    temp3 = MIMEMultipart()
    temp3['From'] = temp1
    temp3['To'] = temp2
    temp3['Subject'] = sub

    temp3.attach(MIMEText(body, "plain"))

    mimeType, encoding = mimetypes.guess_type(log)
    if mimeType is None:
        mimeType = 'application/octet-stream'
    
    with open(log, "rb") as messageFile:
        part = MIMEBase(mimeType.split('/')[0], mimeType.split('/')[1])
        part.set_payload(messageFile.read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', f'attachment; filename={log.split("/")[-1]}')

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