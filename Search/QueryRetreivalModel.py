import Classes.Query as Query
import Classes.Document as Document

class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.CORPUS_SIZE = ixReader.getCorpusSize()
        self.MU = 2000.0
        return


    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN):
        results = []
        queryResult = {}
        termFreq = {}
        tokens = query.getQueryContent().split(" ")
        #iterate for each token in the query
        for token in tokens:
            if len(token) != 0:
                # get the collection frequency of the token through index reader
                cf = self.indexReader.CollectionFreq(token)
                termFreq[token] = cf
                if (cf == 0) :
                    continue
                # fetch posting list of token if collection frequency is not zero
                postingList = self.indexReader.getPostingList(token)
                #Prepare a nested dictionary of form {docid : {token1:freq1},{token2:freq2}
                for docid,freq in postingList.items():
                    if docid not in queryResult.keys() :
                        ttf = {token:freq}
                        queryResult[docid] = ttf
                    else:
                        queryResult[docid][token] = freq
        lResults = []
        for docid,ttf in queryResult.items():
            score = 1.0
            doclen = self.indexReader.getDocLength(docid)
            c1 = doclen / (doclen + self.MU)
            c2 = self.MU / (doclen + self.MU);
            for token in tokens:
                if len(token) > 0:
                    cf = termFreq[token]
                    if (cf == 0):
                      continue
                    p_ref = float(cf / self.CORPUS_SIZE)
                    if token in ttf.keys():
                        tf = ttf[token]
                        p_doc = float(tf / doclen)
                        # calculate score for each docid fetch
                        score *= (c1 * p_doc + c2 * p_ref)
            tmpDS = DocScore(docid, score)
            lResults.append(tmpDS)
        lResults.sort(key=lambda x: x.score, reverse=True)
        #Prepare an array of top topN documents 
        for i in range(topN):
            ds = lResults[i]
            strId = ds.getId()
            doc = Document.Document()
            doc.setDocId(str(strId))
            doc.setDocNo(self.indexReader.getDocNo(strId))
            doc.setScore(ds.getScore())
            results.append(doc)
        return results

class DocScore :
    def __init__(self, docid, score):
        self.docid = docid
        self.score = score
        return

    def getId(self) :
      return self.docid

    def getScore(self):
      return self.score;
