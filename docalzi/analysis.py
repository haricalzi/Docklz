import ssvc
from RPA.Browser.Selenium import Selenium

VulnerabilityID = "CVE-2023-50495"
V3Vector = "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"
V3Score = 6.5


# expoitability
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


# automatibility
ui = V3Vector[27]

if(ui == 'N'):
    automation_calc = 'no'
else:
    automation_calc = 'yes'


# technical impact
confidentiality = V3Vector[35]
integrity = V3Vector[39]
availability = V3Vector[43]

if(confidentiality == "H" or integrity == "H" or availability == "H"):
    ti_calc = 'total'
else:
    ti_calc = 'partial'


# mission wellbeing
mp = ""
pwbi = ""

if (pwbi == "irreversible"):
    mw_calc = 'high'
elif (pwbi == "material" and mp in ["minimal", "support"]):
    mw_calc = 'medium'
elif (pwbi == "minimal"):
    mw_calc = 'low' if (mp == "minimal") else 'medium'
else:
    mw_calc = 'high'

print(mw_calc)

# final decision
decision = ssvc.Decision(
    exploitation = exploit_calc,    # none, poc, (active)   --> from trickest on github
    automatable = automation_calc,  # yes, no               --> from V3Vector, human interaction field
    technical_impact = ti_calc,     # partial, total        --> from V3Vector, Confidentiality, Integrity, Availability fields
    mission_wellbeing = mw_calc,    # low, medium, high
)

outcome = decision.evaluate()
outcome_cutted = str(outcome.action)[11:]
print(outcome_cutted)