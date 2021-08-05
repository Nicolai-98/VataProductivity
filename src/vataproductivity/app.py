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
from toga.style.pack import CENTER, COLUMN, ROW
import os
import sqlite3
import datetime


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
        data = c.fetchall()
        print("Activities fetched: {0}".format(data))
        self.activity_table.data = None
        for row in data:
            seconds = float(row[1])
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            self.activity_table.data.append(row[0], "{:.1f} hours, {:.2f} minutes, {:.2f} seconds".format(h, m, s))
        conn.close()
        
    def save_activities(self, widget):
        if(self.current_activity == '' or None):
            self.main_window.error_dialog('Impossible', 'No activity selected')
            return
        difference = datetime.datetime.now() - self.activity_start_time
        difference_seconds = difference.total_seconds()
        package_dir = os.path.abspath(os.path.dirname(__file__))
        db_dir = os.path.join(package_dir, 'task.db')
        conn = sqlite3.connect(db_dir)
        c = conn.cursor()
        c.execute("SELECT time FROM tasks WHERE name='{0}'".format(self.current_activity))
        print("New time added {0} to {1}".format(difference_seconds, self.current_activity))
        difference_seconds += float(c.fetchone()[0])
        print("Total time {0}".format(difference_seconds))
        c.execute("UPDATE tasks SET time ={0} WHERE name='{1}'".format(difference_seconds, self.current_activity))
        conn.commit()
        self.activity_start_time = None;
        self.current_activity = None;
        c.execute("SELECT * FROM tasks")
        data = c.fetchall()
        print("Activities fetched: {0}".format(data))
        self.activity_table.data = None
        for row in data:
            seconds = float(row[1])
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            self.activity_table.data.append(row[0], "{:.1f} hours, {:.2f} minutes, {:.2f} seconds".format(h, m, s))
        conn.close()
        
    def set_active(self, table, row):
        self.activity_start_time = datetime.datetime.now()
        self.current_activity = row.name
        

    def startup(self):
        self.activity_start_time = datetime.datetime.now()
        self.current_activity = ''
        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            'Activity name:',
            style=Pack(padding_top=3)
        )
        
        self.name_input = toga.TextInput(style=Pack(padding_top=1, padding_right=2,flex=1))
        
        add_activity_button = toga.Button(
            'Add activity',
            on_press=self.save_activity
        )

        name_box = toga.Box(style=Pack(direction=ROW, padding=(5)))
        name_box.add(name_label)
        name_box.add(self.name_input)
        name_box.add(add_activity_button)
        
        self.activity_table = toga.Table(
            ['Name', 'Time spent'],
            missing_value = 'Not available',
            on_select=self.set_active,
            style=Pack(padding=5)
            )
        self.activity_table.MIN_HEIGHT=250
        
        get_activities_button = toga.Button(
            'See all activities',
            on_press=self.get_activities,
            style=Pack(padding=5)
        )
        
        save_activities_button = toga.Button(
            'Update time and save',
            on_press=self.save_activities,
            style=Pack(padding=5)
        )
        
        info_label = toga.Label(
            'Please select an activity to track your time by clicking on it (Marked blue when active):',
            style=Pack(padding_top=3)
        )
        
        main_box.add(name_box)
        main_box.add(get_activities_button)
        main_box.add(info_label)
        main_box.add(self.activity_table)
        main_box.add(save_activities_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return VataProductivity()
