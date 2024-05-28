import ssvc
import requests

cve = "CVE-2023-0013"
anno = cve[4:8]

URL = f"https://github.com/trickest/cve/blob/main/{anno}/{cve}.md"
 
result = requests.get(url = URL)

print(result)

data = r.json()

print(data)





decision = ssvc.Decision(
    exploitation='poc',         #none, poc, active
    automatable='no',           #yes, no
    technical_impact='total',   #partial, total
    mission_wellbeing='high',   #low, medium, high
)

outcome = decision.evaluate()

print(outcome.action)