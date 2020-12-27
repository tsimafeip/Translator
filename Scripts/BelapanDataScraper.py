from nltk import tokenize
import regex as re
import requests
from bs4 import BeautifulSoup as bs
from typing import List, Tuple


def tokenize_from_text(text: str) -> List[str]:
    tokenized_text = tokenize.sent_tokenize(text, language="russian")
    tokenized_clean_text = []
    ad_sentenses = ["Подробности — на сайте www.belapan.com.",
                    "в службе подписки БелаПАН.",
                    "Падрабязнасці — на сайце www.belapan.com.",
                    "можна замовіць у службе падпіскі",
                    "Даведка БелаПАН.",
                    "Справка БелаПАН."]
    unuseful_sent = ["Нацыянальны банк Беларусі ўстанавіў",
                     "Национальный банк Беларуси установил"]

    # to avoid same sentences as "31 кастрычніка, Мінск" we use [1:]
    for line in tokenized_text[1:]:
        if any(substring in line for substring in ad_sentenses):
            continue
        if any(substring in line for substring in unuseful_sent):
            break
        tokenized_clean_text.append(line)
    return tokenized_clean_text


def next_month_page(old_url: str) -> str:
    m = re.search(r'archive/(\d{4,})/(\d{2,})/', old_url)
    year = int(m.group(1))
    new_month = int(m.group(2)) + 1
    if new_month == 13:
        new_month = 1
        year += 1
    if year == 2018 and new_month == 12:
        return "exit"
    str_month = str(new_month).zfill(2)
    replaced_year_url = old_url.replace(m.group(1), str(year))
    new_url = replaced_year_url[:35] + str_month + replaced_year_url[37:69] + str_month + replaced_year_url[71:]
    write_progress(f"Year: {year}. Month: {new_month}")
    print(f"Year: {year}. Month: {new_month}")
    return new_url


def process_month_page(month_page_url: str) -> List[str]:
    try:
        response = requests.get(month_page_url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = bs(response.content, 'html.parser')
    links = []
    for link in soup.findAll('a', href=True, target="_blank"):
        correct_link_ending = link['href']
        # to avoid incorrect non-number links
        if not any(c.isalpha() for c in correct_link_ending[8:].replace("eu", "")):
            if correct_link_ending.find("_") != -1:
                links.append(f"https://by.belapan.by{correct_link_ending}")
    print("Links count: " + str(len(links)))
    write_progress("Links count: " + str(len(links)))
    return links


def process_article_page(page_url: str) -> Tuple[int, List[str]]:
    try:
        r = requests.get(page_url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    soup = bs(r.content, 'html.parser')
    tokenized_clean = []

    # single element is expected with the 'wysiwygContent' class tag
    for content in soup.findAll('div', class_='wysiwygContent'):
        if "Этот материал доступен только по платной подписке." in content.text:
            return -1, []
        tokenized_clean = tokenize_from_text(content.text)
        break
    return len(tokenized_clean), tokenized_clean


def get_rus_url(url_bel: str):
    rus_url_start = url_bel.replace('by.', '')
    index_of_last_symbol = rus_url_start.rfind('_')
    return rus_url_start[:index_of_last_symbol]


def write_counter_to_file(counter: int):
    with open("counter.txt", 'w') as file:
        file.write(str(counter))


def write_progress(progress_sentence: str):
    with open("progress.txt", 'a') as file:
        file.write(f"{progress_sentence}\n")


def write_tokenized_text(text_array: List[str], path_to_file: str):
    with open(path_to_file, 'a', encoding="utf8") as file:
        file.writelines(f"{line}\n" for line in text_array)


start_url = r"https://by.belapan.by/archive/2007/09/?filterby=month&startdate=2007-09-01&chunksize=3000"

if __name__ == "__main__":
    current_url = start_url
    path_to_bel_file = "Belarusian.txt"
    path_to_rus_file = "Russian.txt"
    counter_rus = 0
    counter_bel = 0
    while current_url != "exit":
        current_url = next_month_page(current_url)
        links = process_month_page(current_url)
        for bel_link in links:
            rus_link = get_rus_url(bel_link)
            counter_rus_current, tokenized_rus_text = process_article_page(rus_link)
            if counter_rus_current == -1:
                continue

            counter_bel_current, tokenized_bel_text = process_article_page(bel_link)
            if counter_bel_current != counter_rus_current:
                write_progress(f"Different tokens amount! "
                               f"RusCounterGlobal: {counter_rus}, BelCounterGlobal: {counter_bel}\n"
                               f"RusCounterCurrent: {counter_rus_current}, BelCounterCurrent: {counter_bel_current}\n"
                               f"BelLink: {bel_link}\nRusLink: {rus_link}")
            else:
                write_tokenized_text(tokenized_rus_text, path_to_rus_file)
                write_tokenized_text(tokenized_bel_text, path_to_bel_file)
                counter_rus += counter_rus_current
                counter_bel += counter_bel_current
                write_counter_to_file(counter_rus)
                progress_sentence = f'Tokenized sentences: {counter_rus}'
                print(progress_sentence)
                write_progress(progress_sentence)
