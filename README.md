This contains code to build a index and search for a set of documents. It is part of assignment for academic credict for IS 2140. 

HW1Main.py:
Task 1: Reading Documents from Collection Files
In this task, we implement two classes that can read individual documents from trectext and trecweb format collection files.
PreProcessData.DocumentCollection is a general interface for sequentially reading documents from collection files
PreProcessData.TrectextCollection is the class for trectext format
PreProcessData.TrecwebCollection is the class for trecweb format
Task 2: Normalize Document Texts
In this task, we implement classes to tokenize document texts into individual words, normalize all the words into their lowercase characters, and finally filter stop words.
PreProcessData.TextTokenizer is a class for sequentially reading words from a sequence of characters
PreProcessData.TextNormalizer is the class that transform each word to its lowercase version, and conduct stemming on each word.
PreProcessData.StopwordsRemover is the class that can recognize whether a word is a stop word or not. A stop word list file will be provided, so that the class should take the stop word list file as input.

HW2Main.py
Task 1: Build an index.
In this task, we implement:
Indexing. PreProcessedCorpusReader You will need to get access to the result.trectext and result.trecweb, and return document one by one through the nextDocument(). 
Indexing.MyIndexWriter This class has one essential method IndexADocument (String docno, String content) to create index for a document represented by the docno and the content. The content is a list of words, segmented by blank space generated in the Assignment 1. 
Task 2: Retrieve posting lists of tokens from an index
In this task, we implement:
Indexing. MyIndexReader, which has the following methods:
MyIndexReader():
int GetDocid( String docno ) and String getDocno( int docid ): provides transformation between string docnos and integer docids.
int[][] GetPostingList( String token ): retrieve posting list of the token as a 2-dimension array (see comments in MyIndexReader for the structure of the array)
int GetDocFreq( String token ): get the document frequency of the token.
long GetCollectionFreq( String token ): get the collection frequency of the token

HW3Main.py
Task 1: Automatically translate topic statements to queries
For a given set of topic statements, you should have a module to translate the topic statement information into a set of queries that can be recognized by your retrieval module, in which each query corresponds to a search topic and consists of a query content and a query id. Tokenization, normalization and stop-word removing should be conducted on each query.
In this task,we implement:
Search.ExtractQueryn Queries are extracted and preprocessed from TREC style topic file topics.txt.
Classes.Query: This class stores query information, including the topic id and a representation of the query. If you need to store other information about the query, you CAN MODIFY Classes.Query. The topic file “topics.txt” contains four TREC style topics. Note that the forth topic contains a word “Dysphagia” that did not appear in the collection. You should detect and process such cases.
Task2: Implementing the Statistical Language Model
Your implementation should be able to read the index you built in assignment 2 using document collection file “docset.trectext” (you should use our provided implementation of index builder), and return documents based on the ranking of the documents generated by your retrieval model. The retrieval model is the query likelihood model with Dirichlet Prior Smoothing.
In this task, you should implement:
Search.QueryRetrievalModel In this class, you should implement the method 
retrieveQuery(Query aQuery, int TopN), which retrieves the input query and returns the top N retrieved documents as a list of Classes.Document objects.
IndexingLucene.MyIndexReader/ IndexingWithWhoosh.MyIndexReader:
Returned documents for each query should be ranked in decreasing order of their scores, and they
should be in the following format.
queryid Q0 documentid rank score runid
For example, in the run with an id TEST, for query 40004, document APW20010120.0310.0146 is ranked as number 1 with score 0.65, then the content format for this document is as following. Here Q0 is just a dummy filler, you put it all for all the lines. All the results for every query are saved in one single file.
40004 Q0 APW20010120.0310.0146 1 0.65 TEST

HW4Main.py: (With Relevance feedback)
We need to implement at least the following steps:
(1) Obtain feedback documents: conduct the initial search using the query likelihood retrieval model with Dirichlet smoothing (as required by assignment 3, you can use your own assignment 3 codes), and obtain top K documents where K is a parameter set by the system. These K documents are treated as the relevant documents;
(2) For each query term qi in the query, calculate the probability of the feedback documents generating this term, i.e., P(qi | feedback documents). Here all feedback documents are treated as one big pseudo document;
(3) Then for each query term qi, the probability of one document D generating it based on relevance feedback is a linear combination of the original probability P(qi | D) and P(qi | feedback documents), where parameter α is used as the coefficient of P(qi | D) and 1-α is used as the coefficient for P(qi | feedback documents);
(4) The probability of the query generated by the document is all the probabilities of each query term multiplying together;
(5) Sort top N documents based on the probability generated in step 4


