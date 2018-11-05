import cv2
import os

def facecrop(image, dst_dir):

    # facedata = "haarcascade_frontalface_alt.xml"
    # facedata = cv2.CascadeClassifier('C:\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
    facedata = '/usr/local/Cellar/opencv/3.4.3/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    # print(type(facedata))

    cascade = cv2.CascadeClassifier(facedata)

    img = cv2.imread(image)

    minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    faces = cascade.detectMultiScale(miniframe)

    faceCount = 0;

    for f in faces:
        x, y, w, h = [ v for v in f ]
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
        
        # print("dst_dir: " + dst_dir)
        sub_face = img[y:y+h, x:x+w]
        fname, ext = os.path.splitext(image)
        # print("fname: " + fname)
        newFile = os.path.join(dst_dir,os.path.basename(fname)+"_cropped_"+str(faceCount)+ext)
        # print("newFile " + newFile)
        cv2.imwrite(newFile, sub_face)
        faceCount += 1



    return


#facecrop("download.jpg")
