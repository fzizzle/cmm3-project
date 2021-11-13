import tkinter as tk
from tkinter.filedialog import askopenfile
import os
from PIL import Image, ImageTk
import json
import pathlib

global root
root = tk.Tk()

# Global variables for toggle switch
on = ImageTk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "on.png"))
off = ImageTk.PhotoImage(file=os.path.join(
    os.path.dirname(__file__), "off.png"))
switch_is_on = True


class InputBox():
    """This takes every variable type and creates a label and a text box for it. //
    It also has methods to capture and store the data before running the simulation"""

    def __init__(self, column, row, label, data_type, toggle=False, column_span=1):
        self.column = column
        self.row = row
        self.label = label
        self.data_type = data_type
        self.toggle = toggle
        self.column_span = column_span

    def switch(self):
        # handles toggle button functionality
        global switch_is_on
        if switch_is_on:
            self.toggle.config(image=off)
            switch_is_on = False
            if self.label == 'Velocity Field':
                self.browse.destroy()
        else:
            self.toggle.config(image=on)
            switch_is_on = True
            if self.label == 'Velocity Field':
                self.browse = tk.Button(
                    root, text='Open File', command=lambda: self.open_file())
                self.browse.grid(
                    columnspan=1, column=self.column + 2, row=self.row)

    def open_file(self):
        self.file = askopenfile(mode='r', filetypes=[
                                ('velocity field', '*.dat')]).name
        if self.file is not None:
            self.file_path = str(pathlib.PurePath(str(self.file)))
            success_text = tk.Label(text="File Loaded!")
            success_text.grid(
                columnspan=10, column=self.column + 3, row=self.row)

    def place(self):
        # places the button in the GUI window
        input_label = tk.Label(root, text=self.label)
        input_label.grid(column=self.column, row=self.row)
        if self.toggle:
            self.toggle = tk.Button(root, image=on, bd=0, command=self.switch)
            self.toggle.grid(
                columnspan=1, column=self.column + 1, row=self.row)
            if self.label == 'Velocity Field':
                self.browse = tk.Button(
                    root, text='Open File', command=lambda: self.open_file())
                self.browse.grid(
                    columnspan=1, column=self.column + 2, row=self.row)
        else:
            self.input_box = tk.Entry(root)
            self.input_box.grid(column=self.column + 1, row=self.row)

    def get_input(self):
        # Takes the input from the entry box and returns it.
        if self.toggle and switch_is_on:
            return True
        elif self.toggle and not switch_is_on:
            return False
        elif self.data_type == 'integer':
            data = self.input_box.get()
            return int(data)
        else:
            data = self.input_box.get()
            return float(data)


class Task():
    """Manages each tasks landing page and inputs."""

    def __init__(self, task, row, column_span=10):
        self.task = task
        self.row = row
        self.label = "Task " + (self.task)
        self.column_span = column_span

    def go_to_task(self):
        # Clears elements on the page and replaces them with task appropriate elements.
        for widgets in root.winfo_children():
            widgets.destroy()
        canvas = tk.Canvas(root, height=500, width=800)
        canvas.grid(columnspan=10, rowspan=10)
        place_logo()
        header = tk.Label(text=self.label)
        header.grid(columnspan=10, column=0, row=1)
        instructions = tk.Label(
            text="Define your variables before running the script.")
        instructions.grid(columnspan=10, column=0, row=2)
        self.inputs, self.input_dict = place_input_boxes(self.label)
        btn_run = tk.Button(root, text="Run Simulation", padx=10,
                            pady=10, fg="black", bg="pink", command=self.run)
        btn_run.grid(columnspan=10, column=0, row=9, sticky=tk.W+tk.E)
        btn_back = tk.Button(root, text="Back to Homepage",
                             padx=10, pady=10, fg="black", bg="pink", command=back)
        btn_back.grid(columnspan=10, column=0, row=10, sticky=tk.W+tk.E)

    def run(self):
        # Handles activity of the Run Button, stores user inputs in a data.json before running script.
        dict = self.input_dict
        for input in self.inputs:
            value = input.get_input()
            label = input.label
            dict[label][2] = value
        for input_box in self.inputs:
            if input_box.label == 'Velocity Field' and input_box.file is not None:
                print('working')
                dict['Velocity Field'][2] = True
                dict['File Path'][2] = input_box.file_path
                break
        # Storing inputs in JSON File.
        with open(os.path.join(os.path.dirname(__file__), 'input_boxes.json')) as json_file:
            dictionary = json.load(json_file)
        dictionary[self.label] = dict
        with open(os.path.join(os.path.dirname(__file__), 'input_boxes.json'), 'w') as json_file:
            json.dump(dictionary, json_file, indent=4)
        for widgets in root.winfo_children():
            widgets.destroy()
        # TODO replace this with each tasks function.

    def place_button(self):
        # Places the task button on the main landing page
        btn = tk.Button(root, text=str(self.label), padx=10,
                        pady=10, fg="black", bg="pink", command=self.go_to_task)
        btn.grid(columnspan=10, column=0, row=self.row, sticky=tk.W+tk.E)


def init_buttons(list):
    # Takes a list and element type (Input Box or Button) and generates the element using the respective class
    tasks = ["A", "B", "C", "D", "E"]
    row_num = 2
    for task in tasks:
        element = Task(task, row_num)
        list.append(element)
        element.place_button()
        row_num += 1


def place_input_boxes(task_label):
    # Reads input boxes file, then checks for toggle or input box. Places input boxes/toggles.
    row_num = 3
    boxes = []
    with open(os.path.join(os.path.dirname(__file__), 'input_boxes.json')) as json_file:
        dictionary = json.load(json_file)
    task_dict = dictionary[task_label]
    for key in task_dict:
        if task_dict[key][0] == "toggle":
            element = InputBox(4, row_num, key, task_dict[key][0], toggle=True)
        elif key == "File Path":
            pass
        else:
            element = InputBox(4, row_num, key, task_dict[key][0])
        boxes.append(element)
        element.place()
        row_num += 1
    return boxes, task_dict


def back():
    # Handles the activity of the back button
    for widgets in root.winfo_children():
        widgets.destroy()
    main(root)


def open_file():
    file = askopenfile(mode='r', filetypes=[('velocity field', '*.dat')])
    if file is not None:
        success_text = tk.Label(text="File Loaded!")
        success_text.grid(columnspan=10, column=7, row=5)
        content = file.read()
        with open('velocityfield.dat', 'w') as data:
            data.write(content)


def place_logo():
    # places logo and instructions for the gui
    logo = Image.open(os.path.join(os.path.dirname(__file__), 'logo.png'))
    logo = ImageTk.PhotoImage(logo, master=root)
    logo_label = tk.Label(image=logo, master=root)
    logo_label.image = logo
    logo_label.grid(columnspan=10, column=0, row=0)


def main(root):
    # Generates the landing page.
    canvas = tk.Canvas(root, height=500, width=900)
    canvas.grid(columnspan=10, rowspan=10)
    place_logo()
    instructions = tk.Label(text="Choose the task you wish to run.")
    instructions.grid(columnspan=10, column=0, row=1)
    buttons = []
    init_buttons(buttons)
    root.mainloop()


if __name__ == "__main__":
    main(root)
