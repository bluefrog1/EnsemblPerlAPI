import requests, sys
 
server = "http://rest.ensembl.org"
ext = "/map/human/GRCh38/10:25000..30000:1/GRCh37?"

r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
if not r.ok:
  r.raise_for_status()
  sys.exit()
 
decoded = r.json()
print(repr(decoded))