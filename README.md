# Face-Detection

# Libraries for Menu
 - tkinter
 - pyautogui

# Libraries for Face Recognition
 - cv2
 - face_recognition
 - Image
 - os
 - glob

# Libraries for Face Detection
 - cv2

# Requirements

To run the code you need to create two folders separately. 

 1) images
	- Put images that you want to find the face from the image.
 2) training_set
	- Put person images that you want to see his/her name when the cam sees the same person.
	Note! : Image name should the image owner's name 

# How it works

 When you run the source code successfully, you will see a window that has four buttons which are Image, Camera, Add New Face, and Face Detection. 
 
 
 1)Image Button
 
	 When you click the Image button, it will ask you for an Image Name. This post looks inside the 'images' folder so you need to write the image name that is inside the 'images' folder. 
	 If the image that the user entered exists, it will detect the faces in the image and it will print the name of the person it knows the person. Otherwise, it will just print “unknown”. 
	 
 2) Camera
 
	When you click the Camera button, it opens your webcam and detects faces from the cam. If it knows the faces it will print their names as well. Otherwise, it will print “unknown”. will print unknown.	 
 
 3) Add New Face
 
	 Add New Face button is for collecting data. When you click that button, it will ask you to enter the full name. You need to enter the data owner's full name. 
	 After entering the full name, the webcam will be open automatically, it will wait for a command to take a picture. To take the picture you need to press 'q'.

4) Face Detection 

	Opens the webcam and shows the person's face and eyes. Also, it detects a person's smile. (Using haarcascade)