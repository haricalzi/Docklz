import ssvc


cve = "CVE-2023-0013"
anno = cve[4:8]

req = f"https://github.com/trickest/cve/blob/main/{anno}/{cve}.md"

decision = ssvc.Decision(
    exploitation='poc',         #none, poc, active
    automatable='no',           #yes, no
    technical_impact='total',   #partial, total
    mission_wellbeing='high',   #low, medium, high
)

outcome = decision.evaluate()

print(outcome.action)