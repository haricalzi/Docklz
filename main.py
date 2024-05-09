import argparse, sys, os
from functions import * 

#creo il parser
parser = argparse.ArgumentParser(description='Docker analisys')

#aggiungo le opzioni
parser.add_argument('-light', action="store_true", help='LIGHT: analisi della configurazione di Docker presente sul sistema')
parser.add_argument('-base', action="store", dest="immagine", help='BASE: analisi di un\'immagine Docker, specificare l\'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell\'IMAGE ID, visualizzabili con docker images)')
parser.add_argument('-base', action="store", dest="immagine", help='FULL: analisi completa di un progetto Docker (immagine + container + source code), specificare l\'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell\'IMAGE ID, visualizzabili con docker images)')
parser.add_argument('-path', action="store", dest="path_risultati", default=".", help='specificare il path assoluto/relativo di dove creare la cartella dei risultati')
parser.add_argument('-git', action="store", dest="path_github", help='specificare il path di GitHub in cui scaricare il source code (repository GitHub --> pulsante Code verde --> HTTPS)')

#parso gli argomenti e agisco di conseguenza
args = parser.parse_args()

if(args.light):
        path_ris = mkdir_results(1, args.path_risultati)
        docker_bench_security(path_ris)
elif(args.base):
        path_ris = mkdir_results(2, args.path_risultati)
        docker_inspect(path_ris, args.immagine)
        trivy_image(path_ris, args.immagine)
elif(args.full):
        path_ris = mkdir_results(3, args.path_risultati)
        if(args.git):
            git_clone_sourcecode(args.path_github)
        docker_bench_security(path_ris)
        docker_inspect(path_ris, args.immagine)
        trivy_image(path_ris, args.immagine)
        trivy_fs(path_ris)
        semgrep_scan(path_ris)
else:
        sys.exit(-1)