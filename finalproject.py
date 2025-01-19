#
# finalproject.py (Final Project)
#
# Building an initial text model 
#
import math

def clean_text(txt):
    """takes a string of text (txt) as a parameter and returns
       a list containing the words in txt after it has been
       'cleaned'. This function will be used when you need 
       to process each word in a text individually, without 
       having to worry about punctuation or special characters
    """
    for symbol in """.,?"'!;:""":
        txt = txt.replace(symbol, '')
    text = txt.lower()
    text = text.split()
    return text

def stem(s):
    """accepts a string as parameter. The function should then
       return the stem of s
    """
    if len(s) >= 2:
        if s[-1] == 's' and s[-2] != 's':
            s = s[:-1]
            stem_rest = stem(s)
            return stem_rest
        if s[-2:] == 'er':
            s = s[:-2]
        elif s[-2:] == 'ed':
            s = s[:-2]
        elif s[-1] == 'y':
            s = s[:-1]
    if len(s) >= 5:
        if s[-3:] == 'ess':
            s = s[:-4]
        elif s[-3:] == 'ing':
            s = s[:-3]
        elif s[-4:] == 'ship':
            s = s[:-4]
        elif s[-3:] == 'ion':
            s = s[:-4]
        elif s[-4:] == 'ment':
            s = s[:-4]
        elif s[-3:] == 'ful':
            s = s[:-3]
    if len(s) >= 2:
        if s[-1] == s[-2]:
            s = s[:-1]
    return s

def compare_dictionaries(d1, d2):
    """takes two dictionaries (d1 and d2) as inputs and computes and
       returns their log similarity score
    """
    if d1 == {}:
        return -50
    else:
        log_sim_score = 0
        total = 0
        for key in d1:
            total += d1[key]
        for key2 in d2:
            if key2 in d1 and d1[key2] != 0:
                log_sim_score += d2[key2] * math.log(d1[key2]/total)
            else:
                log_sim_score += d2[key2] * math.log(0.5/total)
    return log_sim_score

class TextModel:
    def __init__(self, model_name):
        """constructs a new TextModel object by accepting a string (model_name)
           as a parameter
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.endings = {}
        
    def __repr__(self):
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of ending punctuations: ' + str(3) + '\n'
        return s
    
    def add_string(self, s):
        """adds a string a text (s) to the model by augmenting
           the feature dictionaries defined in the constructor
        """
        text = s.replace('!', '.')
        text = text.replace('?', '.')
        text = text.split('.')
        text = text[:-1]
        for sentence in text:
            words = sentence.split()
            len_sentence = len(words)
            if len_sentence not in self.sentence_lengths:
                self.sentence_lengths[len_sentence] = 1
            else:
                self.sentence_lengths[len_sentence] += 1
        
        question = s.split('?')
        question = question[:-1]
        len_question = len(question)
        if '?' not in self.endings:
            self.endings['?'] = len_question
        else:
            self.endings['?'] += len_question
            
        period = s.split('.')
        period = period[:-1]
        len_period = len(period)
        if '.' not in self.endings:
            self.endings['.'] = len_period
        else:
            self.endings['.'] += len_period
            
        exclamation = s.split('!')
        exclamation = exclamation[:-1]
        len_exclamation = len(exclamation)
        if '!' not in self.endings:
            self.endings['!'] = len_exclamation
        else:
            self.endings['!'] += len_exclamation
        
        word_list = clean_text(s)
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
                
    def add_file(self, filename):
        """adds all of the text in the file identified by filename
           to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)
        
    def save_model(self):
        """saves the TextModel object (self) by writing its 
           various feature dictionaries to files
        """
        filename1 = self.name + '_' + 'words'
        words = self.words
        f = open(filename1, 'w')    
        f.write(str(words))
        f.close()
        
        filename2 = self.name + '_' + 'word_lengths'
        word_length = self.word_lengths
        d = open(filename2, 'w')
        d.write(str(word_length))
        d.close()
        
        stems_dict = self.name + '_stems'
        d_stems = self.stems
        f_stems = open(stems_dict, 'w')
        f_stems.write(str(d_stems))
        f_stems.close()
       
        sl_dict = self.name + '_sentence_lengths'
        d_sl = self.sentence_lengths
        f_sl = open(sl_dict, 'w')
        f_sl.write(str(d_sl))
        f_sl.close()
       
        endings_dict = self.name + '_endings'
        d_endings = self.endings
        f_endings = open(endings_dict, 'w')
        f_endings.write(str(d_endings))
        f_endings.close()
        
    def read_model(self):
        """reads the stored dictionaries for the called TextModel
           object from their files and assignes them to attributes
           of the called TextModel
        """
        filename1 = self.name + '_' + 'words'
        f = open(filename1, 'r')
        d_str = f.read()
        f.close()
        d = dict(eval(d_str))
        self.words = d
        
        filename2 = self.name + '_' + 'word_lengths'
        h = open(filename2, 'r')
        g_str = h.read()
        h.close()
        j = dict(eval(g_str))
        self.word_lengths = j
        
        filename3 = self.name + '_' + 'stems'
        open_stem = open(filename3, 'r')
        stem_str = open_stem.read()
        open_stem.close()
        stem = dict(eval(stem_str))
        self.stems = stem
        
        filename4 = self.name + '_' + 'sentence_lengths'
        open_length = open(filename4, 'r')
        length_str = open_length.read()
        open_length.close()
        length = dict(eval(length_str))
        self.sentence_lengths = length
        
        filename5 = self.name + '_' + 'endings'
        open_endings = open(filename5, 'r')
        endings_str = open_endings.read()
        open_endings.close()
        ending = dict(eval(endings_str))
        self.endings = ending
    
    def similarity_scores(self, other):
        """computes and returns a list of log similarity scores
           measuring the similarity of self and other -- one score
           for each type of feature
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        endings_score = compare_dictionaries(other.endings, self.endings)
        final_list = [word_score] + [word_lengths_score] + [stems_score] + [sentence_lengths_score] + [endings_score]
        return final_list
        
    def classify(self, source1, source2):
        """compares the called TextModel object (self) to two other
           'source' TextModel objects (source1 and source2) and determines
           which of these other TextModels is the more likely
           source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ':' + str(scores1))
        print()
        print('scores for ' + source2.name + ':' + str(scores2))
        print()
        weighted_sum1 = 10*scores1[0] + 5*scores1[1] + 7*scores1[2] + 10*scores1[3] + 5*scores1[4]
        weighted_sum2 = 10*scores2[0] + 5*scores2[1] + 7*scores2[2] + 10*scores2[3] + 5*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name, 'is more likely to have come from', source1.name)
        elif weighted_sum2 > weighted_sum1:
            print(self.name, 'is more likely to have come from', source2.name)
        print()
    
    
    
