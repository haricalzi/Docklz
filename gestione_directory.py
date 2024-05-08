import os 

#funzione che controlla se bisogna cambiare la cartella di lavoro
def check_workdir():
    print(f"Attualmente ti trovi nella seguente cartella: \"{os.getcwd()}\", devo creare una cartella in cui inserire i risultati, va bene se lo faccio qua? [1 = si, 0 = no]")    
    scelta = int(input())
    #la cartella di lavoro va cambiata    
    if(scelta == 0):
        change_workdir()
    #se la cartella di lavoro va bene, proseguo
    

#funzione che permette di cambiare la cartella di lavoro
def change_workdir():
    scelta = 0
    while(scelta != 1):
        print("Inserisci il percorso assoluto o relativo dalla cartella in cui ti trovi fino a quella desiderata [es. progetti/docker/test]")
        print("PS: Se hai bisogno di aiuto, inserisci HELP_PLIS per eseguire un ls. Se devi spostarti indietro, inserisci HELP_BACK oppure .. (come se fosse il comando cd)\n")
        path = input()
        #eseguo un ls per vedere i nomi delle cartelle 
        if(path == "HELP_PLIS"):
            print("\n\n")
            os.system("ls -lah")
            print("\n\n")
        else:
            if(path == "HELP_BACK"):
                path = ".."
            os.chdir(path)
            print(f"Ti sei spostato nella seguente cartella: \"{os.getcwd()}\", è corretta? [1 = si, 0 = no]")
            scelta = int(input())
            #se scelta = 1 esco dal ciclo, se = 2 reinserisco 
    return os.getcwd()


#funzione che crea la cartella per i risultati
def mkdir_results(s):
    #controllo che la cartella non sia già stata creata
    nome_dir = "results"
    ris = os.popen(f"ls | grep {nome_dir}").read()
    if(ris!=f"{nome_dir}\n"):
        #in caso non esista la creo
        print(f"Creo una cartella chiamata \"{nome_dir}\" all'interno di quella attuale, contenente i risultati delle varie scansioni")
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
    path_ris = f"{nome_dir}/{nome_sottodir}" 
    return path_ris


#funzione che permette di selezionare il path per raggiungere il source code da analizzare
def check_sourcecode_dir():
    print("Alcune delle seguenti scansioni, per essere eseguite, necessitano del path fino alla cartella in cui è presente il source code da analizzare.\n")
    print("\nHai a disposizione, sul tuo sistema, una cartella in cui è salvato il source code del progetto? [1 = si, 0 = no]")
    #se la risposta è no chiedo se proprio non lo ha, o se vuole effetuare un clone da github
    if(int(input()) == 0):
        print("\nNon hai proprio il source code (o non vuoi scansionarlo), oppure è presente su GitHub? [1 = GitHub, 0 = non presente / non voglio]")
        #se non è presente chiamo la funzione che lo clona da GitHub
        if(int(input()) == 0):
            print("\nNessun problema, alcune scansioni non verranno effettuate")
            #codice per evitare alcune scansioni 
            return "NO_TRIVY_SEMGREP"
        else:
            git_clone_sourcecode()
    print("\nLa cartella in cui hai deciso di salvare i risultati è la stessa in cui sono presenti i file da analizzare? [1 = si, 0 = no]")
    #se la cartella non coincide bisogna ottenere il path del percorso da analizzare 
    if(int(input()) == 0):
        print("\nTi verrà chiesto di spostarti (temporaneamente) fino alla cartella da analizzare\n")
        #salvo la posizione attuale, mi sposto, salvo e torno
        attuale = os.getcwd()
        path_scansioni = change_workdir()
        os.chdir(attuale)
        print(os.getcwd())
        return path_scansioni
    else:
        #altrimenti il path delle scansioni è quello attuale, lo ritorno
        return os.getcwd()
  
    
#funzione che permette di effettuare un clone da una repository GitHub
def git_clone_sourcecode():
    print("Recati tramite browser nella relativa repository GitHub --> pulsante Code verde --> copia il path di HTTPS --> incollalo qui di seguito")
    path_git = input()
    os.system(f"git clone {path_git}")
    print("\n\ngit clone effettuato correttamente")
    print("\nOra ti verrà chiesto di selezionare questa cartella per le scansioni, rispondi no alla prossima domanda e seleziona la cartella che si è appena creata dopo il git clone")