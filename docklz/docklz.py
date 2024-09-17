import argparse, sys, os
from .functions import *
from .check_and_install import *
from .report import *


os.system("clear")


def main():
        # Create the parser
        parser = argparse.ArgumentParser(description='Analysis of Docker images and containers')

        # Add options
        parser.add_argument('-light', action="store_true", help='LIGHT: analysis of the Docker configuration present in the system')
        parser.add_argument('-base', action="store", dest="immagine_base", help='BASE: analysis of a Docker image, specify the image to analyze (the full name of the REPOSITORY or the first characters of the IMAGE ID, viewable with "docker images")')
        parser.add_argument('-full', action="store", dest="immagine_full", help='FULL: complete analysis of a Docker project (configuration + image + source code), specify the image to analyze (the full name of the REPOSITORY or the first characters of the IMAGE ID, viewable with "docker images")')
        parser.add_argument('-pathris', action="store", dest="path_risultati", default=".", help='Allows you to specify the absolute/relative path where to create the results folder. Optional, by default, the current path is used')
        parser.add_argument('-git', action="store", dest="path_git", help='Allows you to specify the HTTPS path of a repository (e.g., GitHub, GitLab) from which to download the source code. Optional')
        parser.add_argument('-install', action="store_true", help='Allows automatic installation of commands used during the script, or check if they are already installed. Optional')

        # Parse command-line arguments
        args = parser.parse_args()

        # If no parameters are passed, print help, otherwise just the initial menu
        stampa_iniziale()
        if not (args.light or args.immagine_base or args.immagine_full or args.path_git or args.install):
                stampa_help()

        # Check if cloning from GitHub/GitLab is needed
        if(args.path_git):
                git_clone_sourcecode(args.path_git)

        # Check if more than one scan mode is specified
        if((args.light and args.immagine_base) or (args.light and args.immagine_full) or (args.immagine_base and args.immagine_full)):
                print("Error: You can specify at most one of -light, -base, -full")
        # Execute the specified option
        elif(args.light):
                # light 
                path_ris, nome_pdf = mkdir_results(args.path_risultati)
                report_pdf = create_pdf(f"REPORT {nome_pdf}", path_ris)
                if(args.install):
                        controllo_comando_installato("git")
                docker_bench_security(path_ris, report_pdf)
                save_pdf(report_pdf, f"{path_ris}/report_{nome_pdf}.pdf", "report")

        elif(args.immagine_base):
                # base  
                path_ris, nome_pdf = mkdir_results(args.path_risultati)
                report_pdf = create_pdf(f"REPORT {nome_pdf}", path_ris)
                if(args.install):
                        controllo_comando_installato("wget")
                        controllo_comando_installato("trivy") 
                docker_inspect(path_ris, args.immagine_base, report_pdf)
                trivy_image(path_ris, args.immagine_base, report_pdf)
                save_pdf(report_pdf, f"{path_ris}/report_{nome_pdf}.pdf", "report")

        elif(args.immagine_full):
                # full   
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
