import os, sys


# Funzione controlla se un comando è già installato, in caso contrario lo installa
def controllo_comando_installato(comando):

    comandi_base = ["wget", "curl", "git"]
    if (comando in comandi_base):
        controllo_base(comando)
    elif (comando == "trivy"):
        controllo_trivy()
    else:
        controllo_semgrep() 


# Funzione che gestisce il controllo di comandi base come wget, curl, git 
def controllo_base(comando):

    try:
        #estraggo il nome del pacchetto se esiste, read per leggere popen
        nome = os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}'").read()
        if(nome != f"{comando}\n"):
            print(f"{comando} non installato, procedo con l'installazione ...\n")
            os.system(f"sudo apt -y install {comando}")
    except Exception as e:
        print(f"Si è verificato un errore durante l'installazione di {comando}: {str(e)}")
        sys.exit(-1)


# Funzione che gestisce il controllo avanzato specifico per trivy
def controllo_trivy():

    try:
        comando = "trivy"
        #estraggo il nome del pacchetto se esiste, read per leggere popen
        nome = os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}'").read()
        #estraggo i numeri delle versioni, read per leggere popen e int per convertire in int e confrontare dopo. Awk stampa la colonna 3, cut taglia al punto e mi stampa la colonna 1 o 2
        versione1 = int(os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f1").read())
        versione2 = int(os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f2").read())
        if(nome != f"{comando}\n" or (versione1 == 0 and versione2 <50)):
            print(f"\n{comando} non installato o non aggiornato, procedo con l'installazione / aggiornamento ...\n")
            os.system("wget https://github.com/aquasecurity/trivy/releases/download/v0.50.1/trivy_0.50.1_Linux-64bit.deb")
            os.system("sudo dpkg -i trivy_0.50.1_Linux-64bit.deb")
            os.system("sudo rm -f trivy_0.50.1_Linux-64bit.deb")
    except Exception as e:
        print(f"Si è verificato un errore durante l'installazione di {comando}: {str(e)}")   
        sys.exit(-1)


# Funzione che gestisce il controllo avanzato specifico per semgrep
def controllo_semgrep():

    try:
        comando = "semgrep"
        #estraggo il nome del pacchetto se esiste, read per leggere popen
        nome = os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $1 }}'").read()
        #estraggo i numeri delle versioni, read per leggere popen e int per convertire in int e confrontare dopo. Awk stampa la colonna 2, cut taglia al punto e mi stampa la colonna 1 o 2
        versione1 = int(os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f1").read())
        versione2 = int(os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f2").read())
        if((nome != f"{comando}\n") or (versione1 < 1) or (versione1 == 1 and versione2 < 69)):
            print(f"\n{comando} non installato o non aggiornato, procedo con l'installazione dell'ultima versione...\n")
            os.system("python3 -m pip install semgrep")
    except Exception as e:
        print(f"Si è verificato un errore durante l'installazione di {comando}: {str(e)}")
        sys.exit(-1)
