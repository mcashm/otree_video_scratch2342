from start_session import create_session, relative_to_absolute
from utils import switch_to_top_level_content, switch_to_experiment_iframe, switch_to_meeting_iframe

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def video_works_in_main_room(driver, window_handles):
    pass


def get_room_name(driver):
    return driver.find_element(by=By.CSS_SELECTOR, value=".subject-text--content").text

def is_in_main_room(driver):
    return "Session" in get_room_name(driver)   

def is_in_breakout_room(driver):
    return "Participant" in get_room_name(driver)

def get_video_button(driver):
    return driver.find_element(by=By.CSS_SELECTOR, value=".video-preview .toolbox-icon")

def video_usable(driver):
    return "disabled" not in get_video_button(driver).get_attribute("class")

def video_muted(driver):
    video_button = get_video_button(driver)
    return "toggled" in video_button.get_attribute("class") #toggled is muted, lack of toggled is unmuted

def get_audio_button(driver):
    return driver.find_element(by=By.CSS_SELECTOR, value=".audio-preview .toolbox-icon")

def audio_usable(driver):
    mic_button = get_audio_button(driver)
    return "disabled" not in mic_button.get_attribute("class")

def audio_muted(driver):
    audio_button = get_audio_button(driver)
    print(audio_button)
    return "toggled" in audio_button.get_attribute("class") #toggled is muted, lack of toggled is unmuted
    

#def audio_muted_in_main_room(driver, window_handles):
#    if not is_in_main_room(driver, window_handles):
#      raise RuntimeError("Meeting participant not in main room")
#    return audio_muted(driver, window_handles)
    
#def audio_automatically_remutes_in_main_room(driver, window_handles):
#    pass
    
def change_mic_mute_state(driver):
    audio_button = get_audio_button(driver)
    audio_button.click()

def change_cam_mute_state(driver):
    video_button = get_video_button(driver)
    video_button.click()

#def can_self_mute(driver):
#    audio_button = get_audio_button(driver)
#    audio_button.click() 
#    time.sleep(5) #give the system 5 seconds to respond and remute if it's going to
#    return audio_muted(driver)

#def can_self_unmute_in_side_room(driver)
#    audio_button = get_audio_button(driver)
#    audio_button.click() 
#    time.sleep(5) #give the system 5 seconds to respond and remute if it's going to
#    return not audio_muted(driver)


def jitsi_raise_hand_button_hidden(driver, window_handles):
    pass

def jitsi_no_chat_to_everyone(driver, window_handles):
    pass

def jitsi_no_private_chat_among_participants(driver, window_handles):
    pass

def participant_numbers_as_display_names(driver, window_handles):
    pass

def no_mod_powers_for_participants(driver, window_handles):
    pass

def mod_powers_for_experimenters(driver, window_handles):
    pass

def create_and_move_to_breakout_room(driver, window_handles):
    pass


if __name__ == "__main__":
    driver, window_handles  = create_session()

    print(window_handles)

    time.sleep(15)
    driver.switch_to.window(window_handles['participant_windows'][0])

    switch_to_meeting_iframe(driver, window_handles)

    assert is_in_breakout_room(driver)
    assert video_usable(driver)
    assert audio_usable(driver)
    assert not audio_muted(driver)


    time.sleep(30)
    driver.quit()
