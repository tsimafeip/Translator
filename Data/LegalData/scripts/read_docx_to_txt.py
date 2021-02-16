import docx
from nltk import tokenize
from typing import List
import os
from tqdm import tqdm


def raw_extract():
    def tokenize_from_text(text: str) -> List[str]:
        tokenized_text = tokenize.sent_tokenize(text, language="russian")
        cleaned_text = []
        for raw_sent in tokenized_text:
            if raw_sent == '.':
                continue
            dot_split_sents = raw_sent.split('.')

            for dot_split_sent in dot_split_sents:
                if dot_split_sent:
                    semicolon_split_sents = dot_split_sent.split(';')
                    for semicolon_split_sent in semicolon_split_sents:
                        # to skip dummy sentences with commas
                        if semicolon_split_sent and ', ,' not in semicolon_split_sent:
                            cleaned_text.append(semicolon_split_sent + '\n')
        return cleaned_text

    def get_text(root_path: str, filename_with_postfix: str) -> None:
        filename, postfix = filename_with_postfix.split('.')
        doc = docx.Document(os.path.join(root_path, filename_with_postfix))
        processed_path = os.path.abspath(os.path.join(root_path, '..', 'processed'))
        with open(os.path.join(processed_path, f'{filename}.txt'), "w", encoding='utf-8') as f:
            for para in doc.paragraphs:
                tokenized_from_text = tokenize_from_text(para.text.replace(u'\xa0', u' '))
                f.writelines(tokenized_from_text)

    root_path = os.path.abspath(os.path.join(os.getcwd(), "..", "data", "raw"))
    files = os.listdir(root_path)
    for file in files:
        get_text(root_path, file)


def concat():
    root_path = os.path.abspath(os.path.join(os.getcwd(), "..", "data", "final"))
    files = os.listdir(root_path)
    final_file_ru = "legal_data_ru.txt"
    final_file_be = "legal_data_be.txt"
    with open(os.path.join(root_path, final_file_be), "w", encoding="utf-8") as final_be, \
            open(os.path.join(root_path, final_file_ru), "w", encoding="utf-8") as final_ru:
        for file in files:
            with open(os.path.join(root_path, file), "r", encoding="utf-8") as cur_file:
                parts = file.split('_')
                if len(parts) == 3: 
                    if parts[1].startswith("ru"):
                        final_ru.writelines(cur_file.readlines())
                    else:
                        final_be.writelines(cur_file.readlines())


def clean():
    def clean_speficic_lang(filepath: str, activation_words: List[str], skip_words: List[str]):
        activated = False
        seen_sentences = set()
        with open(filepath, "r", encoding="utf-8") as input_file, \
                open(filepath + "_cleaned.txt", "w", encoding="utf-8") as output_file:
            for index, line in enumerate(input_file):
                # write doc name as first line
                if index == 0 or activated:
                    # skip specific lines: numberic, only non-valid chars or skipwords
                    if any(line.lower().startswith(skip_w) for skip_w in skip_words) \
                            or line.strip().isnumeric() \
                            or not any([ch.isalpha() for ch in line.strip()]):
                        test = index
                        continue

                    if line.lstrip().lower() not in seen_sentences:
                        # to switch headers to correct case
                        if all([ch.isupper() for ch in line.strip() if ch.isalpha()]):
                            lstrip_line = line.lstrip()
                            line = lstrip_line[0] + "".join([ch.lower() for ch in lstrip_line[1:]])
                        output_file.write(line.lstrip())
                        seen_sentences.add(line.lstrip().lower())
                else:
                    if any(line.lower().startswith(act_word) for act_word in activation_words):
                        activated = True

    root_path = os.path.abspath(os.path.join(os.getcwd(), "..", "data", "processed"))
    files = [file for file in os.listdir(root_path) if 'cleaned' not in file]
    for filename in tqdm(files):
        _, lang_with_prefix = filename.split('_')
        filepath = os.path.join(root_path, filename)
        if lang_with_prefix.startswith('be'):
            clean_speficic_lang(filepath,
                                activation_words=['змест', 'раздзел', 'глава'],
                                skip_words=['глава', 'артыкул'])
        else:
            clean_speficic_lang(filepath,
                                activation_words=['оглавление', 'содержание', 'раздел', 'глава'],
                                skip_words=['глава', 'статья'])

#   raw_extract()
#clean()
concat()


# # with open('kodeks_ru.txt', 'r', encoding='utf-8') as f_read, open('kodeks_ru_cleaned.txt', 'w', encoding='utf-8') as f_write:
# #     for index, line in enumerate(f_read):
# #         if len(line) > 700:
# #             f_write.write(line)
# #
# # with open('kodeks_be.txt', 'r', encoding='utf-8') as f_read, open('kodeks_be_cleaned.txt', 'w', encoding='utf-8') as f_write:
# #     for index, line in enumerate(f_read):
# #         if len(line) > 400:
# #             f_write.write(line)
# #             break
