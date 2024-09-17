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
    name_dir = "results"
    print("\n----------------------------------------------------------------")

    if not os.path.exists(name_dir):
        try:
            os.mkdir(name_dir)
            print(f"\nCreating a folder called \"{name_dir}\", containing the results of the various scans")
        except OSError as e:
            print(f"Error during the creation of the folder \"{name_dir}\": {e}")
            sys.exit(-1) 
    
    name_subdir = date_hour()

    if not os.path.exists(f"{name_dir}/{name_subdir}"):
        try:
            os.chdir(name_dir)
            os.mkdir(name_subdir)
            print(f"\nCreating a folder called \"{name_subdir}\" inside \"{name_dir}\", containing the results of the current scan\n")
        except OSError as e:
            print(f"Error during the creation of the folder \"{name_subdir}\": {e}")
            os.chdir(actual)
            sys.exit(-1)

    os.chdir(actual)

    return f"{tosave}/{name_dir}/{name_subdir}", f"{name_subdir}"


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
def date_hour():

    try:
        current = datetime.now()
        return f"{current.day}-{current.month}-{current.year}__{current.hour}-{current.minute}-{current.second}"
    except Exception as e:
        print(f"Error during the generation of date and time: {e}")
        sys.exit(-1)


# Function that prints the initial message
def print_initial():

    print("\n\n--------------------------------------------------")
    print("-------------------- DOCKLZ ----------------------")
    print("--------------------------------------------------")
    print("----- SECURITY ANALISYS OF DOCKER CONTAINERS -----")
    print("--------------------------------------------------\n\n")


# Function that prints the help menu
def print_help():

    print("--------------------------------------------------")
    print("------------ 'docklz -h' -->  help ---------------")
    print("--------------------------------------------------\n\n")


# Function that performs a Docker configuration check using Docker Bench for Security
def docker_bench_security(path_res, report_pdf):

    print("----------------------------------------------------------------")
    try:
        print("\nInstalling Docker Bench for Security\n")
        os.system("git clone https://github.com/docker/docker-bench-security.git")
        os.chdir("docker-bench-security")
    except Exception as e:
        print(f"An error occurred while installing Docker Bench for Security: {str(e)}")
        sys.exit(-1)
    file_name = "DockerBenchmarkSecurity.txt"
    try:
        print("\nRunning Docker configuration analysis...")
        os.system(f"sudo ./docker-bench-security.sh > {path_res}/{file_name}")
        os.chdir("..")
        os.system("sudo rm -rf docker-bench-security")
        print(f"\nAnalysis completed\n")
        # PDF report
        add_little_title_report(report_pdf, "Docker Configuration")
        text = f"Docker configuration analysis completed. Results can be found in the file {file_name}"
        add_data_report(report_pdf, text)
        text = extract_from_dockerbenchsec(f"{path_res}/{file_name}")
        add_data_report(report_pdf, text)
        text = "Click here to register and download the document"
        url = "https://www.cisecurity.org/benchmark/docker"
        add_link_report(report_pdf, text, url)
        text = "Additional advice and explanations are provided within"
        add_data_report(report_pdf, text)
    except Exception as e:
        print(f"An error occurred while running Docker Bench for Security: {str(e)}")
        sys.exit(-1)


# Function that inspects a Docker image using Docker CLI
def docker_inspect(path_res, image, report_pdf):

    print("----------------------------------------------------------------")
    print("\nInspecting a Docker image using Docker CLI\n")
    print("\nAnalysis in progress, please wait...\n")
    file_name = "docker_inspect.json"
    try:
        os.system(f"sudo docker image inspect -f json {image} > {path_res}/{file_name}")
    except Exception as e:
        print(f"An error occurred while analyzing the image using Docker CLI: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalysis completed\n")
    # PDF report
    try:
        image_name = extract_from_JSON_Docker_inspect(f"{path_res}/{file_name}")
        add_little_title_report(report_pdf, f"Image {image_name} analysis")
        text = f"Image analysis with Docker CLI completed. Results can be found in the file {file_name}.\nIt contains various useful pieces of information to get an initial idea of the image being analyzed. Pay special attention to the environment variables: 'Env' field, which should not contain any secrets (passwords, keys) in plaintext."
        add_data_report(report_pdf, text)
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)

