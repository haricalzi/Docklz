Analisi di immagini e container Docker, realizzato da Hari Calzi

options:

  -h, --help  -->  show this help message and exit
  
  -light  -->  LIGHT: analisi della configurazione di Docker presente sul sistema
  
  -base IMMAGINE  -->  BASE: analisi di un'immagine Docker, specificare l'immagine da analizzare (il nome completo della REPOSITORY oppure i primi caratteri     
   dell'IMAGE ID, visualizzabili con docker images)
  
  -full IMMAGINE  -->  FULL: analisi completa di un progetto Docker (immagine + container + source code), specificare l'immagine da analizzare (il nome completo 
   della REPOSITORY oppure i primi caratteri dell'IMAGE ID, visualizzabili con "docker images")
  
  -path PATH_RISULTATI  -->  Permette di specificare il path assoluto/relativo di dove creare la cartella dei risultati. Di default viene considerato quello attuale
  
  -git PATH_GITHUB  -->  Permette di specificare il path di GitHub in cui scaricare il source code (repository GitHub --> pulsante Code verde --> HTTPS). Opzionale,      non utilizzare se è già presente il source code
