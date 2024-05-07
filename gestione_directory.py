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
def mkdir_results(s):
    #controllo che la cartella non sia già stata creata
    nome_dir = "results"
    ris = os.popen(f"ls | grep {nome_dir}").read()
    if(ris!=f"{nome_dir}\n"):
        #in caso non esista la creo
        print(f"Creo una cartella chiamata \"{nome_dir}\" all'interno dell'attuale area di lavoro, contenente i risultati delle varie scansioni")
        print("PS: ricordati di spostarla o rimuoverla, una volta terminate le scansioni, e salvati i dati, per evitare interferenze\n")
        os.system(f"mkdir {nome_dir}")
   #nomi per le directory nelle varie modalità di scansione 
    match s:
        case 1:
            nome_sottodir = "light"
        case 2:
            nome_sottodir = "base"
        case 3:
            nome_sottodir = "full"

    #controllo che la cartella non sia già stata creata
    ris = os.popen(f"ls \\{nome_dir}  | grep {nome_sottodir}").read()
    if(ris!=f"{nome_sottodir}\n"):
        #in caso non esista la creo
        print(f"Creo una cartella chiamata \"{nome_sottodir}\" all'interno di \"{nome_dir}\", contenente i risultati delle scansioni {nome_sottodir}")
        os.chdir(f"{nome_dir}")
        os.system(f"mkdir {nome_sottodir}")
        os.chdir("..")

    #creo il path e lo ritorno, utile per le funzioni successive
    path = f"{nome_dir}/{nome_sottodir}" 
    return path