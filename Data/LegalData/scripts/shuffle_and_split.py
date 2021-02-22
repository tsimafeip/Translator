import random
from sklearn.model_selection import train_test_split

be_data = []
ru_data = []
with open('legal_data_be.txt','r', encoding='utf-8') as source_be, open('legal_data_ru.txt','r', encoding='utf-8') as source_ru:
    be_data = source_be.readlines()
    ru_data = source_ru.readlines()

print(len(be_data))
print(len(ru_data))

be_train, be_test, ru_train, ru_test = train_test_split(be_data, ru_data, test_size=0.15, random_state=42)

with open('legal_data_train_be.txt','w', encoding='utf-8') as train_be, open('legal_data_train_ru.txt','w', encoding='utf-8') as train_ru, \
     open('legal_data_test_be.txt','w', encoding='utf-8') as test_be, open('legal_data_test_ru.txt','w', encoding='utf-8') as test_ru:
    train_be.writelines(be_train)
    train_ru.writelines(ru_train)
    test_be.writelines(be_test)
    test_ru.writelines(ru_test)
