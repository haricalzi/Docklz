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
    #eseguo lo script del DockerBenchmarkSecurity, lo salvo nella relativa cartella
    nome_file = "DockerBenchmarkSecurity.txt"
    os.system(f"sudo ./docker-bench-security.sh > {path}/{nome_file}")
    print("\nAnalisi della configurazione di Docker completata, trovi i risultati grezzi in {path} nel file {nome_file}\n")
            

#funzione che ispeziona un'immagine Docker tramite trivy
def trivy_image(path):
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
    #eseguo il comando trivy image sull'immagine specificata, lo salvo nella relativa cartella
    nome_file = "trivy_image.txt"
    os.system(f"trivy image {immagine} > {path}/{nome_file}")
    print(f"\nAnalisi dell'immagine completata, trovi i risultati grezzi in {path} nel file {nome_file}\n")


#funzione che ispeziona, tramite trivy, una directory alla ricerca di vulnerabilità, secrets, misconfigurations
def trivy_fs():
    os.system("clear")
    print("\n\nTrivy: analisi della directory alla ricerca di vulnerabilità, secrets, misconfigurations in corso, attendere...")
    #eseguo il comando trivy fs, lo salvo nella relativa cartella
    nome_file = "trivy_fs.txt"
    os.system(f"trivy fs --scanners vuln,secret,misconfig . > {path}/{nome_file}")
    print(f"\nAnalisi della directory completata, trovi i risultati grezzi in {path} nel file {nome_file}\n")
    

#funzione che ispezione tramite semgrep il codice sorgente dell'applicazione
def semgrep_scan():
    #controllo semgrep
    controllo_semgrep()
    os.system("clear")
    print("\n\nSemgrep: analisi del codice sorgente dell'applicazione in corso, attendere...")
    #eseguo il comando semgrep scan, lo salvo nella relativa cartella
    nome_file = "semgrep_scan.txt"
    os.system(f"semgrep scan > {path}/{nome_file}")
    print(f"\nAnalisi della directory completata, trovi i risultati grezzi in {path} nel file {nome_file}\n")