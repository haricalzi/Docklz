import os
from sys import exit
from check_and_install import *
from gestione_directory import *

#funzione che stampa il menù iniziale e chiede quale operazione si vuole effettuare
def presentazione():
    print("---------------------------------------------")
    print("--- SECURITY ANALISYS OF DOCKER CONTAINER ---")
    print("---------------------------------------------")
    print("\nBenvenuto :), scegli un'opzione:")
    print("1 -- Analisi della configurazione di Docker presente sul sistema")
    print("2 -- Analisi di un'immagine Docker")
    print("3 -- Ricerca di secrets")
    print("4 -- Analisi completa")
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
            mkdir_results()
            docker_bench_security()
        case 2:
            check_workdir()
            mkdir_results()
            trivy_image()
        case _:
            exit("Parametro non valido, il programma termina")


#funzione che esegue un controllo della configurazione Docker presente sul sistema tramite il Docker Bench for security
def docker_bench_security():
    print("\nAnalisi della configurazione di Docker presente sul sistema\n")
    #controllo git
    controllo_git()
    #controllo Docker Bench for security
    controllo_DBS()
    os.chdir("docker-bench-security")
    print("\n\nAnalisi in corso, attendere...")
    os.system("sudo ./docker-bench-security.sh > ../results/DockerBenchmarkSecurity.txt")
    print("\nAnalisi della configurazione di Docker presente sul sistema completata, trovi i risultati in /results nel file DockerBenchmarkSecurity.txt\n")


#funzione che ispeziona un'immagine Docker tranmite trivy
def trivy_image():
    print("\nAnalisi di un'immagine Docker\n")   
    #controllo wget
    controllo_wget()
    #controllo trivy
    controllo_trivy()
    os.system("clear")
    #stampo le immagini docker presenti nel sistema 
    print("Ecco un elenco delle immagini docker presenti in locale\n\n")
    os.system("docker images")
    #scelgo ed analizzo un'immagine
    print("\n\nQuale immagine vuoi scansionare? Inserisici il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID: ")
    immagine = input()
    print("\n\nAnalisi in corso, attendere...")
    os.system(f"trivy image {immagine} > results/trivy_image.txt")
    print("\nAnalisi dell'immagine completata, trovi i risultati in /results nel file trivy_image.txt\n")
    
