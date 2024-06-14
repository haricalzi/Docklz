import os, sys
from datetime import datetime
from .check_and_install import *
from .analysis import *
from .report import *


# Funzione che crea la cartella per i risultati
def mkdir_results(path):

    actual = os.getcwd()
    os.chdir(path)
    tosave = os.getcwd() 
    nome_dir = "results"
    print("\n----------------------------------------------------------------")

    if not os.path.exists(nome_dir):
        try:
            os.mkdir(nome_dir)
            print(f"\nCreo una cartella chiamata \"{nome_dir}\" all'interno di quella attuale, contenente i risultati delle varie scansioni")
        except OSError as e:
            print(f"Errore durante la creazione della cartella \"{nome_dir}\": {e}")
            sys.exit(-1) 
    
    nome_sottodir = data_ora()

    if not os.path.exists(f"{nome_dir}/{nome_sottodir}"):
        try:
            os.chdir(nome_dir)
            os.mkdir(nome_sottodir)
            print(f"\nCreo una cartella chiamata \"{nome_sottodir}\" all'interno di \"{nome_dir}\", contenente i risultati delle scansioni\n")
        except OSError as e:
            print(f"Errore durante la creazione della cartella \"{nome_sottodir}\": {e}")
            os.chdir(actual)
            sys.exit(-1)

    os.chdir(actual)

    return f"{tosave}/{nome_dir}/{nome_sottodir}", f"{nome_sottodir}"


# Funzione che clona una repository (path HTTPS)
def git_clone_sourcecode(path_git):

    print("----------------------------------------------------------------\n")
    try:
        os.system(f"git clone {path_git}")
        print("\ngit clone effettuato correttamente")
    except Exception as e:
        print(f"Errore durante l'esecuzione di git clone: {str(e)}")
        sys.exit(-1)


# Funzione che gestisce data e ora per creare file e cartelle univoche ed evitare sovrascritture
def data_ora():

    try:
        attuale = datetime.now()
        return f"{attuale.day}-{attuale.month}-{attuale.year}__{attuale.hour}-{attuale.minute}-{attuale.second}"
    except Exception as e:
        print(f"Errore durante la generazione di data ed ora: {e}")
        sys.exit(-1)


# Funzione che stampa il messaggio iniziale
def stampa_iniziale():

    print("\n\n--------------------------------------------------")
    print("-------------------- DOCKLZ ----------------------")
    print("--------------------------------------------------")
    print("----- SECURITY ANALISYS OF DOCKER CONTAINERS -----")
    print("--------------------------------------------------\n\n")
    


# Funzione che stampa il menù di help
def stampa_help():

    print("--------------------------------------------------")
    print("------------ 'docklz -h' -->  help ---------------")
    print("--------------------------------------------------\n\n")


# Funzione che esegue un controllo della configurazione Docker presente sul sistema tramite il Docker Bench for security
def docker_bench_security(path_ris, report_pdf):

    print("----------------------------------------------------------------")
    try:
        print("\nInstallo il Docker Bench of Security\n")
        os.system("git clone https://github.com/docker/docker-bench-security.git")
        os.chdir("docker-bench-security")
    except Exception as e:
        print(f"Si è verificato un errore durante l'installazione del Docker Bench for Security: {str(e)}")
        sys.exit(-1)
    nome_file = "DockerBenchmarkSecurity.txt"
    try:
        print("\nAnalisi della configurazione di Docker in corso...")
        os.system(f"sudo ./docker-bench-security.sh > {path_ris}/{nome_file}")
        os.chdir("..")
        os.system("sudo rm -rf docker-bench-security")
        print(f"\nAnalisi completata\n")
        #report pdf
        add_titoletto_report(report_pdf, "Configurazione di Docker")
        testo = f"Analisi della configurazione di Docker presente nel sistema completata, trovi i risultati nel file {nome_file}"
        add_data_report(report_pdf, testo)
        testo = estrai_da_dockerbenchsec(f"{path_ris}/{nome_file}")
        add_data_report(report_pdf, testo)
        testo = "Clicca qui per registrarti e scaricare il documento"
        url = "https://www.cisecurity.org/benchmark/docker"
        add_link_report(report_pdf, testo, url)
        testo = "Ulteriori consigli e spiegazioni sono presenti al suo interno"
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione del Docker Bench for Security: {str(e)}")
        sys.exit(-1)


