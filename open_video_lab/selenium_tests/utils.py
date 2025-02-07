from selenium import webdriver
from selenium.webdriver.common.by import By

def switch_to_top_level_content(driver, window_handles):
    #probably should do a check to make sure we're in an appropriate window
    driver.switch_to.default_content()

def switch_to_experiment_iframe(driver, window_handles):
    switch_to_top_level_content(driver, window_handles)
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe#experiment_containter")
    driver.switch_to.frame(iframe)

def switch_to_meeting_iframe(driver, window_handles):
    switch_to_top_level_content(driver, window_handles)
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe#jitsiConferenceFrame0")
    driver.switch_to.frame(iframe)
