from selenium import webdriver 
import time
from time import sleep 
import pyautogui
driver = webdriver.Chrome(r"E:\\NASA Hackathon\\chromedriver_win32\\chromedriver")


def coordinates(lati, longi):
	lati_str = str(lati)
	lati_str = lati_str+"° N"
	longi_str = str(longi)
	longi_str = longi_str+"° E"
	coordinates = lati_str+","+longi_str
	return coordinates

driver.get("https://zoom.earth")
searchbar = driver.find_element_by_xpath("/html/body/main/div[5]/form/input[1]")
searchbutton = driver.find_element_by_xpath("/html/body/main/div[5]/form/input[2]")
zoomoutbutton = driver.find_element_by_xpath("/html/body/main/button[5]")
optionsbutton = driver.find_element_by_xpath("/html/body/main/button[3]")
labelsbutton = driver.find_element_by_xpath("/html/body/main/div[6]/form/div[1]/label")
refreshlink = driver.find_element_by_xpath("/html/body/main/article[1]/header")

optionsbutton.click()
time.sleep(1)
labelsbutton.click()
time.sleep(1)

def take_screenshot(lati, longi,zoom):
	searchbar.send_keys(coordinates(lati,longi))
	searchbutton.click()
	time.sleep(1)

	for i in range(0,zoom):
		zoomoutbutton.click()
		time.sleep(1)

	driver.fullscreen_window()
	time.sleep(1)
	return pyautogui.screenshot()

bhatsa = take_screenshot(19.5132,73.4176,6)
bhatsa.save(r"E:\\NASA Hackathon\\bhatsa.png")

searchbar.clear()
time.sleep(5)

tansa = take_screenshot(19.5682,73.2677,5)
tansa.save(r"E:\\NASA Hackathon\\tansa.png")

searchbar.clear()
time.sleep(5)

tulsi = take_screenshot(19.1910,72.9180,3)
tulsi.save(r"E:\\NASA Hackathon\\tulsi.png")

searchbar.clear()
time.sleep(5)

vihar = take_screenshot(19.1540,72.9077,5)
vihar.save(r"E:\\NASA Hackathon\\vihar.png")

searchbar.clear()
time.sleep(5)

modaksagar = take_screenshot(19.6732,73.2957,5)
modaksagar.save(r"E:\\NASA Hackathon\\modaksagar.png")

searchbar.clear()
time.sleep(5)

middleV = take_screenshot(19.7051,73.4338,5)
middleV.save(r"E:\\NASA Hackathon\\middleV.png")

searchbar.clear()
time.sleep(5)

upperV = take_screenshot(19.8143,73.542,6)
upperV.save(r"E:\\NASA Hackathon\\upperV.png")