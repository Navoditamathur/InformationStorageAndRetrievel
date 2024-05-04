import Classes.Path as Path
import os
import pathlib 
# Efficiency and memory cost should be paid with extra attention.
#
# Please add comments along with your code.
class MyIndexWriter:

    def __init__(self, type):
        self.strDataType = type;
        #Initialize global variables and open files
        if self.strDataType == "trecweb":
            pathlib.Path(Path.IndexWebDir).mkdir(parents=True, exist_ok=True)
            self.idno = open(Path.IndexWebDir + "idno.txt","w+")
        else:
            pathlib.Path(Path.IndexTextDir).mkdir(parents=True, exist_ok=True)
            self.idno = open(Path.IndexTextDir + "idno.txt","w+")
        self.ridxBlock = RawIndex()
        global docID
        self.docID = 0
        global numInBlock
        self.numInBlock = 0
        global iBlockID
        self.iBlockID = 0
        return

    def block_to_disk(self, override = False):
        #if the number of documents processed exceeds 40000 create a temporary file and write the created index
        #term1#docid:frequency,position1,position2.....;docid:freq.....
        #term2#....
        if override or self.numInBlock == 40000 :
            if self.strDataType == "trecweb":
                ftemp = open(Path.IndexWebDir + "index"+str(self.iBlockID)+".txt","w+",newline="\n")
            else:
                ftemp = open(Path.IndexTextDir + "index"+str(self.iBlockID)+".txt","w+",newline="\n")
            for x, y in self.ridxBlock.index.items():
                ftemp.write(x.strip()+'#');
                cf = 0
                for i in range(len(y)):
                    cf += y[i][1]
                    ftemp.write(str(y[i][0]).strip() + ":" + str(y[i][1]) + ",")
                    for j in range(2,len(y[i])):
                         if j == (len(y[i]) - 1):
                             s = ";"
                         else:
                             s = ","
                         ftemp.write(str(y[i][j]) + s)
                ftemp.write('@cf='+str(cf))
                ftemp.write("\n")
            #reset the counter
            self.numInBlock = 0
            #increment the number of block files
            self.iBlockID += 1
            #close the temporarory file
            ftemp.close()
            #clear the map object created 
            self.ridxBlock.clear()
            
    # This method build index for each document.
	# NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo, content):
        if docNo != None:
            tokens  = content.split()
            #split the content of the doc to tokens and add it to dictionary with term as key
            dict = {}
            for i in range(len(tokens)):
                token = tokens[i]
                #add token to the dictionary if it's not already added with values as docID, frequency and the position of first occurance of the term in the document
                if token not in dict.keys():
                    dict[token] = [self.docID, 1, i]
                else :
                    #Increment the frequency and append to the array
                    dict[token].append(i);
                    dict[token][1] += 1;
            #Update the block dictionary(Raw Index) created
            self.ridxBlock.update(dict)
        #update the docId
        self.docID += 1
        #update the number of docs in the block
        self.numInBlock += 1
        #write the pair of doc-id and doc-num to the idno file
        self.idno.write(str(self.docID) + "," + docNo.strip() + "\n")
        self.block_to_disk()
        return

    def combine(self) :
        #create a dictionary to store the index
        mp = {}
        termfq = {}
        for i in range(self.iBlockID) :
            #open the temporary file created    
            if self.strDataType == "trecweb":
                f = open(Path.IndexWebDir + "index"+str(i)+".txt","r",newline="\n")
            else:
                f = open(Path.IndexTextDir + "index"+str(i)+".txt","r",newline="\n")
            s = f.readline()
            while s or s != "" or len(s) != 0:
                sp = s.split("#")
                cf = 0
                if len(sp) >= 2 and sp[0] != None and sp[1] != None:
                    postStr = sp[1].split("@cf=")
                    if len(postStr) >= 2:
                        cf = int(postStr[1].strip())
                    if sp[0] not in mp.keys() :
                        # add the term if doesn't exist
                        mp[sp[0]] = postStr[0].strip()
                        termfq[sp[0]] = cf
                    else:
                        # concatenate list with the existing string
                        mp[sp[0]] = mp[sp[0]].strip() + postStr[0].strip()
                        termfq[sp[0]] += cf
                s = f.readline()
            #Delete the temporary file
            if self.strDataType == "trecweb":
                os.remove(Path.IndexWebDir + "index"+str(i)+".txt")
            else:
                os.remove(Path.IndexTextDir + "index"+str(i)+".txt")
        #write to the main index file
        if self.strDataType == "trecweb":
            fidx = open(Path.IndexWebDir + "index.txt","w+")
            fdic = open(Path.IndexWebDir + "dict.txt","w+")
        else:
            fidx = open(Path.IndexTextDir + "index.txt","w+")
            fdic = open(Path.IndexTextDir + "dict.txt","w+")             
        iLineNum = 0
        for k, v in mp.items():
            fidx.write(k.strip() + '=' + v.strip() + "\n");
            #write to dictionary file the the term and line number
            fdic.write(k + "," +str(termfq[k]) + ","+ str(iLineNum) + "\n")
            iLineNum+=1
        mp.clear()
        fidx.close()
        fdic.close()
        

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        #write the remaining index to block
        self.block_to_disk(True)
        if self.idno != None:
            self.idno.close()
        self.ridxBlock.clear()
        self.combine()
        return

            
class RawIndex :
    index = {}
    def update(self, doc) :
        if doc != None :
            for x in doc:
                if x not in self.index.keys():
                    self.index[x] = [doc[x]]
                else:
                    self.index[x].append(doc[x]);
            return True
        return False

    def clear(self) :
        self.index.clear();
