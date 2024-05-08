import os
from sys import exit
from check_and_install import *
from gestione_directory import *


#funzione che esegue un controllo della configurazione Docker presente sul sistema tramite il Docker Bench for security
def docker_bench_security(path_ris):
    print("\nAnalisi della configurazione di Docker presente sul sistema\n")
    #controllo git
    controllo_comando_installato("git")
    #controllo Docker Bench for security
    controllo_DBS()
    #salvo la cartella e mi sposto 
    path_actual = os.getcwd()
    os.chdir("docker-bench-security")
    print("\n\nAnalisi in corso, attendere...")
    #eseguo lo script del DockerBenchmarkSecurity, lo salvo nella relativa cartella
    nome_file = "DockerBenchmarkSecurity.txt"
    os.system(f"sudo ./docker-bench-security.sh > ../{path_ris}/{nome_file}")
    #torno nella cartella originale 
    os.chdir(path_actual)
    print(f"\nAnalisi della configurazione di Docker completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")


#funzione che ispeziona un'immagine Docker tramite Docker CLI
def docker_inspect(path_ris):
    os.system("clear")
    print("\nAnalisi di un'immagine Docker tramite Docker CLI\n")
    #stampo le immagini docker presenti nel sistema 
    print("\nEcco un elenco delle immagini Docker presenti in locale\n\n")
    os.system("docker images")
    #scelgo ed analizzo un'immagine
    print("\n\nQuale immagine vuoi scansionare? Inserisci il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID: ")
    immagine = input()
    #eseguo il comando docker image inspect sull'immagine specificata, lo salvo nella relativa cartella
    nome_file = "docker_inspect.txt"
    os.system(f"docker image inspect {immagine} > {path_ris}/{nome_file}")
    print(f"\nAnalisi dell'immagine completata con Docker CLI, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    return immagine


#funzione che ispeziona un'immagine Docker tramite trivy
def trivy_image(path_ris ,immagine):
    os.system("clear")
    print("\nAnalisi di un'immagine Docker tramite Trivy\n")   
    #controllo wget
    controllo_comando_installato("wget")
    #controllo trivy
    controllo_comando_installato("trivy")
    print("\n\nAnalisi in corso, attendere...\n")
    #eseguo il comando trivy image sull'immagine specificata, lo salvo nella relativa cartella
    nome_file = "trivy_image.txt"
    os.system(f"trivy image {immagine} > {path_ris}/{nome_file}")
    print(f"\nAnalisi dell'immagine completata con Trivy, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")


#funzione che ispeziona, tramite trivy, una directory alla ricerca di vulnerabilità, secrets, misconfigurations
def trivy_fs(path_ris, path_scansioni):
    #se non è presente il source code da analizzare, non eseguo questa funzione 
    if(path_scansioni != "NO_TRIVY_SEMGREP"):
        os.system("clear")
        print("\n\nTrivy: analisi della directory alla ricerca di vulnerabilità, secrets, misconfigurations in corso, attendere...")
        #eseguo il comando trivy fs, lo salvo nella relativa cartella
        nome_file = "trivy_fs.txt"
        os.system(f"trivy fs --scanners vuln,secret,misconfig {path_scansioni} > {path_ris}/{nome_file}")
        print(f"\nAnalisi della directory completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    

#funzione che ispezione tramite semgrep il codice sorgente dell'applicazione
def semgrep_scan(path_ris, path_scansioni):
    #se non è presente il source code da analizzare, non eseguo questa funzione 
    if(path_scansioni != "NO_TRIVY_SEMGREP"):
        #controllo semgrep
        controllo_comando_installato("semgrep")
        os.system("clear")
        print("\n\nSemgrep: analisi del codice sorgente dell'applicazione in corso, attendere...")
        #eseguo il comando semgrep scan, lo salvo nella relativa cartella. Prima di fare ciò mi devo spostare nella cartella del progetto per eseguire lo scan
        nome_file = "semgrep_scan.txt"
        path_actual = os.getcwd()
        os.chdir(path_scansioni)
        os.system(f"semgrep scan > {path_actual}/{path_ris}/{nome_file}")
        os.chdir(path_actual)
        print(f"\nAnalisi del codice sorgente completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")