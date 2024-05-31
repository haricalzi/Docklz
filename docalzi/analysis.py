import ssvc
from RPA.Browser.Selenium import Selenium
import json

# funzione che estrae il nome dell'immagine dal json generato da docker inspect
def estrai_da_JSON_Docker_inspect(json_file):

    with open(json_file, 'r') as file:
        data = json.load(file)

    return data['RepoTags']


# funzione che estrae cve e relative informazioni dal json generato da trivy image
def estrai_CVE_da_JSON_Trivy_image(json_file):
    #lista per salvare i dati estratti
    vulnerabilities_list = []

    with open(json_file, 'r') as file:
        data = json.load(file)

    #itera sulle vulnerabilità
    for result in data['Results']:
        for vulnerability in result['Vulnerabilities']:
            #estrazione dei dati
            vulnerability_id = vulnerability.get('VulnerabilityID', '')
            title = vulnerability.get('Title', '')
            description = vulnerability.get('Description', '')
            severity = vulnerability.get('Severity', '')
            
            #verifica se ci sono dati CVSS specifici per Red Hat
            if 'redhat' in vulnerability.get('CVSS', {}):
                redhat_cvss = vulnerability['CVSS']['redhat']
                v3vector = redhat_cvss.get('V3Vector', '')
                v3score = redhat_cvss.get('V3Score', '')
            else:
                #altrimenti, utilizza i dati CVSS standard
                v3vector = vulnerability.get('CVSS', {}).get('nvd', {}).get('V3Vector', '')
                v3score = vulnerability.get('CVSS', {}).get('nvd', {}).get('V3Score', '')
            
            #valori di default se non presenti i precedenti
            v3vector = v3vector if v3vector else '-1'
            v3score = v3score if v3score else '-1'

            #aggiunge il dizionario alla lista
            vulnerabilities_list.append({
                'VulnerabilityID': vulnerability_id,
                'Title': title,
                'Description': description,
                'Severity': severity,
                'V3Vector': v3vector,
                'V3Score': v3score
            })
    
    return vulnerabilities_list


# funzione che analizza le info di un CVE e ne calcola il peso
def analisi_CVE(vulnerabilities_list):
    new_vulnerabilities_list = []
    threshold = 20

    for vulnerability in vulnerabilities_list:
        if vulnerability['V3Vector'] != "-1" and vulnerability['V3Score'] != "-1":
            if len(vulnerabilities_list) < threshold or vulnerability['Severity'] in ["CRITICAL", "HIGH"]:
                peso = calcolo_peso(vulnerability['V3Vector'], vulnerability['VulnerabilityID'])
            else:
                peso = 1
        else:
            peso = 0
            
        vulnerability['Peso'] = peso
        new_vulnerabilities_list.append(vulnerability)
    
    return new_vulnerabilities_list


# funzione che calcola l'expoitability di un CVE
def exploitability(VulnerabilityID): 
    anno = VulnerabilityID[4:8]
    url = f"https://github.com/trickest/cve/blob/main/{anno}/{VulnerabilityID}.md"
    print(url)
    browser = Selenium()
    options = {
            "arguments": ["--headless"]
        }
    try:

        browser.open_available_browser(url, options=options)

        browser.wait_until_element_is_visible("tag:body", timeout=20)

        search_text1 = "No PoCs found on GitHub currently"
        search_text2 = "No PoCs from references"
        page_source = browser.get_source()

        if search_text1 in page_source and search_text2 in page_source:
            exploit_calc='none'
        else:
            exploit_calc='poc'
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
    finally:
        browser.close_all_browsers()

    return exploit_calc


# funzione che calcola l'automatibility di un CVE
def automatibility(V3Vector):
    ui = V3Vector[27]

    if(ui == 'N'):
        automation_calc = 'no'
    else:
        automation_calc = 'yes'
    
    return automation_calc


# funzione che calcola il technical impact di un CVE
def technical_impact(V3Vector):
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


# funzione che calcola il mission wellbeing di un CVE
def mission_wellbeing(V3Vector):
    # mission prevalence (minimal, support, essential), rilevanza dell'oggetto vulnerabile all'interno del progetto, default = essential (livello massimo)
    mp = "essential" 
    # impatto dei sistemi compromessi sull'uomo, default = irreversible (livello massimo)
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


# funzione che calcola il peso da associare ad ogni CVE
def calcolo_peso(V3Vector, VulnerabilityID):
    decision = ssvc.Decision(
        exploitation = exploitability(VulnerabilityID),     # none, poc, (active)   --> from trickest on github
        automatable = automatibility(V3Vector),             # yes, no               --> from V3Vector, human interaction field
        technical_impact = technical_impact(V3Vector),      # partial, total        --> from V3Vector, Confidentiality, Integrity, Availability fields
        mission_wellbeing = mission_wellbeing(V3Vector),    # low, medium, high
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
            peso = 4
    
    return peso
