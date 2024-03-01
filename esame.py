class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name

    

    def __isdateornot(self, date): 
        #le tre virgolette permettono di trovare la funzione nell'help
        '''Funzione per capire se i valori anno-mese siano corretti, sia come tipo di dato che come numeri in questo specifico contesto
        
        Nota: ho messo __ per rendere privato il metodo, per chiamarlo non basta fare .__isdateornot ma è necessario scrivere ._CSVTimeSeriesFile__isdateornot. Lo utilizzo così da indicare che la funzione non è da utilzzare all'esterno o da modificare'''
        
        try:
            element = date.split('-') # mi aspetto che la tra anno e mese ci sia un -, quindi li separo
            anno = int(element[0])
            mese = int (element[1]) # Per verificare che nei due campi ci siano effettivamente dei valori numerici provo a convertirli ad int
#questa funzione va bene anche se nella stringa si mascherano dei float in quanto non si può far diventare una stringa che ricorda un float un int, ma è necessario, prima trasformala in float e poi in int
            
            if (1949 <= anno <= 1960) and (1 <= mese <= 12): #controllo specifico sui parametri del file
                return True
                
        except Exception:
            return False


    
    def get_data(self): #la funzione get_data mi permette di portare in una lista di liste i valori del file csv, in modo che siano eliminate le righe inutili e i dati siano più facilmente gestibili
        lista = [] #creo una lista vuota
        
        try:
            my_file = open(self.name, 'r')
            
        except FileNotFoundError as e: # verifica se il file esiste
            print("Il file {} non esiste!".format(self.name))
            return None

        
        for indx, line in enumerate(my_file): # utilizzo la funzione enumerate assieme al ciclo for per ottenere gli indici assieme agli elementi della lista
            element = line.strip().split(',') # separa la data dal valore ed elimina eventuali spazi vuoti
            
            if indx == 0: # La funzione enumerate torna utile perché mi permette di ignorare indice zero che corrisponde all'intestazione
                continue # Passa all'indice successivo
                
            try:
                date = element[0]
                value = int(element[1])
                
                if not date or not value: #se non vi sono valori, quindi spazi vuoti eliminati in precedenza dalla funzione strip
                    continue #ignora la riga e passa alla successiva
                    
                if not self.__isdateornot(date):  # date è una data?
                    continue # Ignora la riga e passa all'indice sucessivo
                    
                if lista != []: # if che verifica se i valori sono ordinati temporalmente e non vi siano duplicati (=)
                    data_precedente = lista[-1][0] # atteso: '1950-11'
                    data_precedente = data_precedente.split('-') #lista [1950, 11]
                    data_precedente= "".join(data_precedente) # atteso 195011
                    data_corrente = "".join(date.split('-')) #stessa operazione di sopra ma in un' unica riga
                    if data_corrente <= data_precedente:
                        raise ExamException
                
                sub_list = [date, value]
                if value < 0: # non ci possono essere passeggeri negativi
                    continue
                lista.append(sub_list)
                    
                
            except ValueError:
                print("Non posso convertire {} a valore numerico!".format(value))
                print("Ho avuto un errore di valore.")
                
            except IndexError:
                print("ho avuto un errore di indice")  #può essere che ci siano meno di due campi
            except TypeError:
                print("valore nullo") # raccoglie int(None)
            except ExamException:
                raise ExamException ('Le date non sono ordinate!')
                
        my_file.close()
        return lista #lista di liste con data di tipo stringa e valore numerico di tipo int

# fuori dalla classe
def find_min_max(time_series): #funzione che ricerca max e min dei vari anni
    my_dict = {}  # dizionario vuoto
    for row in time_series: # ciclo for sulle sottoliste di time_series restituita dalla get_data
        anno = row[0].split("-")[0] 
        mese = row[0].split("-")[1]
        valore = row[1]
        if not anno in my_dict.keys(): # se non esiste già il dizionario che ha come chiave un anno specifico lo creo, assieme al sottodizionario con mese e valore
            my_dict[anno] = {mese: valore}
        else:
            my_dict[anno][mese] = valore # nel caso in cui il dizionario che ha come parola chiave un determinato anno esiste già lo devo solo aggiornare aggiungendo la parola chiave mese e assegnando il valore

    max_min_dict = {} # nuovo dizionario in cui salverò i max e min
    
    for anno in my_dict:
        Vmax = float('-inf') # assegno un valore minimo alla Vmax
        Vmin = float('inf') # assegno un valore massimo alla Vmin
        max_mesi = []
        min_mesi = [] #creo due liste vuote che andranno a contenere i mesi di max e min
        for mese in my_dict[anno]: # ciclo all'interno dei sottodizionari
            valore = my_dict[anno][mese]  # assegno ad una variabile valore, il valore effettivo corrispondente ad un mese
            if valore > Vmax: # se il valore trovato è maggiore del massimo precedente
                Vmax = valore # si sovrascrive
                max_mesi = [mese] # e si inserisce il mese max nella lista max_mesi
            elif valore == Vmax:
                max_mesi.append(mese) # se vi sono altri mesi in cui si è registrato lo stesso valore di massimo, si appende il mese alla lista max_min
            if valore < Vmin:
                Vmin = valore
                min_mesi = [mese]
            elif valore == Vmin:
                min_mesi.append(mese) # si opera in maniera analoga al caso max, in questo caso con il min
        max_min_dict[anno] = {'max' : max_mesi, 'min' : min_mesi} #al termine di ogni giro di ciclo for si aggiorna il dizionario con i massimi e minini

    return max_min_dict
