# Translator
Russian-Belarusian neural translator

The data is a part of my thesis about neural translation for the language pair Russian-Belarusian.
A demo is available in two modes: web service (https://corpus.by/Translator/) and Google Collaboratory ('Models\demo_joey.ipynb').

## Repository
The repo consists of
 - 429k aligned sentence pairs (under 'Data/AlignedData/'), split into 10 batches
 - chunks to align (under 'Data/ChunksToAlign/')
 
 - 4.5k aligned sentence pairs of medical domain (under 'Data/MedicalData/')
 
 - 12k aligned sentence pairs of the legal domain (under 'Data/LegalData/'). The corpus preparation is still in progress.
 
 - **Data/TabbedCorpusMiddleSent.txt** is a sample of 65966 sentences, at max 80 characters each, and is handy to train a model only on a sample of data.

 - neural network models in Jupiter Notebook format (under 'Models/'). Those models can be easily launched via 'Google Collaboratory'.
 
 ## Data sources
 The source of the data for the main corpus is https://belapan.by/.
 
 Medical data was scraped from the following pages: https://komzdrav-minsk.gov.by/ , https://4gkb.by/ .
 
 Legal data was prepared from documents translated by the team of the United Institute of Informatics Problems National Academy of Science of Belarus (https://ssrlab.by/7804).
 
 ## Collection
 The main corpus was collected using Scripts\BelapanDataScraper.py. 
 Parsing period: October 2007 - December 2018.
 
 Before using this script default tokenizer was extended with a pre-trained Russian tokenizer (https://github.com/Mottl/ru_punkt).
 Some specific abbreviations ('тэл', 'вул', 'трлн') were added manually. The algorithm is described in the following article - https://elib.bsu.by/handle/123456789/259015/ (in Belarusian)/
 
 Medical domain data was added (approximately 4k, 2020).
 
 Legal domain data was added (approximately 12k, 2021).
 
 ## Data processing
 Data were aligned using 'Scripts\CorpusAligner.py'. It is a basic comparison of line length, which requires a lot of attention, but gives pretty good results.
 
 ## Neural network code
 The model was developed with the JoeyNMT as a base framework (https://github.com/joeynmt/joeynmt).
 
 Both 'Models\full_joey.ipynb' and 'Models\demo_joey.ipynb' are intended to use via 'Google Colaboratory'.
 The full version of the notebook allows following the whole process of data preprocessing, model training, and inference.
 The demo version shows opportunities for translation with the trained model.
 
 'Models\full_joey_gdrive_legal_domain_adaptation.ipynb' was designed on the base of full model for domain adaptation. 
 The algorithm is described in 'Models\domain_adaptation_algorithm.txt'.

--- 
This is an open-source project, data can be used freely.
Any reviews are much than welcome.

-----
Author: _Tsimafei Prakapenka_
