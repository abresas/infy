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
        """
        results_text = ""
        total_visible = False
        variables = {}
        for i, line in enumerate(txt.split("\n")):
            if i > 0:
                results_text += "\n"
            lexer = CustomLexer()
            current_variable = None
            current_expr = AST()
            current_value = 0
            for item in lexer.get_tokens(line):
                print(item)
                if item[0] == Name.Variable:
                    current_variable = item[1]
                elif item[0] == Number:
                    current_value += int(item[1])
                    current_expr.push(item)
                elif item[0] == Name and item[1] in variables:
                    current_value += int(variables[item[1]])
                    current_expr.push(item)
                elif item[0] == Operator:
                    current_expr.push(item)
                elif item[0] == Keyword and item[1] == "total":
                    current_expr.push(item)
                    total = 0
                    for k, v in variables.items():
                        print("key=", k, "value=", v)
                        total += int(v)
                    current_value = total
                elif item[0] == Whitespace:
                    pass
                else:
                    current_variable = None # end of expression
            if not (current_variable is None):
                variables[current_variable] = current_value
            results_text += str(current_value)
        results_area.text = results_text
        results_area.total_visible = total_visible
        self.root.textarea.total_visible = total_visible
        """
        doc = grammar.parse(txt)
        lines = txt.split("\n")
        results = evaluator.eval(doc)
        results_text = ""
        for i, result in enumerate(results):
            if i > 0:
                results_text += "\n"
            if len(lines[i].strip()) == 0:  # avoid "0" on empty lines
                continue
            if int(result) == float(result):
                result = int(result)  # avoid .0 on results
            else:
                result = round(result, 2)
            results_text += str(result)
        results_area.text = results_text
        print("new text from root.textarea", self.root.textarea.text, results_text)


if __name__ == "__main__":
    InfApp().run()
