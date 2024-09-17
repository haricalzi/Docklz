import os, sys


# Function that checks if a command is already installed, if not, installs it
def controllo_comando_installato(comando):

    comandi_base = ["wget", "curl", "git"]
    if (comando in comandi_base):
        controllo_base(comando)
    elif (comando == "trivy"):
        controllo_trivy()
    else:
        controllo_semgrep()


# Function that handles the check for base commands like wget, curl, git
def controllo_base(comando):

    try:
        # Extract the package name if it exists, read to get the output from popen
        nome = os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}'").read()
        if(nome != f"{comando}\n"):
            print(f"{comando} not installed, proceeding with installation ...\n")
            os.system(f"sudo apt -y install {comando}")
    except Exception as e:
        print(f"An error occurred while installing {comando}: {str(e)}")
        sys.exit(-1)


# Function that handles advanced check specific for trivy
def controllo_trivy():

    try:
        comando = "trivy"
        # Extract the package name if it exists, read to get the output from popen
        nome = os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}'").read()
        # Extract version numbers, read to get the output from popen, convert to int and compare later. Awk prints column 3, cut trims at the dot and prints column 1 or 2
        versione1 = int(os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f1").read())
        versione2 = int(os.popen(f"dpkg -l | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f2").read())
        if(nome != f"{comando}\n" or (versione1 == 0 and versione2 <50)):
            print(f"\n{comando} not installed or not updated, proceeding with installation / update ...\n")
            os.system("wget https://github.com/aquasecurity/trivy/releases/download/v0.50.1/trivy_0.50.1_Linux-64bit.deb")
            os.system("sudo dpkg -i trivy_0.50.1_Linux-64bit.deb")
            os.system("sudo rm -f trivy_0.50.1_Linux-64bit.deb")
    except Exception as e:
        print(f"An error occurred while installing {comando}: {str(e)}")
        sys.exit(-1)


# Function that handles advanced check specific to semgrep
def controllo_semgrep():

    try:
        comando = "semgrep"
        # Extract the package name if it exists, read to get the output from popen
        nome = os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $1 }}'").read()
        # Extract version numbers, read to get the output from popen, convert to int and compare later. Awk prints column 2, cut trims at the dot and prints column 1 or 2
        versione1 = int(os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f1").read())
        versione2 = int(os.popen(f"pip list | grep -E '(^|\s){comando}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f2").read())
        if((nome != f"{comando}\n") or (versione1 < 1) or (versione1 == 1 and versione2 < 69)):
            print(f"\n{comando} not installed or not updated, proceeding with installation of the latest version...\n")
            os.system("python3 -m pip install semgrep")
    except Exception as e:
        print(f"An error occurred while installing {comando}: {str(e)}")
        sys.exit(-1)