# Funzione che ispeziona un'immagine Docker tramite Docker CLI
def docker_inspect(path_ris, immagine, report_pdf):

    print("----------------------------------------------------------------")
    print("\nAnalisi di un'immagine Docker tramite Docker CLI\n")
    print("\nAnalisi in corso, attendere...\n")
    nome_file = "docker_inspect.json"
    try:
        os.system(f"sudo docker image inspect -f json {immagine} > {path_ris}/{nome_file}")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi dell'immagine tramite Docker CLI: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalisi completata\n")
    #report pdf
    try:
        nome_immagine = estrai_da_JSON_Docker_inspect(f"{path_ris}/{nome_file}")
        add_titoletto_report(report_pdf, f"Analisi dell'immagine {nome_immagine}")
        testo = f"Analisi dell'immagine con Docker CLI completata, trovi i risultati nel file {nome_file}.\nEsso contiene varie informazioni utili per farsi un'idea iniziale dell'immagine in analisi. È importante porre l'attenzione sulle variabili d'ambiente: campo \"Env\", che non devono contenere alcun secret (password, key) in chiaro."
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura del report: {str(e)}")
        sys.exit(-1)

# Funzione che ispeziona un'immagine Docker tramite trivy
def trivy_image(path_ris ,immagine, report_pdf):

    print("----------------------------------------------------------------")
    print("\nAnalisi di un'immagine Docker tramite Trivy\n")   
    print("\nAnalisi in corso, questo passaggio potrebbe richiedere un po' di tempo. Attendere......\n")
    nome_file = "trivy_image.json"
    nome_file2 = "trivy_image.txt"
    nome_file3 = "docker_inspect.json"
    try:
        os.system(f"sudo trivy image -f json {immagine} > {path_ris}/{nome_file}")
        os.system(f"sudo trivy image {immagine} > {path_ris}/{nome_file2}")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi dell'immagine tramite Trivy: {str(e)}")
        sys.exit(-1)
    #report pdf
    try:
        nome_immagine = estrai_da_JSON_Docker_inspect(f"{path_ris}/{nome_file3}")
        add_titoletto_report(report_pdf, f"CVE relativi all'immagine {nome_immagine}")
        testo = f"Analisi dell'immagine con trivy completata, trovi i risultati grezzi nei file {nome_file2} e {nome_file}"
        add_data_report(report_pdf, testo)
        testo, image_file = ordina_prepara_trivy_image(f"{path_ris}/{nome_file}")
        allegato_pdf = create_pdf("Elenco CVE con peso", path_ris)
        add_data_report(allegato_pdf, testo)
        save_pdf(allegato_pdf, f"{path_ris}/Allegato_CVE.pdf", "allegato")
        testo = f"Ecco un grafico che illustra i CVE analizzati, dividendoli in base al peso. Ulteriori informazioni disponibili nell'allegato \"Allegato_CVE.pdf\"\n"
        add_data_report(report_pdf, testo)
        add_image_report(report_pdf, image_file)
        print(f"\nAnalisi completata\n")
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura del report: {str(e)}")
        sys.exit(-1)

# Funzione che ispeziona tramite trivy una directory alla ricerca di vulnerabilità, secrets, misconfigurations
def trivy_fs(path_ris, report_pdf):

    print("----------------------------------------------------------------")
    print("\nTrivy: analisi della directory alla ricerca di vulnerabilità, secrets, misconfigurations")
    print("\nAnalisi in corso, attendere...\n")
    nome_file = "trivy_fs.json"
    nome_file2 = "trivy_fs.txt"
    try:
        os.system(f"sudo trivy fs -f json --scanners vuln,secret,misconfig . > {path_ris}/{nome_file}")
        os.system(f"sudo trivy fs --scanners vuln,secret,misconfig . > {path_ris}/{nome_file2}")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi di Trivy: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalisi completata\n")
    #report pdf
    try:
        add_titoletto_report(report_pdf, "Analisi del codice sorgente")
        testo = f"L'analisi del codice sorgente è stata eseguita sfruttando due tool differenti, Trivy e Semgrep.\n\nTrovi i risultati dell'analisi con Trivy nei file {nome_file2} e {nome_file}"
        add_data_report(report_pdf, testo)
        testo = estrai_da_JSON_trivy_fs(f"{path_ris}/{nome_file}")
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura del report: {str(e)}")
        sys.exit(-1)


# Funzione che ispeziona tramite semgrep il codice sorgente dell'applicazione
def semgrep_scan(path_ris, report_pdf):

    print("----------------------------------------------------------------")
    print("\nSemgrep: analisi del codice sorgente dell'applicazione\n")
    print("\nAnalisi in corso, questo passaggio potrebbe richiedere un po' di tempo. Attendere......\n")
    nome_file = "semgrep_scan.txt"
    try:
        os.system(f"semgrep scan --severity=WARNING --severity=ERROR > {path_ris}/{nome_file}")
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi di Semgrep: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalisi completata\n")
    #report pdf
    try:
        testo = f"\n-------------------\n\nTrovi i risultati dell'analisi con Semgrep nel file {nome_file}"
        add_data_report(report_pdf, testo)
        testo = estrai_da_semgrep(f"{path_ris}/{nome_file}")
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura del report: {str(e)}")
        sys.exit(-1)
