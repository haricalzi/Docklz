import os, sys
from datetime import datetime
from .check_and_install import *
from .analysis import *
from .report import *


# Function that creates the results folder
def mkdir_results(path):

    actual = os.getcwd()
    os.chdir(path)
    tosave = os.getcwd() 
    nome_dir = "results"
    print("\n----------------------------------------------------------------")

    if not os.path.exists(nome_dir):
        try:
            os.mkdir(nome_dir)
            print(f"\nCreating a folder called \"{nome_dir}\", containing the results of the various scans")
        except OSError as e:
            print(f"Error during the creation of the folder \"{nome_dir}\": {e}")
            sys.exit(-1) 
    
    nome_sottodir = data_ora()

    if not os.path.exists(f"{nome_dir}/{nome_sottodir}"):
        try:
            os.chdir(nome_dir)
            os.mkdir(nome_sottodir)
            print(f"\nCreating a folder called \"{nome_sottodir}\" inside \"{nome_dir}\", containing the results of the current scan\n")
        except OSError as e:
            print(f"Error during the creation of the folder \"{nome_sottodir}\": {e}")
            os.chdir(actual)
            sys.exit(-1)

    os.chdir(actual)

    return f"{tosave}/{nome_dir}/{nome_sottodir}", f"{nome_sottodir}"


# Function that clones a repository (HTTPS path)
def git_clone_sourcecode(path_git):

    print("----------------------------------------------------------------\n")
    try:
        os.system(f"git clone {path_git}")
        print("\ngit clone successfully completed")
    except Exception as e:
        print(f"Error during git clone execution: {str(e)}")
        sys.exit(-1)


# Function that handles date and time to create unique files and folders to avoid overwriting
def data_ora():

    try:
        attuale = datetime.now()
        return f"{attuale.day}-{attuale.month}-{attuale.year}__{attuale.hour}-{attuale.minute}-{attuale.second}"
    except Exception as e:
        print(f"Error during the generation of date and time: {e}")
        sys.exit(-1)


# Function that prints the initial message
def stampa_iniziale():

    print("\n\n--------------------------------------------------")
    print("-------------------- DOCKLZ ----------------------")
    print("--------------------------------------------------")
    print("----- SECURITY ANALISYS OF DOCKER CONTAINERS -----")
    print("--------------------------------------------------\n\n")


# Function that prints the help menu
def stampa_help():

    print("--------------------------------------------------")
    print("------------ 'docklz -h' -->  help ---------------")
    print("--------------------------------------------------\n\n")


# Function that performs a Docker configuration check using Docker Bench for Security
def docker_bench_security(path_ris, report_pdf):

    print("----------------------------------------------------------------")
    try:
        print("\nInstalling Docker Bench for Security\n")
        os.system("git clone https://github.com/docker/docker-bench-security.git")
        os.chdir("docker-bench-security")
    except Exception as e:
        print(f"An error occurred while installing Docker Bench for Security: {str(e)}")
        sys.exit(-1)
    nome_file = "DockerBenchmarkSecurity.txt"
    try:
        print("\nRunning Docker configuration analysis...")
        os.system(f"sudo ./docker-bench-security.sh > {path_ris}/{nome_file}")
        os.chdir("..")
        os.system("sudo rm -rf docker-bench-security")
        print(f"\nAnalysis completed\n")
        # PDF report
        add_titoletto_report(report_pdf, "Docker Configuration")
        testo = f"Docker configuration analysis completed. Results can be found in the file {nome_file}"
        add_data_report(report_pdf, testo)
        testo = estrai_da_dockerbenchsec(f"{path_ris}/{nome_file}")
        add_data_report(report_pdf, testo)
        testo = "Click here to register and download the document"
        url = "https://www.cisecurity.org/benchmark/docker"
        add_link_report(report_pdf, testo, url)
        testo = "Additional advice and explanations are provided within"
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"An error occurred while running Docker Bench for Security: {str(e)}")
        sys.exit(-1)


