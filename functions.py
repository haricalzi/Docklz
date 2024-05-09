import os
from datetime import datetime
from check_and_install import *


#funzione che esegue un controllo della configurazione Docker presente sul sistema tramite il Docker Bench for security
def docker_bench_security(path_ris):
    controllo_comando_installato("git")
    controllo_DBS()
    path_actual = os.getcwd()
    os.chdir("docker-bench-security")
    #eseguo lo script del DockerBenchmarkSecurity, lo salvo nella relativa cartella
    nome_file = f"DockerBenchmarkSecurity{data_ora()}.txt"
    os.system(f"sudo ./docker-bench-security.sh > ../{path_ris}/{nome_file}")
    #torno nella cartella originale
    os.chdir(path_actual)
    print(f"\nAnalisi della configurazione di Docker completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")


#funzione che ispeziona un'immagine Docker tramite Docker CLI
def docker_inspect(path_ris):
    print("\nAnalisi di un'immagine Docker tramite Docker CLI\n")
    nome_file = f"docker_inspect{data_ora()}.txt"
    os.system(f"docker image inspect {immagine} > {path_ris}/{nome_file}")
    print(f"\nAnalisi dell'immagine completata con Docker CLI, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")


#funzione che ispeziona un'immagine Docker tramite trivy
def trivy_image(path_ris ,immagine):
    print("\nAnalisi di un'immagine Docker tramite Trivy\n")   
    #controllo wget
    controllo_comando_installato("wget")
    #controllo trivy
    controllo_comando_installato("trivy")
    print("\n\nAnalisi in corso, attendere...\n")
    #eseguo il comando trivy image sull'immagine specificata, lo salvo nella relativa cartella
    nome_file = f"trivy_image{data_ora()}.txt"
    os.system(f"trivy image {immagine} > {path_ris}/{nome_file}")
    print(f"\nAnalisi dell'immagine completata con Trivy, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")


#funzione che ispeziona, tramite trivy, una directory alla ricerca di vulnerabilità, secrets, misconfigurations
def trivy_fs(path_ris):
    print("\n\nTrivy: analisi della directory alla ricerca di vulnerabilità, secrets, misconfigurations in corso, attendere...")
    #eseguo il comando trivy fs, lo salvo nella relativa cartella
    nome_file = f"trivy_fs{data_ora()}.txt"
    os.system(f"trivy fs --scanners vuln,secret,misconfig . > {path_ris}/{nome_file}")
    print(f"\nAnalisi della directory completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    

#funzione che ispezione tramite semgrep il codice sorgente dell'applicazione
def semgrep_scan(path_ris, path_scansioni):
    os.system("clear")
    #controllo semgrep
    controllo_comando_installato("semgrep")
    print("\n\nSemgrep: analisi del codice sorgente dell'applicazione in corso, attendere...")
    #eseguo il comando semgrep scan, lo salvo nella relativa cartella. Prima di fare ciò mi devo spostare nella cartella del progetto per eseguire lo scan
    nome_file = f"semgrep_scan{data_ora()}.txt"
    os.system(f"semgrep scan > {path_actual}/{path_ris}/{nome_file}")
    print(f"\nAnalisi del codice sorgente completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")


#funzione che crea la cartella per i risultati
def mkdir_results(s, path):
    os.chdir(path) 
    nome_dir = "results"
    if not os.path.exists(nome_dir):
        os.mkdir(nome_dir)
        print(f"Creo una cartella chiamata \"{nome_dir}\" all'interno di quella attuale, contenente i risultati delle varie scansioni")
    match s:
        case 1:
            nome_sottodir = "light"
        case 2:
            nome_sottodir = "base"
        case 3:
            nome_sottodir = "full"
    if not os.path.exists(f"{nome_dir}/{nome_sottodir}"):
        os.chdir(f"{nome_dir}")
        os.mkdir(nome_sottodir)
        print(f"Creo una cartella chiamata \"{nome_sottodir}\" all'interno di \"{nome_dir}\", contenente i risultati delle scansioni {nome_sottodir}")
        os.chdir("..")
    path_ris = f"{nome_dir}/{nome_sottodir}" 
    return path_ris


#funzione che permette di effettuare un clone da una repository GitHub
def git_clone_sourcecode(path_git):
    os.system(f"git clone {path_git}")
    print("\n\ngit clone effettuato correttamente")


#funzione che gestisce data e ora per creare file unici ed evitare sovrascrittura
def data_ora():
    attuale = datetime.now()
    return f"__{attuale.day}-{attuale.month}-{attuale.year}__{attuale.hour}-{attuale.minute}-{attuale.second}"
