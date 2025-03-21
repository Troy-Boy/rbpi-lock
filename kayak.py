from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
import requests
import threading
from datetime import datetime, timezone
from api import API

class KayakApp(App):
	def __init__(self, api: API, boat_id: str, **kwargs):
		super(KayakApp, self).__init__(**kwargs)
		self.api = api
		self.boat_id = boat_id

	def build(self):
		sm = ScreenManager()
		sm.add_widget(WelcomeScreen(name="welcome"))
		sm.add_widget(LockerNumberScreen(name="locker_number"))

		# ✅ Manually add CodeEntryScreen with API and Boat ID
		sm.add_widget(CodeEntryScreen(api=self.api, boat_id=self.boat_id, name="code_entry"))

		sm.add_widget(ProcessingScreen(name="processing"))
		sm.add_widget(ResultScreen(name="result"))

		return sm


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
	def __init__(self, api: API, boat_id: str, **kwargs):
		super().__init__(**kwargs)
		self.api = api
		self.boat_id = boat_id
		self.code = ''
		self.locker_number = ''
		self.utc_time = self.get_current_utc_time()
		self.debug_logs = ''

	def validate_code(self):
		"""Handles the reservation code validation process."""
		if not self.code:
			self.ids.error_message.text = "Please enter your reservation code."
			return

		self.manager.current = "processing"  # Switch to Processing Screen

		# Simulate API call delay
		Clock.schedule_once(lambda dt: self.check_api_response(), 1)

	def check_api_response(self):
		"""Performs the API call and updates UI based on the response."""
		response = self.api.verify_access_code(self.code, self.boat_id)
		print(self.code, self.locker_number)
		result_screen = self.manager.get_screen("result")  # Get ResultScreen

		# Access UI elements from `.kv` file and update them
		result_label = result_screen.ids.result_label
		retry_button = result_screen.ids.retry_button

		if response["success"]:
			self.unlock_locker()
			result_label.text = "Access Granted! Locker Unlocked."
			result_label.color = (0, 1, 0, 1)  # Green text
			retry_button.opacity = 0  # Hide retry button
			retry_button.disabled = True
		else:
			self.unlock_locker()
			error_message = response.get("error", "Unknown error occurred.")
			result_label.text = f"❌ Access Denied! {error_message}"
			result_label.color = (1, 0, 0, 1)  # Red text
			retry_button.opacity = 1  # Show retry button
			retry_button.disabled = False

		self.manager.current = "result"  # Switch to result screen

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
