import cv2, face_recognition, pickle, os

pathList   = os.listdir('wp')
imgList    = []
personsIDs = []


for path in pathList:
    # appending images on imgList
    imgList.append(cv2.imread(os.path.join('wp',path)))
    # appending students ids into students list 
    personsIDs.append(path.split(".")[0])

def findEncodings(imgagesList):
     encodeList = []
     for img in imgagesList:
        # Converting colors because face-recognitions library use RGB colors and CV2 use BGR  
          img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)         
        # encoding the image and append it to the enocodelist   
          encode = face_recognition.face_encodings(img)[0]
          encodeList.append(encode)
     return encodeList

# Remove First element from imgs array that equals None which will occure error in converting Colors
imgList.pop(0)
personsIDs.pop(0)
print("[1/3] Encoding started...")

# Encode Photos
encodingList = findEncodings(imgList)
encodingListWithIDs = [encodingList,personsIDs]

print("[2/3] Writing the File...")

# Save Encoding resault into endoceFile.p
file = open("encodeFile.p","wb")
pickle.dump(encodingListWithIDs,file)
file.close()

print("[3/3] Done.")
