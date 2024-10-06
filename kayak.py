from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import requests
import threading

# Define your screens
class WelcomeScreen(Screen):
    pass

class LockerNumberScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locker_number = ''

    def add_digit(self, digit):
        self.locker_number += str(digit)
        self.ids.locker_input.text = self.locker_number

    def clear_input(self):
        self.locker_number = ''
        self.ids.locker_input.text = ''

    def proceed_to_code(self):
        if self.locker_number:
            self.manager.current = 'code_entry'
            self.manager.get_screen('code_entry').locker_number = self.locker_number
        else:
            self.ids.error_message.text = 'Please enter a locker number.'

class CodeEntryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = ''
        self.locker_number = ''

    def add_digit(self, digit):
        self.code += str(digit)
        self.ids.code_input.text = self.code

    def clear_input(self):
        self.code = ''
        self.ids.code_input.text = ''

    def submit_code(self):
        if self.code:
            self.manager.current = 'processing'
            threading.Thread(target=self.validate_code).start()
        else:
            self.ids.error_message.text = 'Please enter your reservation code.'

    def validate_code(self):
        # Replace with your actual API endpoint and parameters
        url = 'https://your-reservation-system.com/api/validate'
        payload = {
            'locker_number': self.locker_number,
            'code': self.code
        }
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            if result.get('valid'):
                # Unlock the locker
                self.unlock_locker()
                self.manager.get_screen('result').ids.result_message.text = 'Locker unlocked successfully!'
            else:
                self.manager.get_screen('result').ids.result_message.text = 'Invalid code or locker number.'
        except Exception as e:
            self.manager.get_screen('result').ids.result_message.text = 'Network error. Please try again.'
        finally:
            self.manager.current = 'result'

    def unlock_locker(self):
        # Implement GPIO control to unlock the locker
        pass

class ProcessingScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class KayakApp(App):
    def build(self):
        return Builder.load_file('kayak.kv')

if __name__ == '__main__':
    KayakApp().run()
