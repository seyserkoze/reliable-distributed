import requests
import json
import os
import shutil
import sys
from tkinter import filedialog
import tkinter

serv1 = "http://128.237.193.132:102"

#set yourself up with the server
def registerPhone():
    # tell server that you would like to help find the kid
    registerBody = {"requestType":"phoneJoinReq","id": "1"}
    serverResponse = None
    try:
        serverResponse = requests.post(serv1, files=registerBody, timeout=5)
    except:
        print("unable to reach server at: " + serv1)
        print("aborting...")
        sys.exit()

    r = json.loads(serverResponse.text)
    # Parse the server response for the cloudlet's IP and Port
    cloudletIP = r["IP"]
    cloudletPort = r["port"]
    cloudlet = "http://" + str(cloudletIP) + ":" + str(cloudletPort)
    return cloudlet

#GUI
class PhoneGUI:
    def __init__(self, master, cloudlet):
        #logic variables
        self.files = []
        self.cloudlet = cloudlet

        #GUI stuff
        self.master = master
        master.title("Amber Alert Search")

        #Label
        self.label_text = tkinter.StringVar()
        self.label_text.set("Choose images to submit to help out the search!")
        self.label = tkinter.Label(master, textvariable=self.label_text)
        self.label.grid(columnspan=3, sticky=tkinter.N)

        #where we display selected files
        self.text = tkinter.Text(master, height=15, width=60)
        self.text.insert(tkinter.INSERT, "No images selected")
        self.text.config(state=tkinter.DISABLED)
        self.text.grid(columnspan=3, row=1)
        self.yscroller = tkinter.Scrollbar(master, command=self.text.yview)
        self.yscroller.grid(row=1, column=3)
        self.text.config(yscrollcommand=self.yscroller.set)

        #buttons
        self.add_button = tkinter.Button(master, text="Add Images", command=self.add_files)
        self.add_button.grid(column=0, row=3)

        self.clear_button = tkinter.Button(master, text="Clear Selection", command=self.clear)
        self.clear_button.grid(column=1, row=3)

        self.send_button = tkinter.Button(master, text="Send images", command=self.send)
        self.send_button.grid(column=2, row=3)

        self.close_button = tkinter.Button(master, text="Close", command=master.quit)
        self.close_button.grid(column=3, row=3)

    def add_files(self):
        self.text.config(state=tkinter.NORMAL)
        new_files = tkinter.filedialog.askopenfilenames(parent=root, title='Choose images to send')
        for nf in new_files:
            self.files.append(nf)
        self.label_text.set("Send these images?")
        self.text.delete(1.0, tkinter.END)
        for f in self.files:
            name = os.path.basename(f)
            self.text.insert(tkinter.INSERT, name + "\n")
        self.text.config(state=tkinter.DISABLED)

    def clear(self):
        self.text.config(state=tkinter.NORMAL)
        self.files = []
        self.text.delete(1.0, tkinter.END)
        self.text.insert(tkinter.INSERT, "No images selected")
        self.text.config(state=tkinter.DISABLED)
        self.label_text.set("Select images to send")
    
    def send(self):
        self.text.config(state=tkinter.NORMAL)
        if self.files == []:
            self.label_text.set("No Images to send! Select images first!")
            return
        # create temp directory to copy images to
        tempdir = os.getcwd() + '/__tEmPoRArY_NANI'
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        self.copyFiles(tempdir)
        # zip new directory and remove the temp folder
        shutil.make_archive('output', 'zip', tempdir)
        shutil.rmtree(tempdir)

        # send zipped directory file to cloudlet
        files = {'requestType': 'newPhotos' ,'zip': open('output.zip', 'rb')}
        requests.post(cloudlet, files=files, timeout=5)

        #delete zip file
        os.remove('output.zip')

        #clean up the gui
        self.files = []
        self.label_text.set("Images sent!, select more images to send?")
        self.text.delete(1.0, tkinter.END)
        self.text.insert(tkinter.INSERT, "No images selected")
        self.text.config(state=tkinter.DISABLED)

    #copies all files in 'files' to the directory 'tempdir'
    #currently spoofing all pic locations to Pittsburgh
    def copyFiles(self, tempdir):
        location = "Pittsburgh_PA_"
        count = 0
        for f in self.files:
            file_ending = f.split(".")[-1]
            name = location + str(count) + file_ending
            new_name = os.path.join(tempdir, name)
            shutil.copy(f, new_name)
            count += 1


######################START##################################
if len(sys.argv) == 2: #firt arg exists
    serv1 = "http://" + sys.argv[1]
if len(sys.argv) > 2:
    print("Too many commandline arguments, provide only the ip of the server")
    sys.exit()
cloudlet = registerPhone()
root = tkinter.Tk()
my_gui = PhoneGUI(root, cloudlet)
root.mainloop()
#we're done, phone leave
try:
    requests.post(cloudlet, files={'requestType': 'leave'}, timeout =5)
except:
    pass
