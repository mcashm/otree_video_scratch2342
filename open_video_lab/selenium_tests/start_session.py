import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from api import call_api, GET, POST

def relative_to_absolute(rel):
    return f"http://localhost:8000{rel}"


def create_session(NUM_PARTICIPANTS=1, skip_cam_checks=False):
    window_handles = {}

    options = webdriver.ChromeOptions()    
    options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument(r'--use-file-for-fake-video-capture=d:\settings\mbath\Documents\My Videos\sample_video.mjpeg')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)

    #start session
    driver.get("http://localhost:8000")
    demo_link = driver.find_element(by=By.LINK_TEXT , value="Initial 8x8 jitsi test")
    demo_link.click()

    admin_report_href = driver.find_element(by=By.CSS_SELECTOR, value=".AdminReport").get_dom_attribute("href")

    window_handles['session_links'] = driver.current_window_handle


    #open admin_report in new tab
    driver.switch_to.new_window("tab")
    driver.get(relative_to_absolute(admin_report_href))
    #print(relative_to_absolute(admin_report_href))
    window_handles['admin_report'] = driver.current_window_handle

    #open the main experimenter's conference window
    driver.find_element(by=By.CSS_SELECTOR, value="#btnInit").click()
    window_handles['main_experimenter_conference'] = driver.window_handles[-1]


    driver.switch_to.window(window_handles['session_links'])

    session_code = driver.current_url.split(r"/").pop()

    if skip_cam_checks:
        print(f"session_code for api call: {session_code}")
        data = call_api(GET, 'sessions', session_code)
        #for p in data['participants']:
        #    call_api(POST, 'participant_vars', p['code'], vars={"cam_checked": 1})
        call_api(POST, 'participant_vars', data['participants'][0]['code'], vars={"cam_checked": 1})
       

    window_handles['participant_windows'] = []

    for i in range(NUM_PARTICIPANTS):
        time.sleep(5)
        ppt_link = driver.find_element(by=By.CSS_SELECTOR, value=f".participant-link:nth-of-type({i + 1})")
        ppt_link.click()
        window_handles['participant_windows'].append(driver.window_handles[-1])
        
    
    return (driver, window_handles)


if __name__ == "__main__":
    driver, window_handles  = create_session(NUM_PARTICIPANTS=1, skip_cam_checks=True)

    print(window_handles)

    time.sleep(30)

    driver.quit()
