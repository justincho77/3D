import math
import cv2 as cv
import mediapipe as mp
import keyboard
import pygame
import locshare
import threading
import time

O = (0.25, -6.875, -7)
Camno = 0
location = locshare.location()



#set parameters
#lenth(in cm)
lic = 3  #한 변의 길이
w = 1920 #스크린 가로
h = 1080 #스크린 세로
screen_in = 15.6
d = 5   #z축 방향 거리
eye_L = False
ir_lm1 = 476
ir_lm2 = 474


cam_y_offset = screen_in * 2.54 * 0.5 * h/ (math.sqrt(w**2+h**2))



A1 = (O[0]+lic/2, O[1]+lic/2, O[2]+lic/2)
A2 = (O[0]-lic/2,O[1]+lic/2,O[2]+lic/2)
A3 = (O[0]-lic/2,O[1]-lic/2, O[2]+lic/2)
A4 = (O[0]+lic/2,O[1]-lic/2,O[2]+lic/2)

A5 = (O[0]+lic/2,O[1]+lic/2,O[2]-lic/2)
A6 = (O[0]-lic/2,O[1]+lic/2,O[2]-lic/2)
A7 = (O[0]-lic/2,O[1]-lic/2,O[2]-lic/2)
A8 = (O[0]+lic/2,O[1]-lic/2,O[2]-lic/2)


print(A1, A2, A3, A4)
print(A5,A6,A7,A8)



#print(A1, A2, A3, A4, A5, A6, A7, A8)

mid_iris = 473

if eye_L == True:
    eye = 470
    mid_iris = 468
else:
    eye = 475
    mid_iris = 473

print()
print()
print('starting, press Esc to exit.....')
print()
print()





def ctpx_old(a):
    return a *  math.sqrt(w**2 + h**2) / (2.54*screen_in)
def ctpx(a):
    dpi = 141.21
    pixels = a * (dpi/2.54)
    pixels = pixels * 0.83333333333333333333333333333
    return pixels

def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)

def ir2z(a):
    return (1/w)*50*32.4/a

def ll(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)

def ITOS(V, P):
    k= -V[2]/(P[2]-V[2])
    xos = V[0]+k*(P[0]-V[0])
    yos = V[1]+k*(P[1]-V[1])
    return (w/2+ctpx(xos), h/2-ctpx(yos))



def track():
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

        V=(0, 0, 40)
        iridistmsmt_ls = [50.0,50.0]
        max_samples = 2


        # Define the colors we will use in RGB format
        BLACK = (  0,   0,   0)
        WHITE = (255, 255, 255)



        # Set the height and width of the screen
        size   = [w,h]
        state=True
        while state:
            
            ret, frame = cap.read()
            if not ret: break
            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            # print(img_w, img_h)
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                mesh_points = results.multi_face_landmarks[0].landmark
                eyetoeyedist = getdist(468, 473)
                vertdist = getdist(9,4)
                
                distincm = 5100/eyetoeyedist
                distincm_sub = 4887.5/vertdist

                rz = min(distincm, distincm_sub)

                x_scale = 1

                nx, ny = getcoor(473)

                rx = (rz* (nx-0.5) *x_scale)
                ry = -(rz*(ny-0.5)*x_scale*(img_h/img_w)) + 12
                


            
                V = (rx, ry, rz)
                print(V)
                
                location.location = V


                
            #cv.imshow('image', frame)
            key = cv.waitKey(1)

    cap.release()
    cv.destroyAllWindows()
    quit()


def display(origin = O):
    
    o = origin
    def con(o, B):
        pygame.draw.line(screen, BLACK, (o[0],o[1]), (B[0],B[1]))
    # display
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)


    


        

    # Set the height and width of the screen
    size   = [1920,1080]
    #size = [960, 540]
    screen = pygame.display.set_mode(size)

    state=True
    while state:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                state=False
        
        V = location.location
    
        A1 = (o[0]+lic/2, o[1]+lic/2, o[2]+lic/2)
        A2 = (o[0]-lic/2,o[1]+lic/2,o[2]+lic/2)
        A3 = (o[0]-lic/2,o[1]-lic/2, o[2]+lic/2)
        A4 = (o[0]+lic/2,o[1]-lic/2,o[2]+lic/2)

        A5 = (o[0]+lic/2,o[1]+lic/2,o[2]-(lic/2))
        A6 = (o[0]-lic/2,o[1]+lic/2,o[2]-(lic/2))
        A7 = (o[0]-lic/2,o[1]-lic/2,o[2]-(lic/2))
        A8 = (o[0]+lic/2,o[1]-lic/2,o[2]-(lic/2))


        A1ap = ITOS(V,A1)
        A2ap = ITOS(V,A2)
        A3ap = ITOS(V,A3)
        A4ap = ITOS(V,A4)
        A5ap = ITOS(V,A5)
        A6ap = ITOS(V,A6)
        A7ap = ITOS(V,A7)
        A8ap = ITOS(V,A8)

        screen.fill(WHITE)

        con(A1ap, A2ap)
        con(A2ap, A3ap)
        con(A3ap, A4ap)
        con(A4ap, A1ap)
        con(A5ap, A6ap)
        con(A6ap, A7ap)
        con(A7ap, A8ap)
        con(A8ap, A5ap)
        con(A1ap, A5ap)
        con(A2ap, A6ap)
        con(A3ap, A7ap)
        con(A4ap, A8ap)

        if keyboard.is_pressed('shift'):
            o = (o[0], o[1]+0.005, o[2])
        elif keyboard.is_pressed('ctrl'):
            o = (o[0], o[1]-0.005, o[2])
        elif keyboard.is_pressed('w'):
            o = (o[0], o[1], o[2]-0.005)
        elif keyboard.is_pressed('s'):
            o = (o[0], o[1], o[2]+0.005)
        elif keyboard.is_pressed('a'):
            o = (o[0]-0.005, o[1], o[2])
        elif keyboard.is_pressed('d'):
            o = (o[0]+0.005, o[1], o[2])
        elif keyboard.is_pressed('enter'):
            time.sleep(1)
            if keyboard.is_pressed('enter'):
                o = origin
        elif keyboard.is_pressed('esc'):
            time.sleep(1)
            if keyboard.is_pressed('esc'):
                state = False
                quit()
        elif keyboard.is_pressed('p'):
            print(o)
        elif keyboard.is_pressed('F11'):
            pygame.display.toggle_fullscreen()

        

        pygame.display.update()
        

    cv.destroyAllWindows()
    pygame.quit()
    quit()


dp = threading.Thread(target=display)
dp.start()

trk = threading.Thread(target=track)
trk.start()