# Function that inspects a Docker image using Trivy
def trivy_image(path_res, image, report_pdf):

    print("----------------------------------------------------------------")
    print("\nAnalyzing a Docker image with Trivy\n")   
    print("\nAnalysis in progress, this step may take some time. Please wait......\n")
    file_name = "trivy_image.json"
    file_name2 = "trivy_image.txt"
    file_name3 = "docker_inspect.json"
    try:
        os.system(f"sudo trivy image -f json {image} > {path_res}/{file_name}")
        os.system(f"sudo trivy image {image} > {path_res}/{file_name2}")
    except Exception as e:
        print(f"An error occurred during the image analysis with Trivy: {str(e)}")
        sys.exit(-1)
    # PDF report
    try:
        image_name = extract_from_JSON_Docker_inspect(f"{path_res}/{file_name3}")
        add_little_title_report(report_pdf, f"CVE related to the image {image_name}")
        text = f"Trivy image analysis completed. Raw results can be found in files {file_name2} and {file_name}."
        add_data_report(report_pdf, text)
        text, image_file = order_prepare_trivy_image(f"{path_res}/{file_name}")
        attachment_pdf = create_pdf("CVE List by Severity", path_res)
        add_data_report(attachment_pdf, text)
        save_pdf(attachment_pdf, f"{path_res}/attachment_CVE.pdf", "attachment")
        text = f"Here is a chart illustrating the analyzed CVEs, categorized by severity. Further information is available in the attachment \"attachment_CVE.pdf\"\n"
        add_data_report(report_pdf, text)
        add_image_report(report_pdf, image_file)
        print(f"\nAnalysis completed\n")
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)

# Function that inspects a directory with Trivy for vulnerabilities, secrets, and misconfigurations
def trivy_fs(path_res, report_pdf):

    print("----------------------------------------------------------------")
    print("\nTrivy: Analyzing the directory for vulnerabilities, secrets, and misconfigurations")
    print("\nAnalysis in progress, please wait...\n")
    file_name = "trivy_fs.json"
    file_name2 = "trivy_fs.txt"
    try:
        os.system(f"sudo trivy fs -f json --scanners vuln,secret,misconfig . > {path_res}/{file_name}")
        os.system(f"sudo trivy fs --scanners vuln,secret,misconfig . > {path_res}/{file_name2}")
    except Exception as e:
        print(f"An error occurred during the Trivy analysis: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalysis completed\n")
    # PDF report
    try:
        add_little_title_report(report_pdf, "Source Code Analysis")
        text = f"The source code analysis was performed using two different tools, Trivy and Semgrep.\n\nThe results of the Trivy analysis can be find in files {file_name2} and {file_name}."
        add_data_report(report_pdf, text)
        text = extract_from_JSON_trivy_fs(f"{path_res}/{file_name}")
        add_data_report(report_pdf, text)
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)


# Function that inspects the application's source code with Semgrep
def semgrep_scan(path_res, report_pdf):

    print("----------------------------------------------------------------")
    print("\nSemgrep: Analyzing the application's source code\n")
    print("\nAnalysis in progress, this step may take some time. Please wait......\n")
    file_name = "semgrep_scan.txt"
    try:
        os.system(f"semgrep scan --severity=WARNING --severity=ERROR > {path_res}/{file_name}")
    except Exception as e:
        print(f"An error occurred during the Semgrep analysis: {str(e)}")
        sys.exit(-1)
    print(f"\nAnalysis completed\n")
    # PDF report
    try:
        text = f"\n-------------------\n\nThe results of the Semgrep analysis can be find in the file {file_name}"
        add_data_report(report_pdf, text)
        text = extract_from_semgrep(f"{path_res}/{file_name}")
        add_data_report(report_pdf, text)
    except Exception as e:
        print(f"An error occurred while writing the report: {str(e)}")
        sys.exit(-1)
