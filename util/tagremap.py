#
# tagremap.py
# ===========
#
# Generate the tag remapping dictionary as a JSON object, using the
# subtag registry.
#
# Syntax
# ------
#
#   python3 tagremap.py [datapath]
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
# the records of type "grandfathered" and "redundant" that have a
# "Preferred-Value" field.  The "tag" field in these records serves as
# the remapping dictionary key while the "preferred-value" field serves
# as the value the key maps to.
#
# Finally, the program prints the generated tag remapping dictionary out
# to standard output as JSON text.
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
  
  # Skip if this is not a grandfathered or redundant record
  if (r['type'] != 'grandfathered') and (r['type'] != 'redundant'):
    continue
  
  # Skip if there is no preferred-value mapping
  if 'preferred-value' not in r:
    continue
  
  # We found the record so print the mapping -- no escaping is necessary
  # since language tags just have alphanumeric characters and hyphens
  if first_rec:
    jsr.write('\n')
    first_rec = False
  else:
    jsr.write(',\n')
  jsr.write('  "')
  jsr.write(r['tag'])
  jsr.write('": "')
  jsr.write(r['preferred-value'])
  jsr.write('"')

# End the JSON output
#
jsr.write('\n}')

# Write the full JSON object to output
#
print(jsr.getvalue())
