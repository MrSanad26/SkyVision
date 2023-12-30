import cv2, cvzone, pickle, face_recognition, numpy as np, pymongo as mg, json, datetime
from urllib.request import urlopen

# Connect to database
client = mg.MongoClient('localhost', 27017).get_database(
        'skyvision').get_collection('wantedPeople')

# Captrue camera and set the height and width
w, h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

# import banners
banner = [cv2.imread('static/1.png'), cv2.imread('static/2.png'),
          cv2.imread('static/3.png'), cv2.imread('static/4.png')]

mode = 0

# Loading the encoding file
file = open("encodeFile.p", "rb")
encodingListWithIDs = pickle.load(file)
file.close

# declare wnated person id that we will use it to pull from Firebase
id = ""

# declare Info which will hold person data
info = {}
listInfo = []

# Saperate Encoding List and the id list to variables
encodesList, ids = encodingListWithIDs

arrowCounter = 0

# counter to make the banner deny or approve wait for period
counter = 0

while True:

    # import Background
    bg = cv2.imread('static/bg.png')

    # capture frames from camera
    success, img = cap.read()

    # Resizing the farame to make it smaller to be easy in calculation
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Get Face Location to encode only the face not the hole image z
    faceCurFrame = face_recognition.face_locations(imgS)

    # Encode the face by giving the function the image and the location of the face
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Check if the number of people who front the camera is not the same with people in the Dictinary it will clear it and dump the data again
    if len(info) != len(encodeCurFrame):
        arrowCounter = 0
        info = {}
        listInfo = []

    # put the captured camera on the background
    y, x = 50, 140
    bg[y:y+h, x:x+w] = img

    # Put the banner on the Background
    yy, xx = 11, 931
    bg[yy:yy+698, xx:xx+342] = banner[mode]

    # Looping throw all encodings and Compare with face
    # We use zip to loop throw two different arrays other ways we should make 2 for loops saperatly
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):

        # Matches is a Boolean value of which one of the images is match the face.
        # for exapmle if the face in the frame match the second image of total three images, resault will be : [False, True, False]
        matches = face_recognition.compare_faces(encodesList, encodeFace, tolerance = 0.55)

        # Face Distance is a Floeat value of which one of the images is match the face, the closer the number to the zero, the more accurate it is.
        # for exapmle if the face in the frame match the second image of total three images, resault will be : [0.85614333, 0.33314733, 0.73614733]
        faceDis = face_recognition.face_distance(encodesList, encodeFace)

        # Find the index of the match face
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:

            # Make banner Approved or Denied still in the screen for time (if the face still front camera)
            if mode == 1 or mode == 2 or mode == 3:
                if counter < 50:
                    counter = counter + 1
                else:
                    mode = 1
                    counter = 0
            else:
                mode = 1

            # assaign the persons id
            id = ids[matchIndex]

            # Put the facepositions into variables to draw a rectangle around the face
            y1, x2, y2, x1 = faceLoc

            # Multiply the values by 4 becaus e we divde it to 4 in imgS
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            # Set the rectangle positions and draw it
            bbox = x1 + x, y1 + y, x2 - x1, y2 - y1
            bg = cvzone.cornerRect(bg, bbox, rt=1)

            # make logic to import data once
            if id not in info:
                info[f"{id}"] = client.find_one(
                    {f"{id}": {"$exists": True}}, projection={"_id": False})[f"{id}"]
                listInfo = list(info.values())

            # Inserting Texts into the frame when wanted found
            # Write persons name above his face
            cvzone.putTextRect(bg, info[id]["Name"], (x1 + x, y1 + y), 1, 1,
                               (255, 255, 255), (0, 255, 0), cv2.FONT_HERSHEY_COMPLEX_SMALL)
            sPX, sPY = 400, 950
            # Number of wanted people front the camera
            cv2.putText(bg, f'Wanted People in the Camera: {len(info)}', (
                sPY, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 255, 255), 1)
            # Inserting person info
            cv2.putText(bg, f'ID: {listInfo[arrowCounter]["ID"]}', (
                sPY, sPX+00), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            cv2.putText(bg, f'Name: {listInfo[arrowCounter]["Name"]}', (
                sPY, sPX+40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            cv2.putText(bg, f'Severity: {listInfo[arrowCounter]["Severity"]}', (
                sPY, sPX+80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            cv2.putText(bg, f'Last Time: {listInfo[arrowCounter]["Last Time"]}', (
                sPY, sPX+120), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            cv2.putText(bg, f'Last Location:', (sPY, sPX+160),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            cv2.putText(bg, f'{listInfo[arrowCounter]["Last Location"]}', (
                sPY, sPX+200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (255, 255, 255), 1)
            # Inserting Wanted Persons Photo
            bg[100:100+216, 995:995 +
                216] = cv2.imread(f'wantedPersons/{listInfo[arrowCounter]["ID"]}.png')
               
            # If Button O pressed
            if key == 111:
                # Change mode to Denied
                mode = 3

            # If Button P pressed
            if key == 112:
                # Change Mode to approved
                mode = 2
                # Get the current location
                url = "http://ipinfo.io/json"
                res = urlopen(url)
                data= json.load(res)

                # Setting the fromate date
                loc = data["city"] + ", " +data["region"] + ", " + data["country"]
                # Set the update location path and value
                update_location = {'$set': {f'{listInfo[arrowCounter]["ID"]}.Last Location': loc}}
                # Update the Location
                client.update_one({f'{listInfo[arrowCounter]["ID"]}': {"$exists": True}}, update_location)

                # Get the time and set the format
                now = datetime.datetime.now()
                formatted_time = now.strftime("%Y/%m/%d|%H:%M:%S")
                # Set the update time path and value
                update_time = {'$set': {f'{listInfo[arrowCounter]["ID"]}.Last Time': formatted_time}}
                # Update the last time seen
                client.update_one({f'{listInfo[arrowCounter]["ID"]}': {"$exists": True}}, update_time)

                # Show the new data after update, if you don't do this step you will need to remove the face the camera and put it again
                info = {}
                listInfo = []
                info[f"{id}"] = client.find_one({f"{id}": {"$exists": True}}, projection={"_id": False})[f"{id}"]
                listInfo = list(info.values())

        # Make banner Approved or Denied still in the screen for time (if the face not front camera)
        else:
            if mode == 0 or mode == 2 or mode == 3:
                if counter < 50:
                    counter = counter + 1
                else:
                    mode = 0
                    counter = 0

    # Change banner mode to searching when nobody front the camera
    if len(faceCurFrame) == 0:
        mode = 0
    # Show the Apllication page
    cv2.imshow("SKY Vision", bg)
    key = cv2.waitKey(1)

    # if ESC key pressed it will exit the app
    if key == 27:
        break

    # if right arrow key pressed it weill change the person on the camerainfo
    if key == 3:
        arrowCounter = arrowCounter + 1
        if arrowCounter >= len(info):
            arrowCounter = 0

    # if left arrow key pressed it weill change the person on the camerainfo
    if key == 2:
        arrowCounter = arrowCounter - 1
        if arrowCounter < 0:
            arrowCounter = len(info)-1

cv2.destroyAllWindows()