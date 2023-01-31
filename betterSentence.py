# When receiving error: AttributeError: 'NoneType' object has no attribute 'group'
# try simple fix: pip3 install googletrans==4.0.0-rc1

from googletrans import Translator
from googletrans import LANGUAGES as langs
import tkinter as tk
from random import randrange as rr

languages = list(langs.keys())
# languages = ['en', 'de', 'es', 'it', 'fr', 'da', 'hr', 'lb', 'nl']

from threading import Thread

translation_number = 6
class bThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def fetchTranslations(text, outputbox, outputlabel, update):
    try:    
        outputbox.config(state='normal')
        translator = Translator()
        outputlabel.config(text=f"0/{translation_number}")
        update()
        translation = translator.translate(text, dest='en')
        for i in range(translation_number):
            translation = translator.translate(translation.text, dest=languages[rr(len(languages))])
            outputlabel.config(text=f"{i}/{translation_number}")
            outputbox.delete("1.0", "end")
            outputbox.insert("end", translation.text)
            update()    
        translation = translator.translate(translation.text, dest='de')
        outputlabel.config(text="Done!")
        outputbox.delete("1.0", "end")
        outputbox.insert("1.0", translation.text)
        update()
        outputbox.config(state='disabled')
    except Exception as e:
        outputlabel.config(text=f"ERROR! >> {e}")
        update()

class bSentence(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.textFrame = tk.Frame(parent)
        self.inputText = tk.Text(self.textFrame, wrap="word", width=50)
        self.inputText.pack(side="left")
        self.outputText = tk.Text(self.textFrame, wrap="word", width=50, state='disabled')
        self.outputText.pack(side="right")
        
        self.frameWidgets = tk.Frame(parent)
        self.statusLabel = tk.Label(self.frameWidgets)
        def translate():
            try:
                text = self.inputText.get("1.0", "end").replace("\n", "")
                Tfetch = Thread(target=fetchTranslations, args=(text, self.outputText, self.statusLabel, self.parent.update_idletasks))
                Tfetch.start()
            except Exception as e:
                self.statusLabel.config(text=f"ERROR! >> {e}")
        self.btnTranslate = tk.Button(self.frameWidgets, command=translate, text="Translate!!!")
        self.btnTranslate.pack(side="top")
        self.statusLabel.pack(side="right")

        # setup frames
        self.frameWidgets.pack(side="top")
        self.textFrame.pack(side="top")
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Better Sentence by Carl Bellgardt")
    bSentence(root).pack(padx=10, pady=10)
    root.mainloop()
