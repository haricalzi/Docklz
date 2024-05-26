import argparse, sys, os
from .functions import *
from .check_and_install import *

def main():
        #creo il parser
        parser = argparse.ArgumentParser(description='Analisi di immagini e container Docker')

        #aggiungo le opzioni
        parser.add_argument('-light', action="store_true", help='LIGHT: analisi della configurazione di Docker presente sul sistema')
        parser.add_argument('-base', action="store", dest="immagine_base", help='BASE: analisi di un\'immagine Docker, specificare l\'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell\'IMAGE ID, visualizzabili con docker images)')
        parser.add_argument('-full', action="store", dest="immagine_full", help='FULL: analisi completa di un progetto Docker (immagine + container + source code), specificare l\'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell\'IMAGE ID, visualizzabili con "docker images")')
        parser.add_argument('-path', action="store", dest="path_risultati", default=".", help='Permette di specificare il path assoluto/relativo di dove creare la cartella dei risultati. Di default viene considerato quello attuale')
        parser.add_argument('-git', action="store", dest="path_github", help='Permette di specificare il path di GitHub in cui scaricare il source code (repository GitHub --> pulsante Code verde --> HTTPS). Opzionale, non utilizzare se è già presente il source code')
        parser.add_argument('-install', action="store_true", help='Permette di installare in automatico i comandi utilizzati durante lo script, oppure controllare se sono già installati')

        #parso gli argomenti passati da linea di comando
        args = parser.parse_args()

        #se passo il comando senza parametri stampo anche l'help, altrimenti solo il menù iniziale
        stampa_iniziale()
        if not (args.light or args.immagine_base or args.immagine_full):
                stampa_help()

        #controllo di non aver specificato più modalità di scansione
        if((args.light and args.immagine_base) or (args.light and args.immagine_full) or (args.immagine_base and args.immagine_full)):
                print("Errore: puoi specificare al massimo uno tra -light, -base, -immagine_full")
        elif(args.light):
                #light 
                path_ris = mkdir_results(1, args.path_risultati)
                if(args.install):
                        controllo_comando_installato("git")
                docker_bench_security(path_ris)
        elif(args.immagine_base):
                #base  
                path_ris = mkdir_results(2, args.path_risultati)
                if(args.install):
                        controllo_comando_installato("wget")
                        controllo_comando_installato("trivy") 
                docker_inspect(path_ris, args.immagine_base)
                trivy_image(path_ris, args.immagine_base)
        elif(args.immagine_full):
                #full   
                path_ris = mkdir_results(3, args.path_risultati)
                if(args.path_github):
                        git_clone_sourcecode(args.path_github)
                if(args.install):
                        controllo_comando_installato("wget")
                        controllo_comando_installato("trivy")
                        controllo_comando_installato("semgrep") 
                docker_bench_security(path_ris)
                docker_inspect(path_ris, args.immagine_full)
                trivy_image(path_ris, args.immagine_full)
                trivy_fs(path_ris)
                semgrep_scan(path_ris)
        else:
                sys.exit(-1)

        print("----------------------------------------------------------------")


if __name__ == "__main__":
    main()
