"""
Productivity app for dynamic minds.
TODO field to add new tasks
TODO show current task with timer
TODO next button to go to next task (better drop down)
TODO Overview with tasks + time spent
TODO Setup DB on startup if not already set up
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import sqlite3


class VataProductivity(toga.App):

    def save_activity(self, widget):
        name = self.name_input.value
        print("Activity name: "+name)
        package_dir = os.path.abspath(os.path.dirname(__file__))
        print("Package dir: " +package_dir)
        db_dir = os.path.join(package_dir, 'task.db')
        print("Db dir: " +db_dir)
        conn = sqlite3.connect(db_dir)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO tasks VALUES ('{0}', 0)".format(name))
        c.execute("SELECT * FROM tasks where name='{0}'".format(name))
        conn.commit()
        print("Activity stored in db {0}: ".format(c.fetchone()))
        conn.close()
        
        
    def get_activities(self, widget):
        package_dir = os.path.abspath(os.path.dirname(__file__))
        db_dir = os.path.join(package_dir, 'task.db')
        conn = sqlite3.connect(db_dir)
        c = conn.cursor()
        c.execute("SELECT * FROM tasks")
        print("Activities fetched: {0}".format(c.fetchall()))
        self.activity_label.text = "{0}".format(c.fetchall())
        conn.close()
        

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))
        
        self.activity_label = toga.Label(
            'Activities name:',
            style=Pack(padding=(0, 5))
        )

        name_label = toga.Label(
            'Activity name:',
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        add_activity_button = toga.Button(
            'Add new activity',
            on_press=self.save_activity,
            style=Pack(padding=5)
        )
        
        get_activities_button = toga.Button(
            'See all activities',
            on_press=self.get_activities,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(add_activity_button)
        main_box.add(get_activities_button)
        main_box.add(self.activity_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return VataProductivity()
