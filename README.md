# Static analysis of Docker images and containers
Docklz is a tool that performs automated security analysis of Docker images and containers.

It's based on some existing tools, such as [Docker Bench for Security](https://github.com/docker/docker-bench-security), [Trivy](https://github.com/aquasecurity/trivy), [Semgrep](https://github.com/semgrep/semgrep).

### Relevant notes
- Prerequisite: the system must have the following tools installed and properly configured: **Docker** and **Python (>=3.11)**
- The root password may be required at certain steps, as some commands need **sudo** privileges to be executed.
- Depending on the type of analysis selected, some commands (*wget*, *curl*, *pip*, *trivy*, *semgrep*) may be required. These can be automatically installed through an option, refer to the *Docklz Options* section for more details.

### Setup and Usage
1. Clone the repository: `git clone https://github.com/haricalzi/Docklz.git`
2. Use the command `pip install Docklz/` to install `docklz` on your system
3. Run the command `docklz` to execute the scan
4. The **report** of the scan, along with raw results from each tool, can be found in the *results* folder

### Docklz Options

| Option | Description |
|:---|:---|
| `-h, --help` | Prints the help message |
| `-light` | LIGHT: analyzes the Docker configuration present on the system |
| `-base [image name]` | BASE: analyzes a Docker image; specify the image to be analyzed (either the full REPOSITORY name or the first few characters of the IMAGE ID, which can be viewed with `docker images`) |
| `-full [image name]` | FULL: performs a complete analysis of a Docker project (configuration + image + source code); specify the image to be analyzed (either the full REPOSITORY name or the first few characters of the IMAGE ID, which can be viewed with `docker images`) |
| `-pathres [results path]` | Allows specifying the absolute/relative path where the results folder will be created. Optional, by default, the current directory is used |
| `-git [HTTPS repository path]` | Allows specifying the HTTPS path of a repository (e.g., GitHub, GitLab) from which to download the source code. (Optional) |
| `-install` | Allows automatic installation of commands used during the script, or checks if they are already installed. (Optional) |

### Usage Examples
| Example | Description |
|:---|:---|
| `docklz -light` | LIGHT scan |
| `docklz -base nginx:latest` | BASE scan specifying the full image name |
| `docklz -full a06` | FULL scan specifying the first few characters of the IMAGE ID |
| `docklz -base f77 -pathres dir/var` | BASE scan specifying the path where to save the results |
| `docklz -full h99 -install -git https://github.com/quay/clair.git` | FULL scan specifying the installation of necessary tools and cloning the source code from the provided repository |

### Planned Future Implementations
| List |
|:---|
| AI integration into the results analysis phase |
| Improvement of technical impact calculation |
| Calculation of mission prevalence |
| Calculation of public well-being impact |
| Additional metrics for evaluating CVEs |
| Optimization of execution time |

### Credits
Created and developed by *Hari Calzi*, a university student. For any information, feedback, or potential improvements:
- calzihari@gmail.com
- [GitHub](https://github.com/haricalzi)
- [LinkedIn](https://www.linkedin.com/in/haricalzi/)
