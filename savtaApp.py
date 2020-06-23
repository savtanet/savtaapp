import tkinter
from PIL import ImageTk, Image
from TextToSpeech import talkToUser
from SpeechRecognition import recognizeSpeech
import socket
import os

#SERVER_IP = "127.0.0.1"
#SERVER_PORT = 2512

SERVER_IP = "185.195.168.10"
SERVER_PORT = 8080

def answerPage(oldMaster, answer):
    oldMaster.destroy()
    root = tkinter.Tk()
    root.title("Savta App")
    app = FullScreenApp(root)

    tkinter.Label(root, text=answer[0] + " " + answer[1], font=("Arial", "30")).pack()
    tkinter.Label(root, text=answer[2], font=("Arial", "30")).pack()
    tkinter.Label(root, text=answer[3], font=("Arial", "30")).pack()


    root.mainloop()


def getSavtaName():
    return "Kane"

def startConnection():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connecting to remote computer 80
    server_address = (SERVER_IP, SERVER_PORT)
    sock.connect(server_address)

    return sock

def getServerAnswer(request):
    sock = startConnection()

    # Sending data to server
    msg = getSavtaName() + ":" + request
    sock.sendall(msg.encode())

    # Receiving data from the server
    server_msg = sock.recv(1024)
    server_msg = server_msg.decode()
    print(server_msg)
    # Closing the socket
    sock.close()

    return server_msg.split(":")


def startConversation(root):
    talkToUser("Welcome savta, how i can help you today?")
    request = recognizeSpeech()
    while request is None:
        talkToUser("I did not get it, please tell me again")
        request = recognizeSpeech()

    talkToUser("Ok, we are searching for representative, please wait")
    print(request)
    answer = getServerAnswer(request)

    talkToUser("Thank you for using our services, goodbye")

    answerPage(root,answer)


class FullScreenApp(object):
    def __init__(self, master):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth() - pad * 200,
                                             master.winfo_screenheight() - pad * 50))  # *200 , *50
        master.bind('<Escape>', self.toggle_geom)
        self.master.config(bg='white')

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

def mainPage():
    root = tkinter.Tk()
    root.title("Savta App")
    app = FullScreenApp(root)

    img = Image.open("redCircle.png")
    img = img.resize((350, 350))
    imag = ImageTk.PhotoImage(img)

    button = tkinter.Button(root, text="Get Help", font=("Rainy Days", "30", "bold") , image=imag, bg="white",
                            compound="center", relief="raised", bd=0, command=lambda : startConversation(root))
    button.place(x=200, y=100)

    root.mainloop()


def signupPage(oldMaster):
    oldMaster.destroy()

    root = tkinter.Tk()
    root.title("Savta App")
    app = FullScreenApp(root)

    root.update()
    root.geometry("" + str(root.winfo_width()) + "x" + str(root.winfo_height()))

    # create a Form label
    heading = tkinter.Label(root, text="Please signup for the\n first time", bg="white" ,font=("Rainy Days", "25"))

    # create a Name label
    name = tkinter.Label(root, text="Name", bg="white", fg="black", font=("Arial", "12", "italic bold"))

    v = tkinter.IntVar()
    v.set(1)
    maleRadioBut = tkinter.Radiobutton(root, text="Male", padx=20, variable=v, value=1, font=("Arial", "9", "italic bold"),
                               bg="white")
    femaleRadioBut = tkinter.Radiobutton(root, text="Female", padx=20, variable=v, value=2, font=("Arial", "8", "italic bold"),
                                 bg="white")

    # create a phone id label
    phone = tkinter.Label(root, text="Phone Number", bg="white", fg="black", font=("Arial", "12", "italic bold"))

    age = tkinter.Label(root, text="Age", bg="white", fg="black", font=("Arial", "12", "italic bold"))

    city = tkinter.Label(root, text="City", bg="white", fg="black", font=("Arial", "12", "italic bold"))

    languages = tkinter.Label(root, text="Languages", bg="white", fg="black", font=("Arial", "12", "italic bold"))

    leavingAlone = tkinter.Label(root, text="Are you leaving alone?", bg="white", fg="black", font=("Arial", "10", "italic bold"))

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    heading.grid(row=0, column=1, columnspan=3)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=1, column=0)
    name.grid(row=2, column=0)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=3, column=0)
    maleRadioBut.grid(row=4, column=0)
    femaleRadioBut.grid(row=4, column=1)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=5, column=0)
    phone.grid(row=6, column=0)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=7, column=0)

    ####################
    age.grid(row=8, column=0)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=9, column=0)
    city.grid(row=10, column=0)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=11, column=0)
    languages.grid(row=12, column=0)
    tkinter.Label(root, text="", bg="white",font=("Arial", 10)).grid(row=13, column=0)
    leavingAlone.grid(row=14, column=0)
    ####################

    tkinter.Label(root, text="", bg="white", font=("Arial", 20)).grid(row=15, column=0)

    nameString = tkinter.StringVar()
    phoneString = tkinter.StringVar()
    ageString = tkinter.StringVar()
    cityString = tkinter.StringVar()
    languagesString = tkinter.StringVar()
    leavingAloneString = tkinter.StringVar()

    # create a text entry box
    # for typing the information
    name_field = tkinter.Entry(root, textvariable=nameString, bg="gray97")
    phone_field = tkinter.Entry(root, textvariable=phoneString, bg="gray97")
    age_field = tkinter.Entry(root, textvariable=ageString, bg="gray97")
    city_field = tkinter.Entry(root, textvariable=cityString, bg="gray97")
    languages_field = tkinter.Entry(root, textvariable=languagesString, bg="gray97")
    leavingAlone_field = tkinter.Entry(root, textvariable=leavingAloneString, bg="gray97")

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    name_field.grid(row=2, column=1, ipadx="20")
    phone_field.grid(row=6, column=1, ipadx="20")
    age_field.grid(row=8, column=1, ipadx="20")
    city_field.grid(row=10, column=1, ipadx="20")
    languages_field.grid(row=12, column=1, ipadx="20")
    leavingAlone_field.grid(row=14, column=1, ipadx="20")

    errorMsgString = tkinter.StringVar()

    # create a Submit Button and place into the root window
    submit = tkinter.Button(root, text="Submit", fg="black", bg="white", font=("Arial", "16", "italic bold"))
                    #command=lambda: tryToSaveDataSignUp(errorMsgString, usernameString, emailString, v.get(), root))
    submit.grid(row=16, column=1, columnspan=3)

    tkinter.Label(root, text="", bg="white", font=("Arial", 30)).grid(row=17, column=0)
    errorMsg = tkinter.Label(root, text="", bg="white", font=("Arial", 16), fg="red", textvariable=errorMsgString).grid(row=18,
                                                                                                                column=1,
                                                                                                                columnspan=3)
    root.mainloop()


PATH_TO_USER_FILE = 'UserFile.txt'

def main():
    mainPage()

    #if os._exists(PATH_TO_USER_FILE):
     #   mainPage()
    #else:
     #   signupPage(tkinter.Tk())

    #f = open(PATH_TO_USER_FILE, "a")
    #f.write("Now the file has more content!")
    #f.close()

    #open and read the file after the appending:
    #f = open("demofile2.txt", "r")
    #print(f.read())


if __name__ == "__main__":
    main()
