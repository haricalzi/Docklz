from functions import * 
from gestione_directory_files import *

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


#funzione che stampa la conclusione del programma
def fine():
    os.system("clear")
    print("\n\nGrazie per aver utilizzato questo tool, spero ti sia stato utile")
    print("\nPer ulteriori informazione: Hari / github / linkedin\n\n")

#funzione che gestice la scelta effettuata dall'utente
def assegna_compito(scelta):
    os.system("clear")
    #controllo il valore inserito dall'utente
    match scelta:
        case 1:
            path_ris = mkdir_results(scelta)
            docker_bench_security(path_ris)
            attendi_input()
        case 2:
            check_workdir()
            path_ris = mkdir_results(scelta)
            immagine = docker_inspect(path_ris)
            attendi_input()
            trivy_image(path_ris, immagine)
            attendi_input()
        case 3:
            check_workdir()
            path_ris = mkdir_results(scelta)
            path_scansioni = check_sourcecode_dir()
            docker_bench_security(path_ris)
            attendi_input()
            immagine = docker_inspect(path_ris)
            attendi_input()
            trivy_image(path_ris, immagine)
            attendi_input()
            trivy_fs(path_ris, path_scansioni)
            attendi_input()
            semgrep_scan(path_ris, path_scansioni)
            attendi_input()
        case _:
            exit("Parametro non valido, il programma termina")


#inizio main vero e proprio ----------------------------------------------------------

end = "false"
while (end != "true"):
    #stampo il menù di benvenuto 
    presentazione()
    #scelta iniziale da fare
    assegna_compito(int(input("\n\nInserire l'opzione desiderata: ")))
    os.system("clear")

    if (int(input("\n\nScansione completata, vuoi effettuare un'altra analisi [1 = si, 0 = no]? ")) == 0 ):
        end = "true"

#stampo la conclusione del programma
fine()

#fine main vero e proprio ------------------------------------------------------------
