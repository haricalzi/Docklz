import os 

#funzione che controlla se bisogna cambiare la cartella di lavoro
def check_workdir():
    print(f"Attualmente ti trovi nella seguente cartella: \"{os.getcwd()}\", è quella del progetto Docker da analizzare? [1 = si, 2 = no]")    
    scelta = int(input())
    #la cartella di lavoro va cambiata    
    if(scelta == 2):
        change_workdir()
    #la cartella di lavoro va bene, proseguo
    

#funzione che permette di cambiare la cartella di lavoro
def change_workdir():
    scelta = 2
    while(scelta != 1):
        print("Inserisci il percorso assoluto o relativo dalla cartella in cui ti trovi fino a quella del progetto Docker [es. progetti/docker/test]")
        print("PS: Se hai bisogno di aiuto, inserisci HELP_PLIS per eseguire un ls\n")
        path = input()
        #eseguo un ls per vedere i nomi delle cartelle 
        if(path == "HELP_PLIS"):
            print("\n\n")
            os.system("ls -lah")
            print("\n\n")
        else:
            os.chdir(path)
            print(f"Ti sei spostato nella seguente cartella: \"{os.getcwd()}\", è corretta? [1 = si, 2 = no]")
            scelta = int(input())
            #se scelta = 1 esco dal ciclo, se = 2 reinserisco   


#funzione che crea la cartella per i risultati
def mkdir_results():
    print("Creo una cartella chiama \"results\" all'interno dell'attuale area di lavoro, contenente i risultati delle varie scansioni")
    print("PS: ricordati di spostarla o rimuoverla, una volta terminate le scansioni, e salvati i dati, per evitare interferenze")
    #creo la cartella per i risultati
    os.system("mkdir results")