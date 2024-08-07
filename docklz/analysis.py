import ssvc, json, os, sys, aiohttp, asyncio
from .report import *


# Funzione che calcola l'expoitability di un CVE
async def exploitability(session, semaphore, VulnerabilityID): 
    anno = VulnerabilityID[4:8]
    url = f"https://github.com/trickest/cve/blob/main/{anno}/{VulnerabilityID}.md"

    async with semaphore:
        try:
            async with session.get(url) as response:
                print(f"Analisi {VulnerabilityID} in corso")
                if response.status == 404:
                    exploit_calc = 'none'
                else:
                    exploit_calc = 'poc'
        except aiohttp.ClientError as e:
            print(f"Errore durante la richiesta: {e}")
            exploit_calc = 'none'

    return exploit_calc


# Funzione che calcola l'automatibility di un CVE
def automatibility(V3Vector):

    try:
        ui = V3Vector[27]

        if(ui == 'N'):
            automation_calc = 'yes'
        else:
            automation_calc = 'no'
        
        return automation_calc
    except Exception as e:
        print(f"Si è verificato un errore durante il calcolo dell'automatibility di un CVE: {str(e)}")
        sys.exit(-1)

# Funzione che calcola il technical impact di un CVE
def technical_impact(V3Vector):

    try:
        confidentiality = V3Vector[35]
        integrity = V3Vector[39]
        availability = V3Vector[43]

        impact_values = {
            "H": 0.56,
            "L": 0.22,
            "N": 0.0
        }

        confidentiality_value = impact_values.get(confidentiality, 0.0)
        integrity_value = impact_values.get(integrity, 0.0)
        availability_value = impact_values.get(availability, 0.0)

        # Impact Sub-Score
        iss = 1 - ((1 - confidentiality_value) * (1 - integrity_value) * (1 - availability_value))

        # soglia per l'iss
        threshold = 0.67

        if (iss > threshold):
            ti_calc = 'total'
        else:
            ti_calc = 'partial'

        return ti_calc
    except Exception as e:
        print(f"Si è verificato un errore durante il calcolo del technical impact di un CVE: {str(e)}")
        sys.exit(-1)


# Funzione che calcola il mission wellbeing di un CVE
def mission_wellbeing(V3Vector):

    # mission prevalence (minimal, support, essential), rilevanza dell'oggetto vulnerabile all'interno del progetto, default = essential (livello massimo)
    mp = "essential" 
    # pubblic well-being impact (minimal, material, irrevesible), impatto dei sistemi compromessi sull'uomo, default = irreversible (livello massimo)
    pwbi = "irreversible"

    mw_calc = 'high'

    # nel caso venisse implementato un modo per calcolare mp e pwbi, decommentare la parte sottostante

    # if (pwbi == "irreversible"):
    #     mw_calc = 'high'
    # elif (pwbi == "material" and mp in ["minimal", "support"]):
    #     mw_calc = 'medium'
    # elif (pwbi == "minimal"):
    #     mw_calc = 'low' if (mp == "minimal") else 'medium'
    # else:
    #     mw_calc = 'high'

    return mw_calc


# Funzione che calcola il peso da associare ad ogni CVE
async def calcolo_peso(session, semaphore, V3Vector, VulnerabilityID):
    try:
        exploit = await exploitability(session, semaphore, VulnerabilityID)

        decision = ssvc.Decision(
            exploitation=exploit,                           # none, poc, (active)   --> from trickest on github
            automatable=automatibility(V3Vector),           # yes, no               --> from V3Vector, human interaction field
            technical_impact=technical_impact(V3Vector),    # partial, total        --> from V3Vector, Confidentiality, Integrity, Availability fields
            mission_wellbeing=mission_wellbeing(V3Vector),  # low, medium, high     --> default ad high
        )

        outcome = decision.evaluate()
        outcome_cutted = str(outcome.action)[11:]
        
        match outcome_cutted:
            case "TRACK":
                peso = 0
            case "TRACK_STAR":
                peso = 1
            case "ATTEND":
                peso = 2
            case "ACT":
                peso = 3
            case _:
                print("Errore, peso settato al massimo per precauzione")
                peso = 3
        
        return peso
    except Exception as e:
        print(f"Si è verificato un errore durante il calcolo del peso di un CVE: {str(e)}")
        sys.exit(-1)


