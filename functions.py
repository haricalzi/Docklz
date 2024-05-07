import os
from sys import exit
from check_and_install import *
from gestione_directory import *

#funzione che esegue un controllo della configurazione Docker presente sul sistema tramite il Docker Bench for security
def docker_bench_security(s):
    print("\nAnalisi della configurazione di Docker presente sul sistema\n")
    #controllo git
    controllo_git()
    #controllo Docker Bench for security
    controllo_DBS()
    os.chdir("docker-bench-security")
    print("\n\nAnalisi in corso, attendere...")
    #in base alla scelta, lo salvo nella cartella giusta 
    match s:
        case 1:
            os.system("sudo ./docker-bench-security.sh > ../results/light/DockerBenchmarkSecurity.txt")
            print("\nAnalisi della configurazione di Docker presente sul sistema completata, trovi i risultati grezzi in /results/light nel file DockerBenchmarkSecurity.txt\n")
        case 2:
            print("\nAnalisi della configurazione di Docker presente sul sistema completata, trovi i risultati grezzi in /results/base nel file DockerBenchmarkSecurity.txt\n")
        case 3:
            print("\nAnalisi della configurazione di Docker presente sul sistema completata, trovi i risultati grezzi in /results/full nel file DockerBenchmarkSecurity.txt\n")


#funzione che ispeziona un'immagine Docker tranmite trivy
def trivy_image(s):
    print("\nAnalisi di un'immagine Docker\n")   
    #controllo wget
    controllo_wget()
    #controllo trivy
    controllo_trivy()
    os.system("clear")
    #stampo le immagini docker presenti nel sistema 
    print("Ecco un elenco delle immagini Docker presenti in locale\n\n")
    os.system("docker images")
    #scelgo ed analizzo un'immagine
    print("\n\nQuale immagine vuoi scansionare? Inserisici il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID: ")
    immagine = input()
    print("\n\nAnalisi in corso, attendere...")
    #in base alla scelta, lo salvo nella cartella giusta 
    match s:
        case 1:
            os.system(f"trivy image {immagine} > results/light/trivy_image.txt")
            print("\nAnalisi dell'immagine completata, trovi i risultati grezzi in /results/light nel file trivy_image.txt\n")
        case 2:
            os.system(f"trivy image {immagine} > results/base/trivy_image.txt")
            print("\nAnalisi dell'immagine completata, trovi i risultati grezzi in /results/base nel file trivy_image.txt\n")
        case 3:
            os.system(f"trivy image {immagine} > results/full/trivy_image.txt")
            print("\nAnalisi dell'immagine completata, trovi i risultati grezzu in /results/full nel file trivy_image.txt\n")

#funzione che ispezione tramite trivy una directory
def trivy_fs():
   print()

#funzione che ispezione tramite semgrep una directory
def semgrep_scan():
   print()