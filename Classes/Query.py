class Query:

    def __init__(self):
        return

    queryContent = ""
    topicId = ""
    queryTitle = ""
    queryDesc = ""
    queryNarr = ""

    def getQueryContent(self):
        return self.queryContent

    def getTopicId(self):
        return self.topicId

    def setQueryContent(self, content):
        self.queryContent = content

    def setTopicId(self, id):
        self.topicId=id

    def setQueryTitle(self,title) :
        self.queryTitle = title

    def getQueryTitle(self):
        return self.queryTitle

    def setQueryDesc(self, desc) :
        self.queryDesc = desc;

    def getQueryDesc(self):
        return self.queryDesc

    def setQueryNarr(self, narr):
        self.queryNarr = narr;

    def getQueryNarr():
        return self.queryNarr
