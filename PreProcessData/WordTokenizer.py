import Classes.Path as Path
from nltk import RegexpTokenizer

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class WordTokenizer:
    index = 0

    def __init__(self, content):
        # Tokenize the input texts.
        tokenizer = RegexpTokenizer(r"\w+")
        self.tokens = tokenizer.tokenize(content)
        global index
        self.index = 0
        return

    def nextWord(self):
        # Return the next word in the document.
        # Return null, if it is the end of the document.
        word = ""
        if (self.index<len(self.tokens)):
            word = self.tokens[self.index]
            self.index+=1
        else:
            return None
        return word
