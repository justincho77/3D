# 3D

## How to run
1. place all three .py files in the same folder on your device.
2. Run the camcal.py file, and follow the instructions to calibrate the tracking software to your camera setup. Make sure your camera's view is close to perpendicular with your screen for maximum accuracy.
3. Enter the information required to the console window that shows up.
4. After calibration, the file with the calibration data will be made.
5. Run the 3D.py file
6. Wait for the window with the cube to show up. The window may not show on the  top, so please check the taskbar.
7. Close one of your eyes to make it look more real.
8. You can close the window by pressing ESC.

## Controls
This program allows the user to move the cube around in the simulated space using intuitive controls. You can:

Use the wasd keys to move the cube front to back and right to left.
Use ctrl and shift to move the cube up and down.

## How it works
This program uses the mediapipe and opencv library to track the user's eyes and measure the x,y,z coordinates. The coordinates are then used to calcultate what points on the display are going to look identical to what points in space. The results are going to be calculated for each of the eight points of a cube which is shown on screen.

## Downloads
-Download exe file from here: https://drive.google.com/u/0/uc?id=19OfKPzXXfXpw-ymoI-PKIASlqpdydD6H&export=download
(this exe file is outdated. please use the py files for maximum performance.)
