import Classes.Query as Query
import Classes.Document as Document
import Classes.Path as Path
from SearchWithWhoosh import QueryRetreivalModel as QueryRetreivalModel


class PseudoRFRetreivalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.CORPUS_SIZE = ixReader.getCorpusSize()
        self.MU = 2000.0
        return

    # Search for the topic with pseudo relevance feedback.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # query: The query to be searched for.
    # TopN: The maximum number of returned document
    # TopK: The count of feedback documents
    # alpha: parameter of relevance feedback model
    # return TopN most relevant document, in List structure

    def retrieveQuery(self, query, topN, topK, alpha):
        # this method will return the retrieval result of the given Query, and this result is enhanced with pseudo relevance feedback
        # (1) you should first use the original retrieval model to get TopK documents, which will be regarded as feedback documents
        # (2) implement GetTokenRFScore to get each query token's P(token|feedback model) in feedback documents
        # (3) implement the relevance feedback model for each token: combine the each query token's original retrieval score P(token|document) with its score in feedback documents P(token|feedback model)
        # (4) for each document, use the query likelihood language model to get the whole query's new score, P(Q|document)=P(token_1|document')*P(token_2|document')*...*P(token_n|document')


        # get P(token|feedback documents)
        
        tokens = query.getQueryContent().split(" ")
        termFreq= {}
        queryResult = {}
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
        TokenRFScore = self.GetTokenRFScore(query, topK, termFreq, queryResult)
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
                        # calculate score for each docid fetched
                        score *= (alpha * (c1 * p_doc + c2 * p_ref) + (1 - alpha) * TokenRFScore[token])
            tmpDS = DocScore(docid, score)
            lResults.append(tmpDS)
        lResults.sort(key=lambda x: x.score, reverse=True)
        #Prepare an array of top topN documents
        # sort all retrieved documents from most relevant to least, and return TopN
        results=[]
        for i in range(topN):
            ds = lResults[i]
            strId = ds.getId()
            doc = Document.Document()
            doc.setDocId(str(strId))
            doc.setDocNo(self.indexReader.getDocNo(strId))
            doc.setScore(ds.getScore())
            results.append(doc)
        return results

    def GetTokenRFScore(self, query, topK, termFreq, queryResult):
        # for each token in the query, you should calculate token's score in feedback documents: P(token|feedback documents)
        # use Dirichlet smoothing
        # save {token: score} in dictionary TokenRFScore, and return it
        q = QueryRetreivalModel.QueryRetrievalModel(self.indexReader)
        #take the top k retrieved documents as feedback
        feedbackDocs = q.retrieveQuery(query, topK)
        pseudoDoc = {}
        length = 0
        #Prepare a dictionary with term and frequency 
        for doc in feedbackDocs:
            id = doc.getDocId()
            a = queryResult[id]
            for term,freq in a.items():
                if term not in pseudoDoc.keys() :
                    pseudoDoc[term] = freq
                else:
                    pseudoDoc[term] += freq
            length += self.indexReader.getDocLength(int(id))
        #Prepare a dictionary with term and score based on length of documents 
        TokenRFScore={}
        pseudoLen = length
        c1 = pseudoLen / (pseudoLen + self.MU)
        c2 = self.MU / (pseudoLen + self.MU)
        for token,tf in pseudoDoc.items():
            cf = termFreq[token]
            p_doc = tf / pseudoLen
            p_ref = cf / self.CORPUS_SIZE
            score = c1 * p_doc + c2 * p_ref
            TokenRFScore[token] = score
        return TokenRFScore


class DocScore :
    def __init__(self, docid, score):
        self.docid = docid
        self.score = score
        return

    def getId(self) :
      return self.docid

    def getScore(self):
      return self.score