# Funzione che estrae CVE e relative informazioni dal json generato da trivy image
def estrai_CVE_da_JSON_Trivy_image(json_file):
    try:
        vulnerabilities_dict = {}

        with open(json_file, 'r') as file:
            data = json.load(file)

        for result in data['Results']:
            if 'Vulnerabilities' in result:
                for vulnerability in result['Vulnerabilities']:
                    vulnerability_id = vulnerability.get('VulnerabilityID', '')
                    
                    if vulnerability_id not in vulnerabilities_dict:
                        title = vulnerability.get('Title', '')
                        description = vulnerability.get('Description', '')
                        severity = vulnerability.get('Severity', '')

                        if 'redhat' in vulnerability.get('CVSS', {}):
                            redhat_cvss = vulnerability['CVSS']['redhat']
                            v3vector = redhat_cvss.get('V3Vector', '')
                            v3score = redhat_cvss.get('V3Score', '')
                        else:
                            v3vector = vulnerability.get('CVSS', {}).get('nvd', {}).get('V3Vector', '')
                            v3score = vulnerability.get('CVSS', {}).get('nvd', {}).get('V3Score', '')

                        # Valori di default se non presenti i precedenti
                        v3vector = v3vector if v3vector else '-1'
                        v3score = v3score if v3score else '-1'

                        # Aggiunge il dizionario al dizionario delle vulnerabilità
                        vulnerabilities_dict[vulnerability_id] = {
                            'VulnerabilityID': vulnerability_id,
                            'Title': title,
                            'Description': description,
                            'Severity': severity,
                            'V3Vector': v3vector,
                            'V3Score': v3score
                        }
            
        return list(vulnerabilities_dict.values())
    except Exception as e:
        print(f"Si è verificato un errore durante l'estrazione dei CVE dal JSON di Trivy image: {str(e)}")
        sys.exit(-1)


# Funzione che analizza le info di un CVE e ne calcola il peso
async def analisi_CVE(vulnerabilities_list):
    try:
        new_vulnerabilities_list = []
        semaphore = asyncio.Semaphore(4) #limite connessioni in simultanea
        async with aiohttp.ClientSession() as session:
            tasks = []
            for vulnerability in vulnerabilities_list:
                if vulnerability['V3Vector'] != "-1" and vulnerability['V3Score'] != "-1":
                    tasks.append(calcolo_peso(session, semaphore, vulnerability['V3Vector'], vulnerability['VulnerabilityID']))
                else:
                    tasks.append(asyncio.sleep(0, result=0))

            pesi = await asyncio.gather(*tasks)

            for vulnerability, peso in zip(vulnerabilities_list, pesi):
                vulnerability['Peso'] = peso
                new_vulnerabilities_list.append(vulnerability)
            print("\nAnalisi CVE completata\n") 

        return new_vulnerabilities_list
    except Exception as e:
        print(f"Si è verificato un errore durante l'analisi dei CVE: {str(e)}")
        sys.exit(-1)


# Funzione che unisce le precedenti, ordina per peso decrescente e prepara il testo da stampare
def ordina_prepara_trivy_image(json_file):

    try: 
        peso3 = 0
        peso2 = 0
        peso1 = 0
        peso0 = 0
        vulnerabilities_list = estrai_CVE_da_JSON_Trivy_image(json_file)
        if vulnerabilities_list:
            vulnerabilities_list_peso = asyncio.run(analisi_CVE(vulnerabilities_list))
            #ordinamento decrescente per peso
            vulnerabilities_list_sorted = sorted(vulnerabilities_list_peso, key=lambda x: x['Peso'], reverse=True)
            #testo per report
            testo = f"\nL'immagine analizzata è risultata potenzialmente vulnerabile a {len(vulnerabilities_list_sorted)} CVE. Vengono ordinati in ordine decrescente di peso [max=3, min=0], un parametro calcolato che stima la rilevanza del CVE ed indica quanto è urgente effettuare delle azioni di mitigazione\n\n-------------------"
            for vulnerability in vulnerabilities_list_sorted:
                match vulnerability['Peso']:
                    case 3:
                        peso = "3 - Agire immediatamente"
                        peso3 += 1
                    case 2:
                        peso = "2 - Monitorare e pianificare l'intervento"
                        peso2 += 1
                    case 1:
                        peso = "1 - Monitorare la vulnerabilità"
                        peso1 += 1
                    case 0:
                        peso = "0 - Situazione sotto controllo"
                        peso0 += 1
                image_file = make_graph(peso3, peso2, peso1, peso0)
                testo += f"\nVulnerabilityID: {vulnerability['VulnerabilityID']}\n"
                testo += f"Title: {vulnerability['Title']}\n"
                testo += f"Peso: {peso}\n"
                testo += "-------------------"       
        else:
            testo = "\nL'immagine non è risultata vulnerabile a nessun CVE"

        return testo, image_file
    except Exception as e:
        print(f"Si è verificato un errore durante l'associazione del peso ai CVE: {str(e)}")
        sys.exit(-1)


