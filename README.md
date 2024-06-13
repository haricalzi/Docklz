# Analisi di immagini e container Docker
Strumento che effettua analisi di sicurezza relative a immagini e container Docker in modo automatizzato.

Docklz si basa su alcuni tool già esistenti, come [Docker Bench of Security](https://github.com/docker/docker-bench-security), [Trivy](https://github.com/aquasecurity/trivy), [Semgrep](https://github.com/semgrep/semgrep).

### Note importanti
- prerequisito: sul sistema devono essere installati e configurati correttamente **Docker** e **Python (>=3.11)**
- potrebbe essere richiesta la password di root in alcuni passaggi, in quanto alcuni comandi necessitano di **sudo** per essere eseguiti
- a seconda della tipologia di analisi scelta possono essere necessari alcuni comandi (*wget*, *curl*, *pip*, *trivy*, *semgrep*), i quali possono essere installati automaticamente tramite un'opzione, vedi sezione *Opzioni di Docklz*:

### Setup ed utilizzo
1. clonare la repository
2. spostarsi nella directory appena creata
3. utilizare il comando `pip install .` per installare `docklz` all'interno del sistema
4. spostarsi nella directory da analizzare (in cui è presente il source code)
5. utilizzare il comando `docklz` per eseguire la scansione
6. nella cartella *results* è presente il **report** della scansione, oltre ai risultati grezzi di ogni tool

### Opzioni di `Docklz`:
|Opzione|Descrizione|
|:---|:---|
|`-h, --help`|Stampa il messaggio di help|
|`-light`|LIGHT: analisi della configurazione di Docker presente sul sistema|
|`-base [nome immagine]`| BASE: analisi di un'immagine Docker, specificare l'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID, visualizzabili con `docker images`)|
|`-full [nome immagine]`|FULL: analisi completa di un progetto Docker (immagine + container + source code), specificare l'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID, visualizzabili con `docker images`)|
|`-path [path risultati]`|Permette di specificare il path assoluto/relativo in cui creare la cartella dei risultati. Di default viene considerato quello attuale|
|`-git [path HHTPS github]`|Permette di specificare il path di GitHub da cui scaricare il source code. Opzionale, non utilizzare se è già presente il source code|

### Sviluppatore
Ideato e sviluppato da *Hari Calzi*, uno studente universitario.
Per qualsiasi informazione, segnalazione o possibile miglioramento:
- [GitHub](https://github.com/haricalzi)
- [Linkedin](https://www.linkedin.com/in/haricalzi/)
