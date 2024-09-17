import os, sys


# Function that checks if a command is already installed, if not, installs it
def check_command_installed(command):

    base_command = ["wget", "curl", "git"]
    if (command in base_command):
        check_base(command)
    elif (command == "trivy"):
        check_trivy()
    else:
        check_semgrep()


# Function that handles the check for base commands like wget, curl, git
def check_base(command):

    try:
        # Extract the package name if it exists, read to get the output from popen
        nome = os.popen(f"dpkg -l | grep -E '(^|\s){command}($|\s)' | awk '{{ print $2 }}'").read()
        if(nome != f"{command}\n"):
            print(f"{command} not installed, proceeding with installation ...\n")
            os.system(f"sudo apt -y install {command}")
    except Exception as e:
        print(f"An error occurred while installing {command}: {str(e)}")
        sys.exit(-1)


# Function that handles advanced check specific for trivy
def check_trivy():

    try:
        command = "trivy"
        # Extract the package name if it exists, read to get the output from popen
        nome = os.popen(f"dpkg -l | grep -E '(^|\s){command}($|\s)' | awk '{{ print $2 }}'").read()
        # Extract version numbers, read to get the output from popen, convert to int and compare later. Awk prints column 3, cut trims at the dot and prints column 1 or 2
        version1 = int(os.popen(f"dpkg -l | grep -E '(^|\s){command}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f1").read())
        version2 = int(os.popen(f"dpkg -l | grep -E '(^|\s){command}($|\s)' | awk '{{ print $3 }}' | cut -d '.' -f2").read())
        if(nome != f"{command}\n" or (version1 == 0 and version2 <50)):
            print(f"\n{command} not installed or not updated, proceeding with installation / update ...\n")
            os.system("wget https://github.com/aquasecurity/trivy/releases/download/v0.50.1/trivy_0.50.1_Linux-64bit.deb")
            os.system("sudo dpkg -i trivy_0.50.1_Linux-64bit.deb")
            os.system("sudo rm -f trivy_0.50.1_Linux-64bit.deb")
    except Exception as e:
        print(f"An error occurred while installing {command}: {str(e)}")
        sys.exit(-1)


# Function that handles advanced check specific to semgrep
def check_semgrep():

    try:
        command = "semgrep"
        # Extract the package name if it exists, read to get the output from popen
        nome = os.popen(f"pip list | grep -E '(^|\s){command}($|\s)' | awk '{{ print $1 }}'").read()
        # Extract version numbers, read to get the output from popen, convert to int and compare later. Awk prints column 2, cut trims at the dot and prints column 1 or 2
        version1 = int(os.popen(f"pip list | grep -E '(^|\s){command}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f1").read())
        version2 = int(os.popen(f"pip list | grep -E '(^|\s){command}($|\s)' | awk '{{ print $2 }}' | cut -d '.' -f2").read())
        if((nome != f"{command}\n") or (version1 < 1) or (version1 == 1 and version2 < 69)):
            print(f"\n{command} not installed or not updated, proceeding with installation of the latest version...\n")
            os.system("python3 -m pip install semgrep")
    except Exception as e:
        print(f"An error occurred while installing {command}: {str(e)}")
        sys.exit(-1)