# Function that inspects a Docker image using Docker CLI
def docker_inspect(path_ris, immagine, report_pdf):

    print("----------------------------------------------------------------")
    print("\nInspecting a Docker image using Docker CLI\n")
    print("\nAnalysis in progress, please wait...\n")
    nome_file = "docker_inspect.json"
    try:
        os.system(f"sudo docker image inspect -f json {immagine} > {path_ris}/{nome_file}")
    except Exception as e:
        print(f"An error occurred while analyzing the image using Docker CLI: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalysis completed\n")
    # PDF report
    try:
        nome_immagine = estrai_da_JSON_Docker_inspect(f"{path_ris}/{nome_file}")
        add_titoletto_report(report_pdf, f"Image {nome_immagine} analysis")
        testo = f"Image analysis with Docker CLI completed. Results can be found in the file {nome_file}.\nIt contains various useful pieces of information to get an initial idea of the image being analyzed. Pay special attention to the environment variables: 'Env' field, which should not contain any secrets (passwords, keys) in plaintext."
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)

# Function that inspects a Docker image using Trivy
def trivy_image(path_ris, immagine, report_pdf):

    print("----------------------------------------------------------------")
    print("\nAnalyzing a Docker image with Trivy\n")   
    print("\nAnalysis in progress, this step may take some time. Please wait......\n")
    nome_file = "trivy_image.json"
    nome_file2 = "trivy_image.txt"
    nome_file3 = "docker_inspect.json"
    try:
        os.system(f"sudo trivy image -f json {immagine} > {path_ris}/{nome_file}")
        os.system(f"sudo trivy image {immagine} > {path_ris}/{nome_file2}")
    except Exception as e:
        print(f"An error occurred during the image analysis with Trivy: {str(e)}")
        sys.exit(-1)
    # PDF report
    try:
        nome_immagine = estrai_da_JSON_Docker_inspect(f"{path_ris}/{nome_file3}")
        add_titoletto_report(report_pdf, f"CVE related to the image {nome_immagine}")
        testo = f"Trivy image analysis completed. Raw results can be found in files {nome_file2} and {nome_file}."
        add_data_report(report_pdf, testo)
        testo, image_file = ordina_prepara_trivy_image(f"{path_ris}/{nome_file}")
        allegato_pdf = create_pdf("CVE List by Severity", path_ris)
        add_data_report(allegato_pdf, testo)
        save_pdf(allegato_pdf, f"{path_ris}/Allegato_CVE.pdf", "allegato")
        testo = f"Here is a chart illustrating the analyzed CVEs, categorized by severity. Further information is available in the attachment \"Allegato_CVE.pdf\"\n"
        add_data_report(report_pdf, testo)
        add_image_report(report_pdf, image_file)
        print(f"\nAnalysis completed\n")
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)

# Function that inspects a directory with Trivy for vulnerabilities, secrets, and misconfigurations
def trivy_fs(path_ris, report_pdf):

    print("----------------------------------------------------------------")
    print("\nTrivy: Analyzing the directory for vulnerabilities, secrets, and misconfigurations")
    print("\nAnalysis in progress, please wait...\n")
    nome_file = "trivy_fs.json"
    nome_file2 = "trivy_fs.txt"
    try:
        os.system(f"sudo trivy fs -f json --scanners vuln,secret,misconfig . > {path_ris}/{nome_file}")
        os.system(f"sudo trivy fs --scanners vuln,secret,misconfig . > {path_ris}/{nome_file2}")
    except Exception as e:
        print(f"An error occurred during the Trivy analysis: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalysis completed\n")
    # PDF report
    try:
        add_titoletto_report(report_pdf, "Source Code Analysis")
        testo = f"The source code analysis was performed using two different tools, Trivy and Semgrep.\n\nThe results of the Trivy analysis can be find in files {nome_file2} and {nome_file}."
        add_data_report(report_pdf, testo)
        testo = estrai_da_JSON_trivy_fs(f"{path_ris}/{nome_file}")
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)


# Function that inspects the application's source code with Semgrep
def semgrep_scan(path_ris, report_pdf):

    print("----------------------------------------------------------------")
    print("\nSemgrep: Analyzing the application's source code\n")
    print("\nAnalysis in progress, this step may take some time. Please wait......\n")
    nome_file = "semgrep_scan.txt"
    try:
        os.system(f"semgrep scan --severity=WARNING --severity=ERROR > {path_ris}/{nome_file}")
    except Exception as e:
        print(f"An error occurred during the Semgrep analysis: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalysis completed\n")
    # PDF report
    try:
        testo = f"\n-------------------\n\nThe results of the Semgrep analysis can be find in the file {nome_file}"
        add_data_report(report_pdf, testo)
        testo = estrai_da_semgrep(f"{path_ris}/{nome_file}")
        add_data_report(report_pdf, testo)
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)
