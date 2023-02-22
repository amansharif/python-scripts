import subprocess
import json
import pandas as pd

raw_vulnerability = ["kubectl", "get", "vulnerabilityreports", "-A", "-ojson"]
f = open("raw_vulnerability.json", "w")
subprocess.run(raw_vulnerability, stdout=f)
f.close()

with open('raw_vulnerability.json', 'r') as file:
    data = json.load(file)

file = open("vulnerability_summary.csv", "w")
file.write(f"namespace, image_registry, image_repository , image_tag_digest, critical, high, medium, low, unkown, vulnerability_id, vul_title, severity, resource, link, installedVersion, fixedVersions\n")

for item in data['items']:
    #image
    namespace = item['metadata']['namespace']
    registry = item['report']['registry']['server']
    repository = item['report']['artifact']['repository']
    #some have tags some have digest
    try:
        image_tag = item['report']['artifact']['tag']
    except:
        image_tag = item['report']['artifact']['digest']
    #vulnerability counts
    critical_vul = item['report']['summary']['criticalCount']
    high_vul = item['report']['summary']['highCount']
    medium_vul = item['report']['summary']['mediumCount']
    low_vul = item['report']['summary']['lowCount']
    unknown_vul = item['report']['summary']['unknownCount']

    for vul in item['report']['vulnerabilities']:
        vul_id = vul['vulnerabilityID']
        #comma separated string
        vul_title_tmp = vul['title']
        vul_title = vul_title_tmp.replace(",", " ")
        severity = vul['severity']
        resrource = vul['resource']
        #some miss primaryLink
        try:
            link = vul['primaryLink']
        except:
            link = ""
        insVer = vul['installedVersion']
        #comma separated multiple versions
        fixVer_temp = vul['fixedVersion']
        fixVer = fixVer_temp.replace(",", " ")
        
        vul_summary = f"{namespace}, {registry}, {repository}, {image_tag}, {critical_vul}, {high_vul}, {medium_vul}, {low_vul}, {unknown_vul}, {vul_id}, {vul_title}, {severity}, {resrource}, {link}, {insVer}, {fixVer}\n"
        
        file.write(vul_summary)

file.close()

# reading the csv file
cvsDataframe = pd.read_csv('vulnerability_summary.csv')

# creating an output excel file
resultExcelFile = pd.ExcelWriter('vulnerability_summary.xlsx')

# converting the csv file to an excel file
cvsDataframe.to_excel(resultExcelFile, index=False)

# saving the excel file
resultExcelFile.save()

