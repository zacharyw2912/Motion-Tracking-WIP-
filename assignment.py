# ********** NOTES **********
# 1) To test email functionality the examiner MUST change the receiver email to an email they have access to
# 2) The login details for the code are : Username = admin and Password = CSY3058
# 3) Examiner must have pip version 24.3.1 or newer
# ******************************

# Import statements
import smtplib
from tkinter import *
from tkinter import filedialog, messagebox
import cv2
import time
from tkVideoPlayer import TkinterVideo

# Initializing the label, for the video, and the player
my_label = None
player = None

# The objects / variables that will be used to save segments of the video
video_writer = None
motion_recording = False
frame_rate = 30
folder_path = None


# Initiating the variables that will be used to store the windows, so that they can be closed when a new window is open
insert = None
live = None
home = None


# The function that displays the login window
def loginWindow():

    # Sub-function to verify that the username and password
    def verifyLogin():

        # Collecting the inputted username and password form the entry boxes and storing it in variables
        username = username_entry.get()
        password = password_entry.get()

        # If statement to test if the input matches the username and password correctly, if so destroy the login window and open the home page
        if username == "admin" and password == "CSY3058":
            login.destroy()
            homeWindow()
        else:
            # Erorr message that shows if the username or password are incorrect
            messagebox.showerror("Login Failed", "Incorrect username or password")

    # Creating the login Tk.window, assigning the title and setting the dimensions in px
    login = Tk()
    login.title("Login page")
    login.geometry("1000x600")

    # Labels and entry boxes for the username and password, and inputting them onto the page
    username_label = Label(login, text="Username: ")
    username_label.pack()
    username_entry = Entry(login)
    username_entry.pack()

    password_label = Label(login, text="Password: ")
    password_label.pack()

    password_entry = Entry(login, show="*")
    password_entry.pack()

    #The button to input the username and password, that starts the verifyLogin function
    login_button = Button(login, text="Login", command=lambda: verifyLogin())
    login_button.pack()

    #Adding the window to the mainloop
    login.mainloop()


# The function that stores the home window
def homeWindow():

    # Making the home variable global, so that it can be accessed outside the function
    global home


    home = Tk()
    home.title("Warehouse CCTV")
    home.geometry("1000x600")

    # If the insert window is open, destroy it
    if insert:
        insert.destroy()

    # If the live window is open, destroy it
    if live:
        live.destroy()

    # Buttons that redirect the user to new windows
    liveBtn = Button(home, text="Live Feed", command=lambda: liveWindow())
    liveBtn.pack(pady=20)

    insertBtn = Button(home, text="Review Footage", command=lambda: insertWindow())  # Button that will open a new
    insertBtn.pack(pady=20)

    home.mainloop()


# The function that opens the insert window
def insertWindow():

    #Destory the home window
    home.destroy()

    global insert

    # Make the new window, and call it "insert", define the title and the dimensions of the window in px
    insert = Tk()
    insert.title("Cameras")
    insert.geometry("1000x600")

    # Storing the image that will be used for the home button
    homeImage = PhotoImage(file=r"images.png")

    # Resizing the image so that it fits within the button
    photoImage = homeImage.subsample(6, 6)

    # Function within that allows the user to select the file
    def fileSelect():

        # Folder_path can now be accessed outside the function
        global folder_path

        # Label is a placeholder for text or a video
        global my_label, player

        # If a video is already playing, destroy it
        if my_label:
            my_label.destroy()
            player.destroy()

        # Place the label onto the "insert" window
        my_label = Label(insert)
        my_label.pack()

        # Selects the file that the user chooses, and stores it in the variable
        folder_path = filedialog.askopenfilename(title="Select A File", filetypes=(("mov", "*.mov"),))

        # Placing the player in the insert window, and filling out it's dimensions - as well as allowing the video within player to begin
        player = TkinterVideo(insert)
        player.load(folder_path)
        player.pack(expand=True, fill="both")
        player.play()

        # Function that allows the user to play the video
        def play():
            global player
            if player:
                player.play()

        # Function that allows the user to pause the video
        def pause():
            global player
            if player:
                player.pause()

        # Placing the play/pause/insert file/motion detection buttons on the screen
        play = Button(insert, text="Play", command=play)
        play.pack(pady=10)

        pause = Button(insert, text="Pause", command=pause)
        pause.pack(pady=10)

        motion = Button(insert, text="Motion", command=motionDetection)
        motion.pack(pady=10)

    # Button that allows the user to input the file, using the fileSelect function
    insertFileBtn = Button(insert, text="Insert File", command=fileSelect)
    insertFileBtn.pack(pady=20)

    # Button that allows the user to return to the home page
    homeBtn = Button(insert, image=photoImage, command=lambda: homeWindow())
    homeBtn.config(height=40, width=40)
    homeBtn.place(x=50, y=20)

    insert.mainloop()


