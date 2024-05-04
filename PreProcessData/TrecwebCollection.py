import Classes.Path as Path
import bs4

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
# Please add comments along with your code.
class TrecwebCollection:

    def __init__(self):
        # 1. Open the file in Path.DataWebDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.documents = open(Path.DataWebDir, "r")
        return

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        # 3. the HTML tags should be removed in document content.
        docNo = ""
        content = ""
        text = False
        for index, line in enumerate(self.documents):
            if '<DOC>' in line:
                continue
            if '<DOCNO>' in line:
                docNo = line[8:24]
            if '</DOCHDR>' in line:
                text = True
                continue
            if '</DOC>' in line:
                return [docNo, content]
            if text == True:
                parserObj = bs4.BeautifulSoup(line)
                htmltext = parserObj.get_text()
                content += " " + htmltext;
        if docNo == "":
            self.documents.close()
            return None
        return [docNo, content]
