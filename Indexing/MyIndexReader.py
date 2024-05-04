import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
#
# Please add comments along with your code.
class MyIndexReader:
    
    def __init__(self, type):
        #create global dictionary to store doc id - doc no pairs
        global docIDNoMap
        self.docIDNoMap = {}
        global ptrMap
        #create global dictionary to store doc id - colllection frequency, Pointer pairs
        self.ptrMap = {}
        self.strDataType = type
        if self.strDataType == "trecweb":
            idno = open(Path.IndexWebDir + "idno.txt","r")
            dict = open(Path.IndexWebDir + "dict.txt","r")
        else:
            idno = open(Path.IndexTextDir + "idno.txt","r")
            dict = open(Path.IndexTextDir + "dict.txt","r")
        idNoStr = idno.readline()
        while idNoStr or idNoStr!="" or len(idNoStr) != 0:
            s = idNoStr.split(",")
            self.docIDNoMap[s[0]] = s[1]
            self.docIDNoMap[s[1]] = s[0]
            idNoStr = idno.readline()
        lineNoStr = dict.readline()
        while lineNoStr or lineNoStr!="" or len(lineNoStr) != 0:
            s = lineNoStr.split(",")
            self.ptrMap[s[0]] = [s[1],s[2]]
            lineNoStr = dict.readline()
        print("finish reading the index")

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        if docNo in self.docIDNoMap.keys():
            return str(self.docIDNoMap[docNo])
        return -1

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        if docId in self.docIDNoMap.keys():
            return self.docIDNoMap[docId]
        return -1

    # Return DF.
    def DocFreq(self, token):
        arr = []
        #get posting lists
        #docid:frequency,position1,position2.....;docid:freq.....
        posting = self.getPosting(token)
        if str(posting) != "-1":
            arr = posting.split(";")
        df = 0
        for i in arr:
            if len(i)>0:#avoid empty strings
                df += 1
        return df
    

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        if token in self.ptrMap.keys():
            return self.ptrMap[token][0]
        return 0

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        posting = self.getPosting(token)
        #docid:frequency,position1,position2.....;docid:freq.....
        if str(posting) != "-1":
            plist = {}
            arr = posting.split(";")
            for i in arr:
                if len(i) > 0:
                    docStr = i.split(":")
                    #docStr[1] is of form frequency,position1,position2.....
                    #while docStr[0] contains docId
                    if len(docStr) > 0:
                        doc = docStr[0].strip()
                        freqstr = docStr[1].split(",")
                        freq = int(freqstr[0])
                        plist[doc] = freq
            if len(plist) > 0:
                return plist
        return

    def getPosting(self, token):
        if token in self.ptrMap.keys():
            if self.strDataType == "trecweb":
                index = open(Path.IndexWebDir + "index.txt","r",newline="\n")
            else:
                index = open(Path.IndexTextDir + "index.txt","r",newline="\n")
            #lineNo (pointer) stored in map
            lineNo = self.ptrMap[token][1]
            if int(lineNo) >= 0:
                for i in range(int(lineNo)):
                    index.readline();
                postingStr = index.readline()
            index.close()
            #term=docid:frequency,position1,position2.....;docid:freq.....
            pos = postingStr.split("=")
            if pos[0].strip() == token.strip():
                return pos[1].strip()
            return -1
        return -1
