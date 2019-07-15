from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.config import Config
from lexer import CustomLexer

from pygments.token import Number, Operator, Keyword, Text, Name, Whitespace

from grammar import grammar
from evaluator import Evaluator

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')


class Line(Widget):
    pass


evaluator = Evaluator()


class InfApp(App):
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


if __name__ == "__main__":
    InfApp().run()
