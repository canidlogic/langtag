#
# dropscript.py
# =============
#
# Generate the script suppression dictionary as a JSON object, using the
# subtag registry.
#
# Syntax
# ------
#
#   python3 dropscript.py [datapath]
#
# [datapath] is the path to the subtag registry data file.  See the
# subtag module for further information.
#
# Operation
# ---------
#
# This program begins by using the subtag module to load and parse the
# subtag registry data file.
#
# Then, the program iterates through all the parsed records to find all
# the records of type "language" that have a "Suppress-Script" field.
# The "subtag" field in these records serves as the script suppression
# dictionary key while the "suppress-script" field serves as the value
# the key maps to.
#
# Finally, the program prints the generated script suppression 
# dictionary out to standard output as JSON text.
#

import io
import subtag
import sys

# Check that we have exactly one parameter
#
if len(sys.argv) != 2:
  print('Wrong number of program arguments!')
  sys.exit(1)

# Get the parameter
#
fpath = sys.argv[1]

# Load the subtag registry
#
try:
  subtag.parse(fpath)

except subtag.SubtagError as exc:
  print('Error while loading subtag registry:')
  print(exc)
  sys.exit(1)

# Begin the JSON output
#
jsr = io.StringIO()
jsr.write('{')

# Go through the parsed subtag records and build the dictionary entries
#
first_rec = True
for rr in subtag.rec:
  
  # Get current record fields
  r = rr[1]
  
  # Skip if this is not a language record
  if r['type'] != 'language':
    continue
  
  # Skip if there is no suppress-script field
  if 'suppress-script' not in r:
    continue
  
  # We found the record so print the mapping -- no escaping is necessary
  # since subtags just have alphanumeric characters
  if first_rec:
    jsr.write('\n')
    first_rec = False
  else:
    jsr.write(',\n')
  jsr.write('  "')
  jsr.write(r['subtag'])
  jsr.write('": "')
  jsr.write(r['suppress-script'])
  jsr.write('"')

# End the JSON output
#
jsr.write('\n}')

# Write the full JSON object to output
#
print(jsr.getvalue())
