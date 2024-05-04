import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery
import datetime

if __name__ == "__main__":
    startTime = datetime.datetime.now()

    index = MyIndexReader.MyIndexReader("trectext")
    search = QueryRetreivalModel.QueryRetrievalModel(index)
    extractor = ExtractQuery.ExtractQuery()
    queries= extractor.getQuries()
    for query in queries:
        print(query.topicId,"\t",query.queryContent)
        results = search.retrieveQuery(query, 20)
        rank = 1
        for result in results:
            print(query.getTopicId()," Q0 ",result.getDocNo(),' ',rank," ",result.getScore()," MYRUN",)
            rank += 1

    endTime = datetime.datetime.now()
    print("load index & retrieve the token running time: ", endTime - startTime)
