from functions import * 
from gestione_directory import *

#funzione che stampa il menù iniziale e chiede quale operazione si vuole effettuare
def presentazione():
    os.system("clear")
    print("---------------------------------------------")
    print("--- SECURITY ANALISYS OF DOCKER CONTAINER ---")
    print("---------------------------------------------")
    print("\nBenvenuto :), quale tipo di analisi vuoi effettuare?\n")
    print("1 -- LIGHT: analisi della configurazione di Docker presente sul sistema")
    print("2 -- BASE: analisi di un'immagine Docker")
    print("3 -- FULL: analisi completa di un progetto Docker (immagine + container + source code)")
    print("\n---------------------------------------------")
    print("\n\nNB 1: potrebbe essere richiesta la password di root in alcuni passaggi, in quanto alcuni comandi necessitano di sudo per essere eseguiti\n")
    print("NB 2: si presuppone che sul sistema sia già stato installato configurato correttamente Docker")
    print("\n\nInserire l'opztrivy fs --scanners vuln,secret,misconfig . ione desiderata: ")


#funzione che gestice la scelta effettuata dall'utente
def assegna_compito(s):
    os.system("clear")
    #controllo il valore inserito dall'utente
    match s:
        case 1:
            path = mkdir_results(s)
            docker_bench_security(path)
        case 2:
            check_workdir()
            path = mkdir_results(s)
            trivy_image(path)
        case 3:
            check_workdir()
            path = mkdir_results(s)
            docker_bench_security(path)
            trivy_image(path)
            trivy_fs(path)
            semgrep_scan(path)

        case _:
            exit("Parametro non valido, il programma termina")


#inizio main vero e proprio ----------------------------------------------------------

#funzione che stampa il menù iniziale e chiede quale operazione si vuole effettuare
presentazione()
#scelta iniziale da fare
s = int(input())
assegna_compito(s)

#fine main vero e proprio ------------------------------------------------------------