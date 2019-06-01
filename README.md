# Translator
Russian-Belarusian neural translator

The data is a part of my bachelor thesis about neural translation for the language pair Russian-Belarusian.

## Repository
The repo consists of
 - 429k aligned sentence pairs (under Data/AlignedData), split into 10 batches
 - chunks to align (under Data/ChunksToAlign)
 
 - **Data/TabbedCorpusMiddleSent.txt** is a sample of 65966 sentences, at max 80 characters each, and is handy to train a model only on a sample of data.

 - neural network code.
 
 ## Data source
 The main source of the data is https://belapan.by/
 
 ## Collection
 Data was collected using Scripts\BelapanDataScraper.py. 
 Parsing period: october 2007 - december 2018.
 
 Before using this script default tokenizer was extended with pre-trained russian tokenizer (https://github.com/Mottl/ru_punkt).
 Some specific abbreviations ('тэл', 'вул', 'трлн') were added manually.
 
 ## Data processing
 Data was aligned using Scripts\CorpusAlighner.py. It is basic comparison of lines length, which requires a lot of attention, but gives pretty good results.
 
 Afterwards to improve total quality of corpus unique sentences were filtered using Scripts\UniqueSentences.py.
 
--- 
This is an open-source project, data can be used freely.
Any reviews are much than welcome.

-----
Author: _Tsimafei Prakapenka_
