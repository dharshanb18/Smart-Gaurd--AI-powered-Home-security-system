from datetime import datetime, timedelta
import face_recognition
import cv2
import numpy as np
import csv
import smtplib
from email.message import EmailMessage
import pyttsx3


csv_file_path = r"D:\RAO\IoT\IOT project\photos.csv"

# Create empty lists to store the values
known_face_encoding = []

known_faces_names = []

print("Please wait.. initialising..")
print("Getting Faces..")
# Read the CSV file and store the values in the lists
with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # print(row[0])
        image = face_recognition.load_image_file(f"{row[0]}")
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encoding.append(encoding)  
        known_faces_names.append(f"{row[1]}")  

# Print the values in the lists
# print("Values in Column 1:", column1_values)
# print("Values in Column 2:", column2_values)


video_capture = cv2.VideoCapture(0)

# jobs_image = face_recognition.load_image_file(r"D:\RAO\IoT\IOT project\photos\jobs.jpg")
# jobs_encoding = face_recognition.face_encodings(jobs_image)[0]

# ratan_tata_image = face_recognition.load_image_file(r"D:\RAO\IoT\IOT project\photos\tata.jpg")
# ratan_tata_encoding = face_recognition.face_encodings(ratan_tata_image)[0]

# sadmona_image = face_recognition.load_image_file(r"D:\RAO\IoT\IOT project\photos\monalisa.jpg")
# sadmona_encoding = face_recognition.face_encodings(sadmona_image)[0]

# tesla_image = face_recognition.load_image_file(r"D:\RAO\IoT\IOT project\photos\tesla.jpg")
# tesla_encoding = face_recognition.face_encodings(tesla_image)[0]


students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open("entrylogiotsecurity" + '.csv', 'a', newline='')
lnwriter = csv.writer(f)



# Initialize pyttsx3
engine = pyttsx3.init()
print("Smile to the Camera!!..")
def run():
    i=0
    # Initialize variables for intruder detection
    intruder_detected = False
    intruder_start_time = None
    intruder_emails_sent = []  # List to store emails sent for each intruder
    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if s:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
                name = ""
                face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
                best_match_index = np.argmin(face_distance)
                if matches[best_match_index]:
                    name = known_faces_names[best_match_index]
                else:
                    # Intruder detected
                    if not intruder_detected or (intruder_detected and name not in intruder_emails_sent):
                        intruder_detected = True
                        intruder_start_time = datetime.now()
                        intruder_emails_sent.append(name)
                        # return "intruder1"
                    else:
                        # Check if the intruder has been detected for more than 10 seconds
                        if datetime.now() - intruder_start_time > timedelta(seconds=10):
                            # Send email
                            smtp_server = "smtp.gmail.com"
                            port = 587
                            sender_email = "dharshanbalajikaruppa18@gmail.com"
                            receiver_email = "yaswantharao.p2021@vitstudent.ac.in"
                            password = "vpqy tsad nqri rlec"

                            server = smtplib.SMTP(smtp_server, port)
                            server.starttls()
                            server.login(sender_email, password)

                            # Say "Intruder has been detected"
                            engine.say("Intruder has been detected. Sending mail to house owner. Please wait for the reply. Thank you.")
                            engine.runAndWait()

                            message = EmailMessage()
                            message.set_content("Intruder detected! Take a look at the entrance please.")
                            i+=1
                            current_date = now.strftime("%Y-%m-%d")
                            current_time = now.strftime("%H-%M-%S")
                            file_name = f'intruder_frame_No{i}_{current_date}_{current_time}.jpg'
                            cv2.imwrite(f'intruders_photos/{file_name}', frame)
                            ret, buffer = cv2.imencode('.jpg', frame)
                            message.add_attachment(buffer.tobytes(), maintype='image', subtype='jpeg', filename=file_name)

                            message["Subject"] = "Intruder Alert!"
                            message["From"] = sender_email
                            message["To"] = receiver_email

                            server.send_message(message)
                            server.quit()

                            intruder_start_time = datetime.now()  # Reset the timer
                            with open("result/result.txt", "w") as file:
                            # Write "Housemate" into the file
                                file.write("Intruder")
                            return "intruder2"

                face_names.append(name)
                if name in known_faces_names:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    bottomLeftCornerOfText = (10, 100)
                    fontScale = 1.5
                    fontColor = (255, 0, 0)
                    thickness = 3
                    lineType = 2

                    cv2.putText(frame, name + ' is detected',
                                bottomLeftCornerOfText,
                                font,
                                fontScale,
                                fontColor,
                                thickness,
                                lineType)

                    if name in students:
                        print(students)
                        current_date = now.strftime("%Y-%m-%d")
                        current_time = now.strftime("%H-%M-%S")
                        lnwriter.writerow([name, current_date, current_time])
                        # Say "WELCOME HOME <name>"
                        engine.say(f"WELCOME HOME {name}. You can enter the house. Thank you.")
                        engine.runAndWait()
                        # Open the file in write mode
                        with open("result/result.txt", "w") as file:
                            # Write "Housemate" into the file
                            file.write("Housemate")
                        return "housemate"

        cv2.imshow("Smart-Guard: AI-powered Home Security System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

print(run())
video_capture.release()
cv2.destroyAllWindows()
f.close()

