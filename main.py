from functions import * 
from gestione_directory import *

#funzione che stampa il menù iniziale e chiede quale operazione si vuole effettuare
presentazione()

#scelta iniziale da fare
scelta_iniziale = input()
assegna_compito(scelta_iniziale)

#funzione che stampa il menù iniziale e chiede quale operazione si vuole effettuare
def presentazione():
    print("---------------------------------------------")
    print("--- SECURITY ANALISYS OF DOCKER CONTAINER ---")
    print("---------------------------------------------")
    print("\nBenvenuto :), quale tipo di analisi vuoi effettuare?")
    print("1 -- LIGHT: analisi della configurazione di Docker presente sul sistema")
    print("2 -- BASE: analisi di un'immagine Docker")
    print("3 -- FULL: analisi completa di un progetto Docker")
    print("---------------------------------------------")
    print("\n\nNB 1: potrebbe essere richiesta la password di root in alcuni passaggi, in quanto alcuni comandi necessitano di sudo per essere eseguiti\n")
    print("\n\nNB 2: si presuppone che sul sistema sia già stato installato configurato correttamente Docker\n\n")
    print("\nopzione desiderata: ")


#funzione che gestice la scelta effettuata dall'utente
def assegna_compito(scelta_iniziale):
    os.system("clear")
    #controllo il valore inserito dall'utente
    match scelta_iniziale:
        case 1:
            mkdir_results(scelta_iniziale)
            docker_bench_security(scelta_iniziale)
        case 2:
            check_workdir()
            mkdir_results(scelta_iniziale)
            trivy_image(scelta_iniziale)
        case 3: mkdir_results(scelta_iniziale)

        case _:
            exit("Parametro non valido, il programma termina")