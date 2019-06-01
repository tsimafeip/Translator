
path_to_rus_chunk = r'RusssianNotAligned6.txt'
path_to_bel_chunk = r'BelarusssianNotAligned6.txt'
with open(path_to_rus_chunk, 'r', encoding = "utf-8") as rus_file, with open(path_to_bel_chunk, 'r', encoding = "utf-8") as bel_file:
    russianLines = f.readlines()
    belarussianLines = f.readlines()

for index, (ruLine, belLine) in enumerate((zip(russianLines, belarussianLines))):
    maxLine = max(len(ruLine), len(belLine))
    minLine = min(len(ruLine), len(belLine))
    coef = minLine/maxLine

    # Border coefficients and their modifications were found empirically
    border = 0.7341772  
    if (ruLine.startswith('В настоящее время') and belLine.startswith('Цяпер')): border = 0.69
    if (minLine<=56 or maxLine<=35): border=0.55
    if (minLine<=10 or maxLine<=10): border=0.49

    # You can skip manually some indexes with correct translations
    if (index == 543 or index == 57349): continue;
    
    if coef < border: 
        print(f'Coef:{coef}')
        print(f'Border:{border}')
        print("Index:" + str(index + 1))
        print(ruLine)
        print(belLine)      
        break
