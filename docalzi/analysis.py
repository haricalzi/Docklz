import ssvc
from RPA.Browser.Selenium import Selenium

cve = "CVE-2023-0049"
anno = cve[4:8]

url = f"https://github.com/trickest/cve/blob/main/{anno}/{cve}.md"


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
        exploitable='none'
    else:
        exploitable='poc'
except Exception as e:
    print(f"Si è verificato un errore: {e}")
finally:
    browser.close_all_browsers()


decision = ssvc.Decision(
    exploitation=exploitable,   # none, poc, (active) --> from trickest on github
    automatable='no',           # yes, no
    technical_impact='total',   # partial, total
    mission_wellbeing='high',   # low, medium, high
)

outcome = decision.evaluate()
outcome_cutted = str(outcome.action)[11:]
print(outcome_cutted)