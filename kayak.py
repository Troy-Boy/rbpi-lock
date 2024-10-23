from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
import requests
import threading
from datetime import datetime, timezone
from api import API

class KayakApp(App):
	def __init__(self, api, boat_id, **kwargs):
		super(KayakApp, self).__init__(**kwargs)
		self.api = api
		self.boat_id = boat_id

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
			code_entry_screen = self.manager.get_screen('code_entry')
			code_entry_screen.locker_number = self.locker_number
			# Update the banner text
			code_entry_screen.ids.banner_label.text = code_entry_screen.get_banner_text()
			self.manager.current = 'code_entry'
		else:
			self.ids.error_message.text = 'Please enter a locker number.'

class CodeEntryScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.api = App.get_running_app().api
		self.boat_id = App.get_running_app().boat_id
		self.code = ''
		self.locker_number = ''
		self.utc_time = self.get_current_utc_time()
		self.debug_logs = ''

	def get_current_utc_time(self):
		"""Get the current UTC time as a formatted string."""
		return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

	def add_digit(self, digit):
		self.code += str(digit)
		self.ids.code_input.text = self.code

	def clear_input(self):
		self.code = ''
		self.ids.code_input.text = ''

	def on_pre_enter(self):
	# Update the banner when the screen is about to be displayed
		self.utc_time = self.get_current_utc_time()
		self.ids.banner_label.text = self.get_banner_text()

	def on_enter(self):
		# Schedule the time update every second
		self.time_event = Clock.schedule_interval(self.update_time, 1)

	def on_leave(self):
		# Cancel the scheduled event
		Clock.unschedule(self.time_event)

	def update_time(self, dt):
		self.utc_time = self.get_current_utc_time()
		self.ids.banner_label.text = self.get_banner_text()

	def submit_code(self):
		if self.code:
			threading.Thread(target=self.validate_code).start()
		else:
			self.ids.error_message.text = 'Please enter your reservation code.'

	def validate_code(self):
		# Replace with your actual API endpoint and parameters
		if self.code:
			payload = {
				'locker_number': self.locker_number,
				'code': self.code
			}
			try:
				# response = api.verify_access_code(self.code, self.boat_id, json=payload)
				# result = response.json()
				print(self.api)
				if self.api:
					# Unlock the locker
					self.unlock_locker()
					self.manager.get_screen('result').ids.result_message.text = 'Locker unlocked successfully!'
				else:
					self.manager.get_screen('result').ids.result_message.text = 'Invalid code or locker number.'
				self.update_debug_logs("API call successful: DONE !")
			except Exception as e:
				print(e)
				self.manager.get_screen('result').ids.result_message.text = 'Network error. Please try again.'
				self.update_debug_logs(f"API call failed: {e}")
			finally:
				self.manager.current = 'result'
		else:
			self.ids.error_message.text = 'Please enter your reservation code.'

	def unlock_locker(self):
		# Implement GPIO control to unlock the locker
		pass

	def update_debug_logs(self, log_message):
		# Update the debug logs and refresh the banner
		self.debug_logs += f"{log_message}\n"
		self.utc_time = self.get_current_utc_time()
		# Update the banner text on the main thread
		self.ids.banner_label.text = self.get_banner_text()
		Clock.schedule_once(lambda dt: setattr(self.ids.banner_label, 'text', self.get_banner_text()))

	def get_banner_text(self):
		return (
			f"[b]Boat ID:[/b] {self.boat_id}    [b]Locker:[/b] {self.locker_number}    [b]Time:[/b] {self.utc_time}\n"
			f"{self.debug_logs}"
		)

class ProcessingScreen(Screen):
	pass

class ResultScreen(Screen):
	pass

if __name__ == '__main__':
	KayakApp().run()
