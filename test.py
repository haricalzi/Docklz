import requests

def verifica_link(link):
    try:
        response = requests.get(link)
        if response.status_code == 404:
            print("Non trovato")
        else:
            print("Trovato")
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")

# Esempio di utilizzo
link = "https://github.com/trickest/cve/blob/main/2024/CVE-2024-0010.md"
verifica_link(link)