# Funzione che estrae il nome dell'immagine dal json generato da docker inspect
def estrai_da_JSON_Docker_inspect(json_file):
    
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        if 'RepoTags' in data[0]:
            repotags = data[0]['RepoTags'][0].replace("[","").replace("]","")
        else:
            repotags = "ERRORE"

        return repotags
    except Exception as e:
        print(f"Si è verificato un errore durante l'estrazione del nome dell'immagine analizzata: {str(e)}")
        sys.exit(-1)

# Funzione che estrae le eventuali problematiche rilevate nel JSON prodotto da Trivy fs
def estrai_da_JSON_trivy_fs(json_file):

    with open(json_file, 'r') as file:
        data = json.load(file)

    if 'Title' in data:
        testo = f"Ecco le principali problematiche rilevate da Trivy:\n{estrai_titoli(data, testo)}"
    else:
        testo = "Non è stata rilevata alcuna problematica tramite questa analisi"
    return testo


# Funzione che estrae i titoli dato il contenuto di un JSON in modo ricorsivo
def estrai_titoli(data, testo):
    
    try:
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'Title':
                    testo += f"- {value}\n"
                else:
                    testo = estrai_titoli(value, testo)
        elif isinstance(data, list):
            for element in data:
                testo = estrai_titoli(element, testo)
            
        return testo
    except Exception as e:
        print(f"Si è verificato un errore durante l'estrazione dei titoli dal Json: {str(e)}")
        sys.exit(-1)
        

# Funzione che estrae le eventuali problematiche rilevate nel txt prodotto da Semgrep
def estrai_da_semgrep(txt_file):

    try:
        titoli = []

        with open(txt_file, 'r') as file:
            if (os.path.getsize(txt_file) == 0):
                testo = "Non è stata rilevata alcuna problematica tramite questa analisi"
            else:
                testo = "Ecco le principali problematiche rilevate:\n"
                for line in file:
                    line = line.strip()
                    if line.startswith('❯❯❱'):
                        titolo = line[4:]
                    elif line.startswith('❯❱'):
                        titolo = line[3:]
                    elif line.startswith('❯'):
                        titolo = line[1:]
                    elif line.startswith('❱'):
                        titolo = line[1:]
                    else:
                        continue

                    titolo = titolo.replace('.', ' ').replace('-', ' ')
                    if titolo not in titoli:
                        titoli.append(titolo)
                        testo += f"- {titolo}\n"
                    
        return testo
    except Exception as e:
        print(f"Si è verificato un errore durante l'estrazione da Semgrep: {str(e)}")
        sys.exit(-1)


# Funzione che estrae il numero di problematiche dal Docker Bench for Security
def estrai_da_dockerbenchsec(txt_file):

    try:
        with open(txt_file, 'r') as file:
            content = file.read()
        warn_count = content.count("[WARN]")
        if (warn_count == 0):
            testo = "Non sono stati rilevati problemi nella configurazione di Docker"
        else:
            testo = f"Sono stati rilevati {warn_count} problemi nella configurazione di Docker.\nControllare nel file le voci con esito WARN e confrontare con il CIS Docker Benchmark v1.6.0"

        return testo
    except Exception as e:
        print(f"Si è verificato un errore durante l'estrazione del numero di problematiche dal Docker Bench for Security: {str(e)}")
        sys.exit(-1)
