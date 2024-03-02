import math
import cv2 as cv
import mediapipe as mp
import keyboard
import json


sceeninfocalibrated = False
caminfocalibrated = False
Camno = 0


print()
print()
print('starting, press Esc to exit.....')
print()
print()

def readfromjson(name):
    with open(name, "r") as filehandle:
        data = json.load(filehandle)
        return data

def write2json(filename, data):
    with open(filename, "w") as filehandle:
        json.dump(data, filehandle)




def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)

def ll(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)





def calibratecam():
    mp_face_mesh = mp.solutions.face_mesh

    #cap = cv.VideoCapture(0)
    cap = cv.VideoCapture(Camno, cv.CAP_DSHOW)

    def getcoor(landmarkno):
        x, y = mesh_points[landmarkno].x, mesh_points[landmarkno].y
        return x,y

    def getdist(landmarkno1, landmarkno2, captureimgw = 640, captureimgh = 480):
        x1, y1 = getcoor(landmarkno1)
        x1, y1 = x1 * captureimgw, y1*captureimgh
        x2,y2 = getcoor(landmarkno2)
        x2, y2 = x2* captureimgw, y2*captureimgh
        return ll(x1,y1, x2,y2)


    with mp_face_mesh.FaceMesh(
        max_num_faces=1, refine_landmarks=True, min_detection_confidence = 0.5,    
    ) as face_mesh:

        state=True
        while state:
            
            ret, frame = cap.read()
            if not ret: break
            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            # print(img_w, img_h)
            results = face_mesh.process(rgb_frame)
            step = 'distancecal'

            if results.multi_face_landmarks:
                mesh_points = results.multi_face_landmarks[0].landmark
                eyetoeyedist = getdist(468, 473)
                vertdist = getdist(9,4)
                
                if step == 'distancecal':
                    calparam = 'distincm'
                    print('starting calibration for distance estimation. please prepare a ruler for measuring the actual distance.')
                    do = True
                    while do:
                        distincmparam = 3600
                        distincm_subparam = 3450
                        print('calibrating first method for calculation. use the up and down arrow keys to make the value on screen match the actual distance measured.')
                        if calparam == 'distincm':
                            distincm = distincmparam/eyetoeyedist
                            print(distincm)
                            if keyboard.is_pressed('up'):
                                distincmparam += 1
                            elif keyboard.is_pressed('down'):
                                distincmparam -= 1


                            elif keyboard.is_pressed('enter'):
                                calparam = 'distincm_sub'

                        print('calibrating second method for calculation. use the up and down arrow keys to make the value on screen match the actual distance measured.')
                        if calparam == 'distincm_sub':
                            distincm_sub = distincm_subparam/vertdist
                            print(distincm_sub)
                            if keyboard.is_pressed('up'):
                                distincm_subparam += 1
                            elif keyboard.is_pressed('down'):
                                distincm_subparam -= 1

                                
                            elif keyboard.is_pressed('enter'):
                                step = 'yoffsetcalc'
                                do = False




                cam_y_offset = 12
                if step == 'yoffsetcalc':
                    do = True
                    print('starting calibration for the camera offset from the screen center. place your eyes approximately at the center of the screen,')
                    print('then use the up and down arrow keys to make the value on screen be 0.')
                    while do:
                        distincm = distincmparam/eyetoeyedist
                        rz = distincm

                        nx, ny = getcoor(473)
                        

                        rx = (rz* (nx-0.5) )
                        ry = -(rz*(ny-0.5)*(img_h/img_w)) + cam_y_offset
                        print(ry)
                        
                        if keyboard.is_pressed('up'):
                            cam_y_offset += 0.05
                        elif keyboard.is_pressed('down'):
                            cam_y_offset -= 0.05
                        elif keyboard.is_pressed('enter'):
                            step = 'finished'
                            do = False
                
                if step == 'finished':
                    print('calibration finished, outputting file as json.')
                    outputdata = [distincmparam, distincm_subparam, cam_y_offset]
                    write2json('caminfo.json', outputdata)

                                
            cv.imshow('image', frame)
            key = cv.waitKey(1)

    cap.release()
    cv.destroyAllWindows()
    quit()

