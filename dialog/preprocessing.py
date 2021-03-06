import jieba
import re
import os
from dialog.models import *
from robot.settings import BASE_DIR
class preprocessing():
    __PAD__ = 0
    __GO__ = 1
    __EOS__ = 2
    __UNK__ = 3
    vocab = ['__PAD__', '__GO__', '__EOS__', '__UNK__']
    def __init__(self):
        # self.encoderFile = "./question.txt"
        # self.decoderFile = './answer.txt'
        self.encoderFile = []
        self.decoderFile = []
        for each in Question.objects.all():
            self.encoderFile.append(each.content)
            self.decoderFile.append(each.answer.content)

        # self.dictFile = 'word_dict.txt'
        # jieba.load_userdict(self.dictFile)
        for each in Keyword.objects.all().values_list("content",flat=True):
            jieba.add_word(each)

        # self.stopwordsFile = "./preprocessing/stopwords.dat"
        
    def wordToVocabulary(self, originFile, vocabFile, segementFile):
        # stopwords = [i.strip() for i in open(self.stopwordsFile).readlines()]
        # print(stopwords)
        # exit()
        vocabulary = []
        sege = open(segementFile, "w")
        for sent in originFile:
            # 去标点
            if "enc" in segementFile:
                #sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。“”’‘？?、~@#￥%……&*（）]+", "", sent.strip())
                sentence = sent.strip()
                words = jieba.lcut(sentence)
                print(words)
            else:
                words = jieba.lcut(sent.strip())
            vocabulary.extend(words)
            for word in words:
                sege.write(word+" ")
            sege.write("\n")
        sege.close()

        # 去重并存入词典
        vocab_file = open(vocabFile, "w")
        _vocabulary = list(set(vocabulary))
        _vocabulary.sort(key=vocabulary.index)
        _vocabulary = self.vocab + _vocabulary
        for index, word in enumerate(_vocabulary):
            vocab_file.write(word+"\n")
        vocab_file.close()

    def toVec(self, segementFile, vocabFile, doneFile):
        word_dicts = {}
        vec = []
        with open(vocabFile, "r") as dict_f:
            for index, word in enumerate(dict_f.readlines()):
                word_dicts[word.strip()] = index

        f = open(doneFile, "w")
        with open(segementFile, "r") as sege_f:
            for sent in sege_f.readlines():
                sents = [i.strip() for i in sent.split(" ")[:-1]]
                vec.extend(sents)
                for word in sents:
                    f.write(str(word_dicts.get(word))+" ")
                f.write("\n")
        f.close()
            

    def main(self):
        # 获得字典
        encoderVocabFile = os.path.join(BASE_DIR,'dialog','preprocessing/enc.vocab')
        encoderSegementFile = os.path.join(BASE_DIR,'dialog','preprocessing/enc.segement')
        encoderVec = os.path.join(BASE_DIR,'dialog','preprocessing/enc.vec')
        self.wordToVocabulary(self.encoderFile, encoderVocabFile, encoderSegementFile)

        decoderVocabFile = os.path.join(BASE_DIR,'dialog','preprocessing/dec.vocab')
        decoderSegementFile = os.path.join(BASE_DIR,'dialog','preprocessing/dec.segement')
        decoderVec = os.path.join(BASE_DIR,'dialog','preprocessing/dec.vec')
        self.wordToVocabulary(self.decoderFile, decoderVocabFile, decoderSegementFile)
        # 转向量
        self.toVec(encoderSegementFile, 
                   encoderVocabFile, 
                   encoderVec)
        self.toVec(decoderSegementFile, 
                   decoderVocabFile, 
                   decoderVec)

pre = preprocessing()
pre.main()
