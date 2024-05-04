import Classes.Path as Path

# Please add comments along with your code.
class PreprocessedCorpusReader:

    def __init__(self, type):
        self.documents = open(Path.ResultHM1+""+type, "r")
        return

    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
        strDocID = self.documents.readline()
        strDocText = ""
        if (not strDocID) or strDocID == "" or len(strDocID) == 0:
            #close the file if no more doc ids exist
            self.documents.close();
            return None;
        strDocText = self.documents.readline()
        return [strDocID,strDocText]
        
