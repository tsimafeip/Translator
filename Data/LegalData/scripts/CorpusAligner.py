﻿import os

# judges, process, budget

doc_name = "budget"
be_postfix = "_be.txt_cleaned.txt"
ru_postfix = "_ru.txt_cleaned.txt"
root_path = os.path.join(os.getcwd(), "..", "source_data", "processed")
path_to_rus_chunk = os.path.abspath(os.path.join(root_path, f"{doc_name}{ru_postfix}"))
path_to_bel_chunk = os.path.abspath(os.path.join(root_path, f"{doc_name}{be_postfix}"))

for index, (rus_line, bel_line) in enumerate((zip(open(path_to_rus_chunk, 'r', encoding="utf-8"),
                                                  open(path_to_bel_chunk, 'r', encoding="utf-8")))):
    max_line = max(len(rus_line), len(bel_line))
    min_line = min(len(rus_line), len(bel_line))
    coef = min_line / max_line

    # Border coefficients and their modifications were found empirically
    border = 0.7841772
    if rus_line.startswith('В настоящее время') and bel_line.startswith('Цяпер'): border = 0.69
    if min_line <= 56 or max_line <= 35: border = 0.55
    if min_line <= 10 or max_line <= 10: border = 0.49

    # You can skip manually some indexes with correct translations
    #if (index + 1) in [87, 92]: continue

    if coef < border:
        print(f'Coef: {coef}')
        print(f'Border: {border}')
        print(f'Index: {index + 1}')
        print(rus_line)
        print(bel_line)
        break
else:
    print("Done!")
