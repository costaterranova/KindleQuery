import pandas as pd

def clip_parser():
        
    
    try:
        filepath = '/Users/Apple/Desktop/LIFE/Present/EDU/BOOKS/MODEL/tempDir/name.txt'
        with open(filepath, encoding="utf8", errors='ignore') as f:
                    full_name = f.read()
        filepath = f'/Users/Apple/Desktop/LIFE/Present/EDU/BOOKS/MODEL/tempDir/{full_name}_Clippings.txt'
        with open(filepath, encoding="utf8", errors='ignore') as f:
            file = f.read()
            print('using uploaded file')


    except:
        print('upload file')
        file = ''
        
    if len(file) > 0:
        frasi = file.split('\n')

        for i in range(len(frasi)):
            if "- Your Highlight on Location" in frasi[i]:
                frasi[i] = frasi[i].split(' | ')
            if '==========' in frasi[i]:
                frasi[i] = ""
            if "- Your Note on Location" in frasi[i]:
                frasi[i] = frasi[i].split(' | ')
                frasi[i+2] = frasi[i+2] + 'èunanota'
            if "-  La tua evidenziazione alla posizione" in frasi [i]:
                frasi[i] = frasi[i].split(' | ')
            if "La tua nota alla posizione" in frasi [i]:
                frasi[i] = frasi[i].split(' | ')
                frasi[i+2] = frasi[i+2] + 'èunanota'

        while("" in frasi) :
            frasi.remove("")

        libr = []
        wrongs = []
        for frase in range(len(frasi)-1):
            lib = {}

            try:

                if isinstance(frasi[frase], list): 
                    lib['autore'] = frasi[frase-1].split(' (')[1][:-1]
                    lib['titolo'] = frasi[frase-1].split(' (')[0]

                    lib['location'] = frasi[frase][0].split(' ')[-1]
                    if frasi[frase][1].endswith('M'):
                        lib['date'] = ' '.join(frasi[frase][1].split(' ')[-5:])
                    else:
                        lib['date'] = ' '.join(frasi[frase][1].split(' ')[-4:])

                    if not frasi[frase+1].endswith('èunanota'):
                        lib['citazione'] = frasi[(frase +1)]
                        lib['nota'] = ''
                        libr.append(lib)
                    elif frasi[frase+1].endswith('èunanota'):
                        lib['citazione'] = ''
                        lib['nota'] = frasi[(frase +1)][:-8]
                        libr.append(lib)
            except:
                wrongs.append(frasi[frase])
                
        libreria = pd.DataFrame(libr)
        libreria = libreria[~libreria['autore'].str.contains("COSTANTINO TERRANOVA")]
        libreria = libreria[~libreria['titolo'].str.contains("Absorptive Capacity")]
        libreria = libreria[~libreria['titolo'].str.contains("STE Draft 6")]

        # removing duplicates and useless quotes
        # must create a new dataframe for notes
        libreria = libreria[libreria['citazione'] != '']
        libreria = libreria.drop_duplicates(subset = 'citazione').reset_index()
        list_of_quotes_to_drop = []
        for quote in range(1,len(libreria)-1):
            if libreria['citazione'][quote] in libreria['citazione'][quote+1] or libreria['citazione'][quote] in libreria['citazione'][quote-1]:
                list_of_quotes_to_drop.append(quote) 
            if len(libreria['citazione'][quote].split(' ')) < 3 and quote not in list_of_quotes_to_drop:
                list_of_quotes_to_drop.append(quote)

        libreria = libreria.drop(list_of_quotes_to_drop).reset_index()
        libreria = libreria.drop('level_0', axis=1, inplace=False)
        libreria = libreria.drop('index', axis=1, inplace=False)

        return libreria
    else:
        return file




