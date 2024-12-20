from gpiozero import MotionSensor
from picamera2 import Picamera2, Preview
import time
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

pir = MotionSensor(4)

cam = Picamera2()
camera_config = cam.create_still_configuration()  
cam.configure(camera_config)  
cam.start()  

from_email_addr = 'From-email'
from_email_password = 'password'
to_email_addr = 'To-email'
subject = 'Security alert!'

while True:
    if pir.motion_detected:
        print("Motion detected!")
        time.sleep(2)
        picname = datetime.now().strftime("%y-%m-%d-%H-%M") + '.jpg'
        cam.capture_file(picname) 
        time.sleep(5)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr

        with open(picname, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user=from_email_addr, password=from_email_password)
        server.send_message(msg)
        server.quit()
    else:
        print("No motion detected.")
