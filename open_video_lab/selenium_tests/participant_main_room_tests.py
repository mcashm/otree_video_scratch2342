import unittest
import time

from start_session import create_session, relative_to_absolute
from utils import switch_to_top_level_content, switch_to_experiment_iframe, switch_to_meeting_iframe


from selenium import webdriver
from selenium.webdriver.common.by import By
import feature_tests_general

class TestParticipantMainRoomBehaviour(unittest.TestCase):
    
    driver = None
    window_handles = {}

    @classmethod
    def setUpClass(cls):
        cls.driver, cls.window_handles = create_session(skip_cam_checks=True)
        time.sleep(15)
        cls.driver.switch_to.window(cls.window_handles['participant_windows'][0])

    def setUp(self):
        switch_to_meeting_iframe(self.driver, self.window_handles)
        self.assertTrue(feature_tests_general.is_in_main_room(self.driver))

    def test_in_main_room(self):
        self.assertTrue(feature_tests_general.is_in_main_room(self.driver))

    def test_cam_not_disabled(self):
        self.assertTrue(feature_tests_general.video_usable(self.driver))

    def test_cant_toggle_mic(self):
        self.assertTrue(feature_tests_general.audio_muted(self.driver))
        feature_tests_general.change_mic_mute_state(self.driver)
        time.sleep(5) #give the system 5 seconds to respond and remute if it's going to
        self.assertTrue(feature_tests_general.audio_muted(self.driver))

    def test_mic_muted(self):
        self.assertTrue(feature_tests_general.audio_muted(self.driver))

    def test_cam_toggle_works(self):
        initial_mute_state = feature_tests_general.video_muted(self.driver)
        feature_tests_general.change_cam_mute_state(self.driver)
        time.sleep(5) #give the system 5 seconds to respond and remute if it's going to
        self.assertTrue(initial_mute_state != feature_tests_general.video_muted(self.driver))
        

    def tearDown(self):
        switch_to_top_level_content(self.driver, self.window_handles)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()    


if __name__ == "__main__":
    unittest.main()
