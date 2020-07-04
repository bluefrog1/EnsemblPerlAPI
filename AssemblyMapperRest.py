import requests, sys, os

## This script is mapping slices from one assemblies(GRCh38) to the another(GRCh37).
## To run it use the folowing format python <species> <inputFileName>
## Example, 'python human assemblymapper.in'
  
if __name__ == '__main__':
  if len(sys.argv) == 3:
      species, inFile = sys.argv[1:]
  else:
      print('Incorrect input.')
      print('Use python <species> <inputFileName>')
      exit(0)

# Specify the original and mapping assemblies.
assemblyOriginal = 'GRCh38'
assemblyMapping  = 'GRCh37'

try:
  f = open(inFile, 'r')
except FileNotFoundError:
  print('File ' + inFile + ' does not exist')
  exit(0)

# Read the file line by line, delete spaces and comments
for line in f:
  strippedLine = line.strip().replace(' ', '')
  if len(strippedLine) > 0 and strippedLine[0] not in ['#','\n','']:
    posComment = strippedLine.find('#')
    if posComment != -1:
      strippedLine = strippedLine[:posComment-1] 

    # get the values for the request line.
    values = strippedLine.split(':')

    # if there is no start or strand, replace them with '1'     
    if not values[3]:
      values[3] = '1'
   
    if len(values) == 5:
      values.append('1')  
   
    server = "http://rest.ensembl.org"
    
    # building the request line
    ext = '/map/' + species + '/' + assemblyOriginal + '/'

    ext +=  values[2] + ':'   # seq_region_name
    ext +=  values[3] + '..'  # start
    ext +=  values[4] + ':'   # end
    ext +=  values[5] + '/'   # strand

    ext += assemblyMapping + '?'

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
    if not r.ok:
      r.raise_for_status()
      sys.exit()
 
    decoded = r.json()
    print(repr(decoded))

f.close()
