import os

#funzione che controlla se il Docker Bench for Security è già installato, in caso contrario lo installa
def controllo_DBS():
    #print("Controllo se hai già installato Docker Bench for Security nell'attuale directory, in caso contrario lo installo\n")
    ris = os.popen("ls | grep docker-bench-security").read()
    if(ris!="docker-bench-security\n"):
        print("Docker Bench for Security non installato, procedo con l'installazione ...\n")
        os.system("git clone https://github.com/docker/docker-bench-security.git")


#funzione controlla se un comando è già installato, in caso contrario lo installa (passargli il nome del comando)
def controllo_comando_installato(comando):
    comandi_base = ["wget", "curl", "git"]
    if (comando in comandi_base):
        controllo_base(comando)
    elif (comando == "trivy"):
        controllo_trivy(comando)
    else:
        controllo_semgrep() 


#funzione che gestisce il controllo di comandi base come wget, curl, git 
def controllo_base(comando):
    #estraggo il nome del pacchetto se esiste, read per leggere popen
    nome = os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}'").read()
    #controllo se il pacchetto è installato, altrimenti lo installo
    if(nome != f"{comando}\n"):
        print(f"{comando} non installato, procedo con l'installazione ...\n")
        os.system(f"sudo apt install {comando}")


#funzione che gestisce il controllo avanzato specifico per trivy
def controllo_trivy(comando):
    #estraggo il nome del pacchetto se esiste, read per leggere popen
    nome = os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}'").read()
    #estraggo i numeri delle versioni, read per leggere popen e int per convertire in int e confrontare dopo. Awk stampa la colonna 3, cut taglia al punto e mi stampa la colonna 1 o 2
    versione1 = int(os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f1").read())
    versione2 = int(os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f2").read())
    if(nome != f"{comando}\n" or (versione1 == 0 and versione2 <50)):
        print(f"{comando} non installato o non aggiornato, procedo con l'installazione / aggiornamento ...\n")
        os.system("wget https://github.com/aquasecurity/trivy/releases/download/v0.50.1/trivy_0.50.1_Linux-64bit.deb")
        os.system("sudo dpkg -i trivy_0.50.1_Linux-64bit.deb")
        os.system("rm -f trivy_0.50.1_Linux-64bit.deb")
        

#funzione che gestisce il controllo avanzato specifico per semgrep
def controllo_semgrep(comando):
    #estraggo il nome del pacchetto se esiste, read per leggere popen
    nome = os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $1 }}'").read()
    #estraggo i numeri delle versioni, read per leggere popen e int per convertire in int e confrontare dopo. Awk stampa la colonna 2, cut taglia al punto e mi stampa la colonna 1 o 2
    versione1 = int(os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f1").read())
    versione2 = int(os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f2").read())
    if((nome != f"{comando}\n") or (versione1 < 1) or (versione1 == 1 and versione2 < 69)):
        print(f"{comando} non installato o non aggiornato, procedo con l'installazione / aggiornamento ...\n")
        os.system("python3 -m pip install semgrep")
