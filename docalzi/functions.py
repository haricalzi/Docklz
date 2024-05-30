import os
from datetime import datetime
from .check_and_install import *
from .report import *

#funzione che esegue un controllo della configurazione Docker presente sul sistema tramite il Docker Bench for security
def docker_bench_security(path_ris, report_pdf):
    print("----------------------------------------------------------------")
    try:
        print("\nInstallo il Docker Bench of Security\n")
        os.system("git clone https://github.com/docker/docker-bench-security.git")
        os.chdir("docker-bench-security")
    except Exception as e:
        print(f"Si è verificato un errore durante l'installazione del Docker Bench for Security: {str(e)}")
    try:
        nome_file = "DockerBenchmarkSecurity.txt"
        print("\nAnalisi della configurazione di Docker in corso...")
        os.system(f"sudo ./docker-bench-security.sh > {path_ris}/{nome_file}")
        os.chdir("..")
        os.system("sudo rm -rf docker-bench-security")
        testo = f"Analisi della configurazione di Docker completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}"
        print(f"\n{testo}\n")
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione del Docker Bench for Security: {str(e)}")


#funzione che ispeziona un'immagine Docker tramite Docker CLI
def docker_inspect(path_ris, immagine):
    print("----------------------------------------------------------------")
    print("\nAnalisi di un'immagine Docker tramite Docker CLI\n")
    try:
        nome_file = "docker_inspect.json"
        os.system(f"sudo docker image inspect {immagine} > {path_ris}/{nome_file}")
        print(f"\nAnalisi dell'immagine con Docker CLI completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi dell'immagine tramite Docker CLI: {str(e)}")


#funzione che ispeziona un'immagine Docker tramite trivy
def trivy_image(path_ris ,immagine):
    print("----------------------------------------------------------------")
    print("\nAnalisi di un'immagine Docker tramite Trivy\n")   
    print("\nAnalisi in corso, attendere...\n")
    nome_file = "trivy_image.json"
    try:
        os.system(f"sudo trivy image -f json {immagine} > {path_ris}/{nome_file}")
        print(f"\nAnalisi dell'immagine con trivy completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi dell'immagine tramite Trivy: {str(e)}")


#funzione che ispeziona, tramite trivy, una directory alla ricerca di vulnerabilità, secrets, misconfigurations
def trivy_fs(path_ris):
    print("----------------------------------------------------------------")
    print("\nTrivy: analisi della directory alla ricerca di vulnerabilità, secrets, misconfigurations in corso, attendere...\n")
    nome_file = "trivy_fs.json"
    try:
        os.system(f"sudo trivy fs -f json --scanners vuln,secret,misconfig . > {path_ris}/{nome_file}")
        print(f"\nAnalisi della directory completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi di Trivy: {str(e)}")   


#funzione che ispeziona tramite semgrep il codice sorgente dell'applicazione
def semgrep_scan(path_ris):
    print("----------------------------------------------------------------")
    print("\nSemgrep: analisi del codice sorgente dell'applicazione in corso, questo passaggio potrebbe richiedere un po' di tempo. Attendere...")
    nome_file = "semgrep_scan.txt"
    try:
        os.system(f"semgrep scan > {path_ris}/{nome_file}")
        print(f"\nAnalisi del codice sorgente completata, trovi i risultati grezzi in {path_ris} nel file {nome_file}\n")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi di Semgrep: {str(e)}") 


#funzione che crea la cartella per i risultati
def mkdir_results(path):
    actual = os.getcwd()
    os.chdir(path)
    tosave = os.getcwd() 
    nome_dir = "results"
    if not os.path.exists(nome_dir):
        try:
            os.mkdir(nome_dir)
            print("----------------------------------------------------------------")
            print(f"\nCreo una cartella chiamata \"{nome_dir}\" all'interno di quella attuale, contenente i risultati delle varie scansioni")
        except OSError as e:
            print(f"Errore durante la creazione della cartella \"{nome_dir}\": {e}")
            return None   
    
    nome_sottodir = data_ora()

    if not os.path.exists(f"{nome_dir}/{nome_sottodir}"):
        try:
            os.chdir(nome_dir)
            os.mkdir(nome_sottodir)
            print(f"\nCreo una cartella chiamata \"{nome_sottodir}\" all'interno di \"{nome_dir}\", contenente i risultati delle scansioni\n")
        except OSError as e:
            print(f"Errore durante la creazione della cartella \"{nome_sottodir}\": {e}")
            return None
    os.chdir(actual)
    return f"{tosave}/{nome_dir}/{nome_sottodir}", f"{nome_sottodir}.pdf"


#funzione che permette di effettuare un clone da una repository GitHub
def git_clone_sourcecode(path_git):
    print("----------------------------------------------------------------")
    try:
        os.system(f"git clone {path_git}")
        print("\ngit clone effettuato correttamente")
    except Exception as e:
        print(f"Errore durante l'esecuzione di git clone: {str(e)}")


#funzione che gestisce data e ora per creare file unici ed evitare sovrascrittura
def data_ora():
    try:
        attuale = datetime.now()
        return f"{attuale.day}-{attuale.month}-{attuale.year}__{attuale.hour}-{attuale.minute}-{attuale.second}"
    except Exception as e:
        print(f"Errore durante la generazione di data ed ora: {e}")
        return None


#funzione che stampa un messaggio iniziale
def stampa_iniziale():
    print("\n\n--------------------------------------------------")
    print("-------------------- DOCALZI ---------------------")
    print("--------------------------------------------------")
    print("----- SECURITY ANALISYS OF DOCKER CONTAINERS -----")
    print("--------------------------------------------------\n\n")
    print("NB 1: si presuppone che sul sistema sia già stato installato e configurato correttamente Docker")
    print("\nNB 2: prerequisiti: wget, curl, pip, trivy, semgrep")
    print("\nNB 3: potrebbe essere richiesta la password di root in alcuni passaggi, in quanto alcuni comandi necessitano di sudo per essere eseguiti")


#funzione che stampa il menù di help
def stampa_help():
    print("\n\n---------------------------------------------------")
    print("-------------- 'docalzi -h' per help --------------")
    print("---------------------------------------------------\n\n")