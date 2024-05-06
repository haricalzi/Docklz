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
def mkdir_results(scelta_iniziale):
    #controllo che la cartella non sia già stata creata
    ris = os.popen("ls | grep results").read()
    if(ris!="results\n"):
        #in caso non esista la creo
        print("Creo una cartella chiamata \"results\" all'interno dell'attuale area di lavoro, contenente i risultati delle varie scansioni")
        print("PS: ricordati di spostarla o rimuoverla, una volta terminate le scansioni, e salvati i dati, per evitare interferenze\n")
        os.system("mkdir results")
   #controllo se devo creare le cartelle per le varie modalità 
    match scelta_iniziale:
        case 1:
            #cartella per risultati delle scansioni LIGHT 
            #controllo che la cartella non sia già stata creata
            ris = os.popen("ls \\results | grep light").read()
            if(ris!="light\n"):
                #in caso non esista la creo
                print("Creo una cartella chiamata \"light\" all'interno di \"results\", contenente i risultati delle scansioni LIGHT")
                os.chdir("results")
                os.system("mkdir light")
                os.chdir("..")
        case 2:
            #cartella per risultati delle scansioni BASE 
            #controllo che la cartella non sia già stata creata
            ris = os.popen("ls \\results | grep base").read()
            if(ris!="base\n"):
                #in caso non esista la creo
                print("Creo una cartella chiamata \"base\" all'interno di \"results\", contenente i risultati delle scansioni BASE")
                os.chdir("results")
                os.system("mkdir base")
                os.chdir("..")
        case 3:
            #cartella per risultati delle scansioni FULL 
            #controllo che la cartella non sia già stata creata
            ris = os.popen("ls \\results | grep full").read()
            if(ris!="full\n"):
                #in caso non esista la creo
                print("Creo una cartella chiamata \"full\" all'interno di \"results\", contenente i risultati delle scansioni FULL")
                os.chdir("results")
                os.system("mkdir full")
                os.chdir("..")
