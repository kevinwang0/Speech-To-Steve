import spacy
import neuralcoref

#installing neuralcoref:
#pip install neuralcoref
#pip install spacy==2.1.0
#for medium:
#python -m spacy download en_core_web_md
#for large:
#python -m spacy download en_core_web_lg

nlp = spacy.load('en_core_web_lg') #use medium sized english model 
#nlp.Defaults.stop_words |= {'a','an','the', 'to'} 
#nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
#nlp.add_pipe(nlp.create_pipe('merge_entities'))
neuralcoref.add_to_pipe(nlp)

class Command:
    filterWords = {'a','an','the', 'to', 'then', 'for', 'in', 'on', 'at', 'by'} #static class atribute
    actions = [ 'jump', 'walk', 'crouch', 'run', 'find', 'kill', 'turn', 'switch', 'equip', 'go', 'break', 'cook', 'use']
    entities = ['llama', 'cow', 'sheep', 'chicken', 'horse', 'pig']
    food = ["mutton", "chicken", "porkchop", 'pork', "beef", 'cow', 'sheep', 'chicken', 'pig']
    blocks = ['coal ore', 'log', 'iron ore', 'lapis ore']

    #used a dict so similarity checks for a category of actions (keys) and then searches for specfic supported actions(values)
    #reduces search to a category of actions instead the entire range of actions

    def __init__(self, rawText):
        numerical = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four':'4', 'five': '5', 'six':'6', 'seven': '7', 'eight':'8', 'nine': '9'}
        wordList = []
        for word in rawText.split():
            if word in numerical.keys():
                wordList.append(numerical[word])
            else:
                wordList.append(word)
        self.rawText = " ".join(wordList)
        self.doc = nlp(self.rawText)
        if self.doc._.has_coref:
            self.rawText = self.doc._.coref_resolved
            self.doc = nlp(self.doc._.coref_resolved)
    
    #helper function for check_adj()
    def check_prep(self, prep):
        nouns = []
        for tok in prep.children:
            if tok.pos_ == 'NOUN':
                nouns.append(tok)
        return nouns
        
    #helper function for parse() used to pick up potential undetected noun chunks
    def check_adj(self, word):
        adj = []     
        for tok in word.children:
            if tok.dep_ == 'prep':
                for n in self.check_prep(tok):
                    adj += self.check_adj(n)
            elif tok.pos_ == "NUM" or tok.pos_ == "ADJ" or tok.pos_ == "ADV" or tok.dep_ == "compound":
                    adj.append(tok)

        print("check adj ->", word.text, '->', adj + [word.text])
        return adj + [word]
    
    #helper function for parse() used to get conjunctive sentence/ compound words
    #ie Find a sheep, horse, and cow -> [sheep, horse, cow]
    def parse_conj(self, dobj, verb):
        objList = []
        for child in dobj.children:
            print("parse conjunction ->", dobj.text, '-> ', child.text)
            if (child.pos_ == 'NOUN' or child.pos_ == 'ADV') and (child.dep_ == 'conj'):
                objList.append( {verb: self.check_adj(child) }) #find adj for found noun/adv
                objList += self.parse_conj(child, verb)  #check if there is connecting to found noun/adv
        return objList
    
    #Parses doc object and returns a list of dicts. Each dict's key is the verb and the value a list of tokens
    #kind of buggy works on grammarly correct sentences, and mixed results on more relaxed sentences
    def parse(self):
        parseList = []
        for token in self.doc:
            if token.pos_ == 'VERB':
                print("VERB -> ", token.lemma_) 
                print("VERB CHILDREN -> ", [c.text for c in token.children])
                neg = 0
                dobjs = []
                pair = {token.lemma_: dobjs}
                for child in token.children:
                    print("VERB CHILD ->", child.text)
                    if child.pos_ == 'ADV' and child.dep_== 'neg':
                        neg = 1
                        print("NEGATIVE CASE") #ie input is "do not walk left" then ignore the command
                        break
                    elif child.pos_ == 'NOUN' or child.dep_ == 'dobj': #verb then noun
                        print("NOUN CASE")
                        dobjs += self.check_adj(child)
                        objList = self.parse_conj(child, token.lemma_) #check for conjunctions
                        if objList:
                            parseList += objList
                    elif child.pos_ == 'ADP' and child.dep_ == 'prep': # prepositional phrases
                        print("PREP PHRASE CASE")
                        for p in child.children:
                            print("prep", p.text)
                            if p.pos_ == 'NOUN':
                                dobjs += self.check_adj(p) 
                                objList = self.parse_conj(p,token.lemma_) #don't check for conjunction preps?
                                if objList:
                                    parseList += objList
                    elif (child.pos_ == 'ADV' or child.dep_ == 'advmod') and not child.text in Command.filterWords: #add adverbs
                        print("ADVERB CASE")
                        dobjs += (self.check_adj(child))
                        objList = self.parse_conj(child, token.lemma_) #check for conjunctions
                        if objList:
                            parseList += objList
                if not neg:
                    parseList.append(pair)

        print("PARSELIST ->", parseList)
        parseList = self.similarity_actions(parseList) #similarity check against Command.actions
        print("PARSELIST AFTER SIMILARITY ->", parseList)
        return parseList

    #helper function for similarity_actions
    def best_similarity(self,word):
        mostSimilar = ""
        mostSimilarProb = 0
        doc = nlp(self.rawText)
        for action in Command.actions:
            currentProb = nlp(self.rawText.replace(word,action)).similarity(doc)
            if currentProb > mostSimilarProb:
                mostSimilar = action
                mostSimilarProb = currentProb
        return mostSimilar

    #jump run walk
    #check similiarty of action
    #only actions
    def similarity_actions(self, parseList):
        newParseList = []
        for i,pair in enumerate(parseList):
            for k in pair.keys():
                objList = parseList[i][k] #save old keys objList
                newKey = self.best_similarity(k)
                newParseList.append({newKey:objList})
        return newParseList

    #find similarity (a probability) of word2 against word1 with orginal doc
    def similarity_words(self, w1, w2):
        doc = nlp(self.rawText)
        #print("SIMILAIRTY TExt ->", self.rawText.replace(w1, w2))
        synonymDoc = nlp( self.rawText.replace(w1, w2))
        return synonymDoc.similarity(doc)
