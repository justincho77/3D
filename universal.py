import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import pygame
import cv2 as cv
import numpy as np
import mediapipe as mp
import keyboard

#set parameters
#lenth(in cm)                   100px = 2.35cm****
lic = 2  #한 변의 길이
w = 1920 #스크린 가로
h = 1080 #스크린 세로
d = 5   #z축 방향 거리
eye_L = True

scrs = int(input("If your monitor resolution is 4K (UHD), press '1'. If your monitor resolution is 1080P (FHD), press'2'."))
if scrs == 1:
    w = 3840
    h = 2160
else: 
    w = 1920
    h = 1080

blk = int(input('Select the background color of the 3D effect. Press 1 for black (recommended) and 2 for white.'))
if blk == 1:
    bg_black = True
else:
    bg_black = False

eyei = int(input("Select the eye that will be open. Press 1 for your right eye and 2 for your left."))
if eyei == 1:
    eye_L = False
else: eye_L = True
lic = input('Write the length of one edge of the cube (In centimeters). Leaving it blank and pressing Enter will keep it at default.')
if len(lic) == 0:
    lic = 2
else:
    lic = int(lic)
d = input('Write the distance of the cube from the screen (Also in centimeters). Leaving it blank and pressing Enter will keep it at default.')
if len(d) == 0:
    d = 5
else:
    d = int(d)

if eye_L == True:
    eye = 470
else: eye = 475

print()
print()
print('starting, press Esc to exit')
print()
print()






def ctpx(a):
    return 100*a/2.35
lipx = ctpx(lic)

def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)

def ir2z(a):
    return (w/1920)*50*32.4/a

def ll(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)

def ITOS(V, P):
    k= P[2]/(V[2]-P[2])
    xos = P[0]-k*(V[0]-P[0])
    yos = P[1]-k*(V[1]-P[1])
    return (xos, yos)


if bg_black == True:
    def con(A, B):
        pygame.draw.line(screen, WHITE, (A[0],A[1]), (B[0],B[1]))
if bg_black == False:
    def con(A, B):
        pygame.draw.line(screen, BLACK, (A[0],A[1]), (B[0],B[1]))

if bg_black == True:
    def cls():
        screen.fill(BLACK)
if bg_black == False:
    def cls():
        screen.fill(WHITE)


A1 = (w/2 - lipx/2, h/2 - lipx/2, d)
A2 = (w/2 + lipx/2, h/2 - lipx/2, d)
A3 = (w/2 + lipx/2, h/2 + lipx/2, d)
A4 = (w/2 - lipx/2, h/2 + lipx/2, d)
A5 = (w/2 - lipx/2, h/2 - lipx/2, d+lic)
A6 = (w/2 + lipx/2, h/2 - lipx/2, d+lic)
A7 = (w/2 + lipx/2, h/2 + lipx/2, d+lic)
A8 = (w/2 - lipx/2, h/2 + lipx/2, d+lic)


mp_face_mesh = mp.solutions.face_mesh

cap = cv.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True, min_detection_confidence = 0.5, min_tracking_confidence=0.5
) as face_mesh:

    V=(960, 540, 40)
    num470x_ls = [960,960,960,960,960,960,960,960,960]
    num470y_ls = [960,960,960,960,960,960,960,960,960]
    iridistmsmt_ls = [50,50,50,50,50,50,50,50,50]
    max_samples = 15

    pygame.init()

    clock = pygame.time.Clock()


    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)



    # Set the height and width of the screen
    size   = [1920, 1080]
    screen = pygame.display.set_mode(size)
    state=True
    while state:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                state=False
            if keyboard.is_pressed('Esc'):
                state=False
        
        ret, frame = cap.read()
        if not ret: break
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_points = results.multi_face_landmarks[0].landmark
            num470x, num470y = mesh_points[eye].x*1920, mesh_points[eye].y*1080           #in case of left eye
            num472x, num472y = mesh_points[eye+2].x*1920, mesh_points[eye+2].y*1080       #in case of left eye

            num470x_ls.append(num470x)
            num470x_filtered = mean(num470x_ls)

            num470y_ls.append(num470y)
            num470y_filtered = mean(num470y_ls)

            if len(num470x_ls) == max_samples:
                num470x_ls.pop(0)
            if len(num470y_ls) == max_samples:
                num470y_ls.pop(0)
            if len(iridistmsmt_ls) == max_samples:
                iridistmsmt_ls.pop(0)

            iridist = ll(num470x, num470y, num472x, num472y)
            iridistmsmt_ls.append(iridist)
            iridist_filtered = mean(iridistmsmt_ls)
            
            #print (ir2z(iridist))

            V = (num470x_filtered, num470y_filtered, ir2z(iridist_filtered))
        #cv.imshow('image', frame)
        key = cv.waitKey(1)

        A1ap = ITOS(V, A1)
        A2ap = ITOS(V,A2)
        A3ap = ITOS(V,A3)
        A4ap = ITOS(V,A4)
        A5ap = ITOS(V,A5)
        A6ap = ITOS(V,A6)
        A7ap = ITOS(V,A7)
        A8ap = ITOS(V,A8)

        cls()
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

        
        pygame.display.update()
        clock.tick(60)


cap.release()
cv.destroyAllWindows()
pygame.quit()
quit()