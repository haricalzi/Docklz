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
    parser.add_argument('-base', action="store", dest="image_base", help='BASE: analysis of a Docker image, specify the image to analyze (the full name of the REPOSITORY or the first characters of the IMAGE ID, viewable with "docker images")')
    parser.add_argument('-full', action="store", dest="image_full", help='FULL: complete analysis of a Docker project (configuration + image + source code), specify the image to analyze (the full name of the REPOSITORY or the first characters of the IMAGE ID, viewable with "docker images")')
    parser.add_argument('-pathres', action="store", dest="path_results", default=".", help='Allows you to specify the absolute/relative path where to create the results folder. By default, the current path is used')
    parser.add_argument('-git', action="store", dest="path_git", help='Allows you to specify the HTTPS path of a repository (e.g., GitHub, GitLab) from which to download the source code. Optional, do not use if the source code is already present')
    parser.add_argument('-install', action="store_true", help='Allows automatic installation of commands used during the script, or check if they are already installed')

    # Parse command-line arguments
    args = parser.parse_args()

    # If no parameters are passed, print help, otherwise just the initial menu
    print_initial()
    if not (args.light or args.image_base or args.image_full or args.path_git or args.install):
        print_help()
    
    # Check if cloning from GitHub/GitLab is needed
    if(args.path_git):
        git_clone_sourcecode(args.path_git)

    # Check if more than one scan mode is specified
    if((args.light and args.image_base) or (args.light and args.image_full) or (args.image_base and args.image_full)):
        print("Error: You can specify at most one of -light, -base, -full")
    # Execute the specified option
    elif(args.light):
        # light 
        path_res, pdf_name = mkdir_results(args.path_results)
        report_pdf = create_pdf(f"REPORT {pdf_name}", path_res)
        if(args.install):
            check_command_installed("git")
        docker_bench_security(path_res, report_pdf)
        save_pdf(report_pdf, f"{path_res}/report_{pdf_name}.pdf", "report")

    elif(args.image_base):
        # base  
        path_res, pdf_name = mkdir_results(args.path_results)
        report_pdf = create_pdf(f"REPORT {pdf_name}", path_res)
        if(args.install):
            check_command_installed("wget")
            check_command_installed("trivy") 
        docker_inspect(path_res, args.image_base, report_pdf)
        trivy_image(path_res, args.image_base, report_pdf)
        save_pdf(report_pdf, f"{path_res}/report_{pdf_name}.pdf", "report")

    elif(args.image_full):
        # full   
        path_res, pdf_name = mkdir_results(args.path_results)
        report_pdf = create_pdf(f"REPORT {pdf_name}", path_res)
        if(args.install):
            check_command_installed("wget")
            check_command_installed("trivy")
            check_command_installed("semgrep") 
        docker_bench_security(path_res, report_pdf)
        docker_inspect(path_res, args.image_full, report_pdf)
        trivy_image(path_res, args.image_full, report_pdf)
        trivy_fs(path_res, report_pdf)
        semgrep_scan(path_res, report_pdf)
        save_pdf(report_pdf, f"{path_res}/report_{pdf_name}.pdf", "report")
    else:
        sys.exit(-1)
    
    os.system("sudo rm -rf CVE_weight_chart.png")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    main()
