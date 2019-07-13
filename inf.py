from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')

class Line(Widget):
    pass


class InfApp(App):
    def text_changed(self, txt):
        results_area = self.root.resultsarea
        results_text = ""
        total_visible = False
        total = 0
        for i, line in enumerate(txt.split("\n")):
            if i > 0:
                results_text += "\n"
            if line == 'total':
                total_visible = True
                results_text += str(total)
            for word in line.split():
                if word.isdigit():
                    results_text += word
                    total += int(word)
                    break
        results_area.text = results_text
        results_area.total_visible = total_visible
        self.root.textarea.total_visible = total_visible
        print("new text from root.textarea", self.root.textarea.text, results_text)


if __name__ == "__main__":
    InfApp().run()
