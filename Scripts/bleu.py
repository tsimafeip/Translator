from sacrebleu import corpus_bleu

fileBel = r'...\med_sentences_be.txt'
fileBelPred = r'..\med.txt'

with open(fileBel, 'r', encoding="utf-8") as fileBel, \
        open(fileBelPred, 'r', encoding="utf-8") as fileBelPred:
    realBel = fileBel.readlines()
    predBel = fileBelPred.readlines()

print(corpus_bleu(predBel, [realBel]))
