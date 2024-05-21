# Analisi di immagini e container Docker

### Note importanti
- si presuppone che sul sistema siano già stati installati e configurati correttamente **Docker** e **Python**
- potrebbe essere richiesta la password di root in alcuni passaggi, in quanto alcuni comandi necessitano di sudo per essere eseguiti
- lo script installa in automatico, nel caso non presenti ed in caso di necessità, i seguenti programmi: wget, curl, pip, trivy, semgrep. In caso di problemi, procedere manualmente con l'installazione e la configurazione, poi avviare nuovamente lo script

### Setup
1. clonare la repository
2. spostarsi nella directory appena creata
3. utilizare il comando `pip install .`
4. spostarsi nella directory da analizzare
5. utilizzare il comando `docalzi` per eseguire le scansioni

### Opzioni di `docalzi`:
`-h, --help`  -->  show this help message and exit

`-light`  -->  LIGHT: analisi della configurazione di Docker presente sul sistema
  
`-base [nome_immagine]`  -->  BASE: analisi di un'immagine Docker, specificare l'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID, visualizzabili con docker images)
  
`-full [nome_immagine]`  -->  FULL: analisi completa di un progetto Docker (immagine + container + source code), specificare l'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri dell'IMAGE ID, visualizzabili con "docker images")
  
`-path [path_risultati]`  -->  Permette di specificare il path assoluto/relativo di dove creare la cartella dei risultati. Di default viene considerato quello attuale
  
`-git [path_github]`  -->  Permette di specificare il path di GitHub in cui scaricare il source code (repository GitHub --> pulsante Code verde --> HTTPS). Opzionale, non utilizzare se è già presente il source code
