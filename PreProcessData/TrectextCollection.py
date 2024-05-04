import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class TrectextCollection:
    
    def __init__(self):
        # 1. Open the file in Path.DataTextDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.documents = open(Path.DataTextDir, "r")
        return

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        docNo = ""
        content = ""
        text = False
        for index, line in enumerate(self.documents):
            if '<DOC>' in line:
                continue
            if '<DOCNO>' in line:
                docNo = line[8:24]
            if '<TEXT>' in line:
                text = True
                continue
            if '</TEXT>' in line:
                text = False
                continue
            if '</DOC>' in line:
                return [docNo, content]
            if text == True:
                content += line       
        if docNo == "":
            self.documents.close()
            return None
        return [docNo, content]
