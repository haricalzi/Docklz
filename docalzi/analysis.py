import ssvc
from RPA.Browser.Selenium import Selenium

# funzione che calcola l'expoitability di un CVE
def exploitability(VulnerabilityID): 
    anno = VulnerabilityID[4:8]
    url = f"https://github.com/trickest/cve/blob/main/{anno}/{VulnerabilityID}.md"
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
    pwbi = ""

    if (pwbi == "irreversible"):
        mw_calc = 'high'
    elif (pwbi == "material" and mp in ["minimal", "support"]):
        mw_calc = 'medium'
    elif (pwbi == "minimal"):
        mw_calc = 'low' if (mp == "minimal") else 'medium'
    else:
        mw_calc = 'high'

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
    print(outcome_cutted)

    match outcome_cutted:
        case "Track":
            peso = 1
        case "Track*":
            peso = 2
        case "Attend":
            peso = 3
        case "Act":
            peso = 4
        case _:
            print("Errore, peso settato al massimo per precauzione")
            peso = 4
    
    return peso




#temporary main code
VulnerabilityID = "CVE-2023-50495"
V3Vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"
V3Score = 6.5
peso = calcolo_peso(V3Vector, VulnerabilityID)