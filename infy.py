import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.config import Config
from kivy.properties import ObjectProperty, ListProperty
from plyer import filechooser

from grammar import grammar
from evaluator import Evaluator

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')


class Line(Widget):
    pass


class LoadButton(Button):
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

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        app = App.get_running_app()
        app.load(self.selection[0])


class SaveButton(Button):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''

    selection = ListProperty([])

    def on_press(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        app = App.get_running_app()
        if app.filepath:
            app.save(app.filepath)
        else:
            filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        app = App.get_running_app()
        app.save(self.selection[0])


class InfyApp(App):
    filepath = None

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
        lines = txt.split("\n")
        results = evaluator.eval(doc)
        results_text = ""
        for i, result in enumerate(results):
            if i > 0:
                results_text += "\n"
            if len(lines[i].strip()) == 0:  # avoid "0" on empty lines
                continue
            if result.__class__.__name__ == 'Quantity':
                result = result.magnitude
            if int(result) == float(result):
                result = int(result)  # avoid .0 on results
            else:
                result = round(result, 2)
            results_text += str(result)
        results_area.text = results_text
        print("new text from root.textarea", self.root.textarea.text, results_text)


evaluator = Evaluator()

if __name__ == "__main__":
    InfyApp().run()
