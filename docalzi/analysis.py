import ssvc


cve = "CVE-2023-0013"
anno = cve[4:8]



decision = ssvc.Decision(
    exploitation='poc',
    automatable='no',
    technical_impact='total',
    mission_wellbeing='high',
)

outcome = decision.evaluate()

print(outcome.action)