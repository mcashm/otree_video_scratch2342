import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def relative_to_absolute(rel):
    return f"http://localhost:8000{rel}"

NUM_PARTICIPANTS = 1
window_handles = {}




options = webdriver.ChromeOptions()    
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
options.add_argument(r'--use-file-for-fake-video-capture=d:\settings\mbath\Documents\My Videos\sample_video.mjpeg')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)


#start session
driver.get("http://webcamtests.com")

time.sleep(30)

driver.quit()
