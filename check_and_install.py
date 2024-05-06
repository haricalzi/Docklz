#test11

import os

#funzione controlla se git è già installato, in caso contrario lo installa
def controllo_git():
    print("Controllo se hai già installato git, in caso contrario lo installo\n")
    #estraggo il nome del pacchetto (git) se esiste, read per leggere popen
    nome = os.popen("dpkg -l | grep -w git | awk '{ print $2 }'").read()
    #controllo se il pacchetto è installato
    if(nome != "curl\n"):
        print("Curl non installato, procedo con l'installazione ...\n")
        os.system("sudo apt install git")
    else:
        print("Git già installato\n")


#funzione che controlla se wget è già installato, in caso contrario lo installa
def controllo_wget():
    rint("Controllo se hai già installato wget, in caso contrario lo installo\n")
    #estraggo il nome del pacchetto (wget) se esiste, read per leggere popen
    nome = os.popen("dpkg -l | grep -w wget | awk '{ print $2 }'").read()
    #controllo se il pacchetto è installato
    if(nome != "wget\n"):
        print("Wget non installato, procedo con l'installazione ...\n")
        os.system("sudo apt install wget")
    else:
        print("Wget già installato\n")


#funzione che controlla se curl è già installato, in caso contrario lo installa
def controllo_curl():
    print("Controllo se hai già installato curl, in caso contrario lo installo\n")
    #estraggo il nome del pacchetto (curl) se esiste, read per leggere popen
    nome = os.popen("dpkg -l | grep -w curl | awk '{ print $2 }'").read()
    #controllo se il pacchetto è installato
    if(nome != "curl\n"):
        print("Curl non installato, procedo con l'installazione ...\n")
        os.system("sudo apt install curl")
    else:
        print("Curl già installato\n")


#funzione che controlla se semgrep è già installato, in caso contrario lo installa
def controllo_semgrep():
    print("Controllo se hai già installato semgrep, in caso contrario lo installo\n")
    os.system("python3 -m pip install semgrep")


#funzione che controlla se il Docker Bench for Security è già installato, in caso contrario lo installa
def controllo_DBS():
    print("Controllo se hai già installato Docker Bench for Security nell'attuale directory, in caso contrario lo installo\n")
    ris = os.popen("ls | grep docker-bench-security").read()
    if(ris!="docker-bench-security\n"):
        print("Docker Bench for Security non installato, procedo con l'installazione ...\n")
        os.system("git clone https://github.com/docker/docker-bench-security.git")
    else:
        print("Docker Bench for Security già installato\n")


#funzione che controlla se trivy è già installato, in caso contrario lo installa
def controllo_trivy():
    print("Controllo se hai già installato trivy, in caso contrario lo installo\n")
    #estraggo il nome del pacchetto (trivy) se esiste, read per leggere popen
    nome = os.popen("dpkg -l | grep -w trivy | awk '{ print $2 }'").read()
    #estraggo i numeri delle versioni, read per leggere popen e int per convertire in int e confrontare dopo 
    versione1 = int(os.popen("dpkg -l | grep trivy | awk '{ print $3 }' | cut -d '.' -f1").read())
    versione2 = int(os.popen("dpkg -l | grep trivy | awk '{ print $3 }' | cut -d '.' -f2").read())
    #controllo se il pacchetto è installato o non aggiornato
    if(nome != "trivy\n" or (versione1 == 0 and versione2 <50)):
        print("Trivy non installato o non aggiornato, procedo con l'installazione / aggiornamento ...\n")
        os.system("wget https://github.com/aquasecurity/trivy/releases/download/v0.50.1/trivy_0.50.1_Linux-64bit.deb")
        os.system("sudo dpkg -i trivy_0.50.1_Linux-64bit.deb")
        os.system("rm -f trivy_0.50.1_Linux-64bit.deb")
    else:
        print("Trivy già installato ed aggiornato\n")