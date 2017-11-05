import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tkinter import *
import requests
from tkinter import messagebox

root=Tk()
root.minsize(width=400, height=300)

def download_and_save(url,songname):
	print(url,songname)
	r = requests.get(url, stream=True)
	filenme=songname+'.mp4'
	with open(filenme, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=1024):
			fd.write(chunk)
		fd.close()
	print("Check the folder where you are runnning the script for the mp4 file.")
	return 0

def download_mp3(url,songname):
	r = requests.get(url, stream=True)
	filenme=songname+'.mp3'
	total_size = int(r.headers['Content-Length'])/1024
	progress=0
	download_frame=Frame(root)
	download_frame.pack(anchor="s")
	var = StringVar()
	var.set("Size remaining: ")
	pbar = Label(download_frame, textvariable = var)
	pbar.pack(side="bottom")
	with open(filenme, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=1024*100):
			progress+=100
			if total_size-progress<0:
				var.set("File downloaded")
			else:
				var.set("Size remaining: "+str(total_size-progress))
			root.update()
			fd.write(chunk)
		fd.close()
	print("Check the folder where you are runnning the script for the mp3 file.")
	return 0

def close_window():
	exit()

def download(SONG_NAME):
	# THIS SCRIPT USES SELENIUM 2.53.6 AND PHANTOMJS 2.1.1
	print(SONG_NAME)
	if SONG_NAME=="":
		empty_name = Label(frame,text="No video name entered")
		empty_name.pack()
		return 0
	download_frame=Frame(root,bg='yellow')
	download_frame.pack(anchor='center')
	driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])

	URL = "https://www.youtube.com/results?search_query="+SONG_NAME
	#driver = webdriver.PhantomJS()
	driver.get(URL)#driver navigates to the youtube url
	print(driver.current_url)
	driver.find_element_by_xpath("//a[@class='yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink      spf-link ']").click()
	WATCH_URL = driver.current_url
	print(WATCH_URL)
	driver.close()
	# FOR MP3 DOWNLOADER
	driver1 = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
	#driver1 = webdriver.PhantomJS()
	WATCH_URL_list=list(WATCH_URL)
	WATCH_URL_list.insert(12,'ss')
	WATCH_URL=''.join(WATCH_URL_list)
	driver1.get(WATCH_URL)
	wait = WebDriverWait(driver1, 10000)
	dnld_xpath = "//div[@class='def-btn-name']"
	more_xpath ="//a[contains(.,'More')]"
	dnldbtn = wait.until(EC.element_to_be_clickable((
    By.XPATH, dnld_xpath)))
	dnldbtn.click()
	more_btn = wait.until(EC.element_to_be_clickable((
    By.XPATH, more_xpath)))
	more_btn.click()
	#arrow = driver.find_element_by_xpath("//div[@class='def-btn-name']").click()
	d_720 = driver1.find_element_by_xpath("//a[contains(.,'MP4 720')]").get_attribute('href')
	d_360 = driver1.find_element_by_xpath("//a[contains(.,'MP4 360')]").get_attribute('href')
	mp3url = driver1.find_element_by_xpath("//a[contains(.,'Audio M4A 128')]").get_attribute('href')
	d_720p=Button(download_frame,text="Download 720p",command= lambda:download_and_save(d_720,SONG_NAME))
	d_720p.pack()
	d_360p=Button(download_frame,text="Download 360p",command= lambda:download_and_save(d_360,SONG_NAME))
	d_360p.pack()
	d_mp3=Button(download_frame,text="Download MP3",command= lambda:download_mp3(mp3url,SONG_NAME))
	d_mp3.pack()
	close_button = Button(frame,text="Close",command=close_window)
	close_button.pack(side="bottom")
	driver1.close()
	
	
frame=Frame(root,bg='black')
frame.pack(anchor='center',ipady=10)
slabel = Label(frame,text="Enter the song video name below")
slabel.pack()
songname = StringVar()
sname_input = Entry(frame,textvariable=songname)
sname_input.pack()
submit = Button(frame,text="Download",command=lambda : download('+'.join(songname.get().split(" "))))
submit.pack()
root.mainloop()
