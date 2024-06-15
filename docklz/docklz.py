import argparse, sys, os
from .functions import *
from .check_and_install import *
from .report import *


os.system("clear")

def main():
        #creo il parser
        parser = argparse.ArgumentParser(description='Analisi di immagini e container Docker')

        #aggiungo le opzioni
        parser.add_argument('-light', action="store_true", help='LIGHT: analisi della configurazione di Docker presente nel sistema')
        parser.add_argument('-base', action="store", dest="immagine_base", help='BASE: analisi di un\'immagine Docker, specificare l\'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell\'IMAGE ID, visualizzabili con "docker images")')
        parser.add_argument('-full', action="store", dest="immagine_full", help='FULL: analisi completa di un progetto Docker (configurazione + immagine + source code), specificare l\'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell\'IMAGE ID, visualizzabili con "docker images")')
        parser.add_argument('-pathris', action="store", dest="path_risultati", default=".", help='Permette di specificare il path assoluto/relativo in cui creare la cartella dei risultati. Di default viene considerato quello attuale')
        parser.add_argument('-git', action="store", dest="path_git", help='Permette di specificare il path HTTPS di una repository (es. GitHub, GitLab) da cui scaricare il source code. Opzionale, non utilizzare se è già presente il source code')
        parser.add_argument('-install', action="store_true", help='Permette di installare in automatico i comandi utilizzati durante lo script, oppure controllare se sono già installati')

        #parso gli argomenti passati da linea di comando
        args = parser.parse_args()

        #se passo il comando senza parametri stampo anche l'help, altrimenti solo il menù iniziale
        stampa_iniziale()
        if not (args.light or args.immagine_base or args.immagine_full or args.path_git or args.install):
                stampa_help()
        
        #controllo se devo clonare da GitHub / GitLab
        if(args.path_git):
                git_clone_sourcecode(args.path_git)

        #controllo di non aver specificato più modalità di scansione
        if((args.light and args.immagine_base) or (args.light and args.immagine_full) or (args.immagine_base and args.immagine_full)):
                print("Errore: puoi specificare al massimo uno tra -light, -base, -immagine_full")
        #eseguo l'opzione specificata
        elif(args.light):
                #light 
                path_ris, nome_pdf = mkdir_results(args.path_risultati)
                report_pdf = create_pdf(f"REPORT {nome_pdf}", path_ris)
                if(args.install):
                        controllo_comando_installato("git")
                docker_bench_security(path_ris, report_pdf)
                save_pdf(report_pdf, f"{path_ris}/report_{nome_pdf}.pdf", "report")

        elif(args.immagine_base):
                #base  
                path_ris, nome_pdf = mkdir_results(args.path_risultati)
                report_pdf = create_pdf(f"REPORT {nome_pdf}", path_ris)
                if(args.install):
                        controllo_comando_installato("wget")
                        controllo_comando_installato("trivy") 
                docker_inspect(path_ris, args.immagine_base, report_pdf)
                trivy_image(path_ris, args.immagine_base, report_pdf)
                save_pdf(report_pdf, f"{path_ris}/report_{nome_pdf}.pdf", "report")

        elif(args.immagine_full):
                #full   
                path_ris, nome_pdf = mkdir_results(args.path_risultati)
                report_pdf = create_pdf(f"REPORT {nome_pdf}", path_ris)
                if(args.install):
                        controllo_comando_installato("wget")
                        controllo_comando_installato("trivy")
                        controllo_comando_installato("semgrep") 
                docker_bench_security(path_ris, report_pdf)
                docker_inspect(path_ris, args.immagine_full, report_pdf)
                trivy_image(path_ris, args.immagine_full, report_pdf)
                trivy_fs(path_ris, report_pdf)
                semgrep_scan(path_ris, report_pdf)
                save_pdf(report_pdf, f"{path_ris}/report_{nome_pdf}.pdf", "report")
        else:
                sys.exit(-1)
        
        os.system("sudo rm -rf CVE_peso_grafico.png")
        print("----------------------------------------------------------------")

if __name__ == "__main__":
    main()
