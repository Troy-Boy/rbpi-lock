from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class CodeInputApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="Enter Your Reservation Code:", font_size='24sp')
        self.text_input = TextInput(font_size='24sp', multiline=False)
        submit_button = Button(text="Submit", font_size='24sp', on_press=self.submit_code)
        layout.add_widget(self.label)
        layout.add_widget(self.text_input)
        layout.add_widget(submit_button)
        return layout

    def submit_code(self, instance):
        code = self.text_input.text
        if self.validate_code(code):
            self.label.text = "Code accepted. Unlocking..."
            self.unlock_mechanism()
        else:
            self.label.text = "Invalid code. Please try again."

    def validate_code(self, code):
        # Implement your code validation logic here
        return True  # Replace with actual validation

    def unlock_mechanism(self):
        # Implement the mechanism to unlock the kayak/boat
        pass

if __name__ == '__main__':
    CodeInputApp().run()
