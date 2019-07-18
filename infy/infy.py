#!/usr/bin/env python3
import os
from pkg_resources import resource_filename

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.properties import ListProperty, StringProperty
from plyer import filechooser

from . import grammar
from . import Evaluator


class FileChooseButton(Button):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''

    selection = ListProperty([])

    def on_press(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection


class LoadButton(FileChooseButton):
    def on_selection(self, *a, **k):
        app = App.get_running_app()
        app.load(self.selection[0])


class SaveButton(FileChooseButton):
    def on_press(self):
        app = App.get_running_app()
        if app.filepath is not None:
            super(FileChooseButton, self).on_press()
        else:
            app.save(app.filepath)

    def on_selection(self, *a, **k):
        app = App.get_running_app()
        app.save(self.selection[0])


class TypeInput(CodeInput):
    def on_cursor(self, a, b):
        # fixes kivy not scrolling down when you add a new row to the bottom
        super(CodeInput, self).on_cursor(a, b)
        if self.cursor_row == len(self._lines) - 1:
            app = App.get_running_app()
            app.root.scrlv.scroll_y = 0


class InfyApp(App):
    filepath = None
    load_icon = StringProperty()
    save_icon = StringProperty()
    white_bg = StringProperty()

    def build(self):
        self.icon = resource_filename(__name__, 'assets/lean.svg')
        self.load_icon = resource_filename(__name__, 'assets/folder.png')
        self.save_icon = resource_filename(__name__, 'assets/save.png')
        self.white_bg = resource_filename(__name__, 'assets/white.png')

    def load(self, filepath):
        with open(filepath) as stream:
            self.root.textarea.text = stream.read()
        self.filepath = filepath
        self.title = 'Infy - ' + os.path.basename(self.filepath)

    def save(self, filepath):
        print('saving', filepath, self.root.textarea.text)
        with open(filepath, 'w') as stream:
            stream.write(self.root.textarea.text)
        self.filepath = filepath
        self.title = 'Infy - ' + os.path.basename(self.filepath)

    def text_changed(self, txt):
        results_area = self.root.resultsarea
        doc = grammar.parse(txt)
        results = evaluator.eval(doc)
        results_text = ""
        for i, result in enumerate(results):
            if i > 0:
                results_text += "\n"
            if result is None:
                continue
            if result.__class__.__name__ == 'Quantity':
                result = result.magnitude
            if int(result) == float(result):
                result = int(result)  # avoid .0 on results
            else:
                result = round(result, 2)
            results_text += str(result)
        results_area.text = results_text


def run():
    InfyApp().run()


evaluator = Evaluator()