# The function that shows the "live" video
def liveWindow():

    home.destroy()

    global live

    live = Tk()
    live.title("Cameras")
    live.geometry("1000x600")

    homeImage = PhotoImage(file=r"images.png")
    photoImage = homeImage.subsample(6, 6)

    # Widgets allow for multiple videos to be placed on the screen at once
    video_widget1 = TkinterVideo(live, scaled=True)
    video_widget1.load("nv232.mov")
    video_widget1.place(x=150, y=0, width=400, height=300)

    video_widget2 = TkinterVideo(live, scaled=True)
    video_widget2.load("nv236.mov")
    video_widget2.place(x=600, y=0, width=400, height=300)

    # Loop the current videos, to appear like they are live
    def videoLoop():
        video_widget1.seek(0)
        video_widget1.play()

        video_widget2.seek(0)
        video_widget2.play()

    # Place the videos inside the widgets so that they can b ee positioned appropriately
    video_widget1.bind('<<Ended>>', lambda event: videoLoop())
    video_widget2.bind('<<Ended>>', lambda event: videoLoop())

    homeBtn = Button(live, image=photoImage, command=lambda: homeWindow())
    homeBtn.config(height=40, width=40)
    homeBtn.place(x=50, y=20)

    # Call the videoLoop function so that the videos loop indefinitely
    videoLoop()
    live.mainloop()


# The function that detects motion, and sends an alert email
def motionDetection():

    global motion_recording, video_writer

    # The email that is sending the alert
    email = ("testpurposeemail420")

    # The email that receieve the alert, REVIEW NOTES
    receiver_email = ("zachary.white2912@gmail.com")

    # The subject and message of the email
    subject = ("Unauthorized motion detected")
    message = ("------------------------------------------------------ ALERT -------------------------------------------------------- \n \n \n"
               "               MOTION DETECTED ON PREMISES  \n \n \n"
               "               REVIEW FOOTAGE IMMEDIATELY IN SOFTWARE ")

    # Putting the subject and message into the email
    text = f"Subject: {subject}\n\n{message}"

    # Connecting to the server that allows the emails to be sent automatically
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # The app password for the dud email
    server.login(email, "gphn szrb wccf yuej")



    # Allows the video to be split frame by frame
    cap = cv2.VideoCapture(folder_path)

    # The first frame of the video is always 1
    frame_number = 1

    # The duration that the clip made will be in, in seconds
    recording_duration = 5
    start_time = None

    # Error trapping, if there is an error attempting to open the file
    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    # Error trapping, if there is an error attempting to start the video
    _, start_frame = cap.read()
    if start_frame is None:
        print("Error: Could not read the starting frame.")
        exit()

    # Making the first frame grey scale, and adding gaussian blur which makes the motion detection appear smoother
    start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
    start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)
    email_sent = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        # Working out the difference between the current frame, and the first frame
        difference = cv2.absdiff(frame_bw, start_frame)

        # Converting the difference into binary
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        # Execute the code if the threshold is created than 250 and there is not already being motion recorded
        if threshold.sum() > 250 and not motion_recording:
            print("Motion detected, starting video recording!")
            motion_recording = True
            start_time = time.time()

            # Files saved will use the H.264 codec, to increase efficiency
            fourcc = cv2.VideoWriter_fourcc(*'mpv4')

            # The filename will be unique based on the timestamp of the video
            output_filename = f"motion_segment_{time.time()}.mp4"
            video_writer = cv2.VideoWriter(output_filename, fourcc, frame_rate, (int(cap.get(3)), int(cap.get(4))))


        if motion_recording:
            # Write the current frame to the video file
            video_writer.write(frame)

            if not email_sent:
                server.sendmail(email, receiver_email, text)
                print("Email has been sent")
                email_sent = True




            # Check if the recording time has passed
            if time.time() - start_time >= recording_duration:
                print("Recording finished.")
                motion_recording = False
                video_writer.release()

        # Show the threshold image (motion detection)
        cv2.imshow("Motion", threshold)
        key_pressed = cv2.waitKey(30)
        if key_pressed == ord("q"):
            break

    # Release everything
    cap.release()
    if video_writer:
        video_writer.release()

    cv2.destroyAllWindows()


# Open the program with the loginWindow function
if __name__ == "__main__":
   loginWindow()