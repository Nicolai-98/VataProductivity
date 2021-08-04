"""
Productivity app for dynamic minds.
TODO field to add new tasks
TODO show current task with timer
TODO next button to go to next task (better drop down)
TODO Overview with tasks + time spent
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class VataProductivity(toga.App):

    def save_activity(self, widget):
        print("Hello, ", self.name_input.value)

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            'Your name:',
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            'Say Hello!',
            on_press=self.save_activity,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return VataProductivity()
