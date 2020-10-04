import cv2
import numpy as np 
import matplotlib.pyplot as plt 
import json 

names = ["bhatsa.png","tansa.png","tulsi.png", "vihar.png","modaksagar.png","middleV.png","upperV.png"]
pixel_values = {}
for name in names:

	img = cv2.imread(name)
	h,w,d = img.shape

	if name == "vihar.png":
		img_crop = img[400:800,700:1200]
	else:
		img_crop = img[220:1500,220:1500]

	img_crop = cv2.resize(img_crop, (680,420))

	image_RGB = cv2.cvtColor(img_crop, cv2.COLOR_BGR2RGB)
	Gaussian = cv2.GaussianBlur(image_RGB, (7, 7), 0)

	median = cv2.medianBlur(Gaussian, 5)

	if name == "middleV.png" or name == "modaksagar.png":
		lower = np.array([5,5,5])
		upper = np.array([60,60,60])
	elif name == "bhatsa.png" or name == "tansa.png":
		lower = np.array([5,5,5])
		upper = np.array([71,71,60])
	else:
		lower = np.array([9,10,5])
		upper = np.array([45,60,60])

	mask = cv2.inRange(median,lower,upper)
	res = cv2.bitwise_and(median,median,mask=mask)

	pixels = 680*420
	black = pixels-cv2.countNonZero(mask)
	white = pixels-black
	pixel_values[name] = white

	cv2.imshow("mask",mask)
	cv2.imshow("res",res)
	cv2.imshow("crop", img_crop)
	cv2.imshow("hsv", median)
	cv2.imwrite("hsv.jpg", median)
	cv2.waitKey()
	cv2.destroyAllWindows()


#using the images 
zoom_6 = 1.64*10**-4
zoom_5 = 5.2*10**-4
zoom_3 = 2.7*10**-5

#Area of each lake = zoom number*white pixel
Bhatsa_A = zoom_6*pixel_values["bhatsa.png"]
tansa_A = zoom_5*pixel_values["tansa.png"]
middleV_A = zoom_5*pixel_values["middleV.png"]
modaksagar_A = zoom_5*pixel_values["modaksagar.png"]
tulsi_A = zoom_3*pixel_values["tulsi.png"]
upperV_A = zoom_6*pixel_values["upperV.png"]
vihar_A = zoom_5*pixel_values["vihar.png"]

area_of_river = {
		"Bhatsa": Bhatsa_A,
		"tansa" : tansa_A,
		"middleV" : middleV_A, 
		"modaksagar" : modaksagar_A, 
		"tulsi" : tulsi_A,
		"upperV" : upperV_A,
		"vihar" : vihar_A 
} 

with open("river_areas.json","w") as outfile:
	json.dump(area_of_river, outfile)
