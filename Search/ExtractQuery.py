import Classes.Query as Query
import Classes.Path as Path
import PreProcessData.StopWordRemover as StopWordRemover
import PreProcessData.WordNormalizer as WordNormalizer
import PreProcessData.WordTokenizer as WordTokenizer

class ExtractQuery:

    def __init__(self):
        # 1. you should extract the 4 queries from the Path.TopicDir
        # 2. the query content of each topic should be 1) tokenized, 2) to lowercase, 3) remove stop words, 4) stemming
        # 3. you can simply pick up title only for query.
        self.f = open(Path.TopicDir)
        return

    # Return extracted queries with class Query in a list.
    def getQuries(self):
        q = []
        line = self.f.readline()
        while "<top>" in line:
            title = ""
            title_n = ""
            desc = ""
            desc_n = ""
            narr = ""
            narr_n = ""
            #Prepare a query object
            qNext = Query.Query()
            line = self.f.readline()
            topid = line.split(':')
            # set Topic Id
            qNext.setTopicId(topid[1].strip())
            line = self.f.readline()
            title = line.split('>')[1].strip()
            line = self.f.readline()
            line = self.f.readline()
            while "<narr>" not in line :
                if "<desc>"in line :
                    line = self.f.readline()
                desc += line;
                line = self.f.readline()
            while "</top>" not in line :
                if "<narr>"in line :
                    line = self.f.readline()
                narr += line
                line = self.f.readline()
            tokenizer_title = WordTokenizer.WordTokenizer(title.strip())
            tokenizer_desc = WordTokenizer.WordTokenizer(desc.strip())
            tokenizer_narr = WordTokenizer.WordTokenizer(narr.strip())
            stopwordRemover = StopWordRemover.StopWordRemover()
            #initialize word normalizer
            normalizer = WordNormalizer.WordNormalizer()
            while True:
                word = tokenizer_title.nextWord()
                if word == None:
                    break
                word = normalizer.lowercase(word)
                if stopwordRemover.isStopword(word) == False:
                    title_n += normalizer.stem(word) + " "
            while True:
                word = tokenizer_desc.nextWord()
                if word == None:
                    break
                word = normalizer.lowercase(word)
                if stopwordRemover.isStopword(word) == False:
                    desc_n += normalizer.stem(word) + " "
            while True:
                word = tokenizer_narr.nextWord()
                if word == None:
                    break
                word = normalizer.lowercase(word)
                if stopwordRemover.isStopword(word) == False:
                    narr_n += normalizer.stem(word) + " "
            #Set Query Title
            qNext.setQueryTitle(title_n)
            #Set Query Description
            qNext.setQueryDesc(desc_n)
            #Set Query Narration
            qNext.setQueryNarr(narr_n)
            #Set Query Content
            qNext.setQueryContent(title_n)
            q.append(qNext)
            self.f.readline()
            line = self.f.readline()
        return q

