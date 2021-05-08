#
# langremap.py
# ============
#
# Generate the language subtag remapping dictionary as a JSON object,
# using the full language tag database.
#
# Syntax
# ------
#
#   python3 langremap.py [subtag] [iso2] [iso3code] [iso3name]
#     [iso3macro] [iso3retire] [iso5]
#
# [subtag] is the path to the subtag registry data file.  See the subtag
# module for further information.
#
# [iso2] is the path to the ISO-639-2 data file.  See the iso2 module
# for further information.
#
# [iso3code] is the path to the ISO-639-3 main code table file.  See the
# iso3 module for further information.
#
# [iso3name] is the path to the ISO-639-3 name table file.  See the iso3
# module for further information.
#
# [iso3macro] is the path to the ISO-639-3 macrolanguage table file.
# See the iso3 module for further information.
#
# [iso3retire] is the path to the ISO-639-3 retirements table file.  See
# the iso3 module for further information.
#
# [iso5] is the path to the ISO-639-5 data file.  See the iso5 module
# for further information.
#
# Operation
# ---------
#
# This program begins by using the fulldb module to load the full
# language tag database into memory and check for consistency.
#
# Then, the program iterates through all the "language" records in the
# subtag registry that have a "preferred-value" field.  For language
# subtags that have two characters, the program adds those archaic tag
# mappings to the dictionary.  For language subtags with three
# characters, the program simply makes sure that equivalent mappings
# exist in the (automatically corrected) ISO-639-3 retirements table,
# except for the adp language tag, which maps to the "dz" in the subtag
# registry but maps to its three-letter equivalent code "dzo" in the
# ISO-639-3 retirements table.
#
# Next, the program iterates through all records in the ISO-639-3
# retirements table that have a "mapping" field.  All these mappings are
# recorded in the dictionary, except that the "adp" record is altered to
# map to the equivalent two-letter code "dz" instead.
#
# Finally, the program prints the generated language remapping
# dictionary out to standard output as JSON text.
#

import fulldb
import io
import iso2
import iso3
import iso5
import subtag
import sys

# Check that we have exactly seven parameters
#
if len(sys.argv) != 8:
  print('Wrong number of program arguments!')
  sys.exit(1)

# Fill in all the data file paths
#
dfp = fulldb.DataFilePaths()

dfp.subtag_path = sys.argv[1]
dfp.iso2_path = sys.argv[2]
dfp.iso3_code_path = sys.argv[3]
dfp.iso3_name_path = sys.argv[4]
dfp.iso3_macro_path = sys.argv[5]
dfp.iso3_retire_path = sys.argv[6]
dfp.iso5_path = sys.argv[7]

# Completely load the language tag database into memory from all the
# data files and check consistency
#
try:
  fulldb.parse_all(dfp)

except fulldb.FullDBError as fde:
  print('Error while loading full database!')
  print(fde)
  sys.exit(1)

except iso2.ISO2Error as i2e:
  print('Error loading ISO-639-2 data file!')
  print(i2e)
  sys.exit(1)

except iso3.ISO3Error as i3e:
  print('Error loading ISO-639-3 data files!')
  print(i3e)
  sys.exit(1)
  
except iso5.ISO5Error as i5e:
  print('Error loading ISO-639-5 data file!')
  print(i5e)
  sys.exit(1)
  
except subtag.SubtagError as ste:
  print('Error loading subtag registry!')
  print(ste)
  sys.exit(1)

# Start the language remapping dictionary out empty
#
rmd = dict()

# Go through all the records in the subtag registry, add archaic tags to
# the dictionary, and check that other mappings are consistent with
# ISO-639-3
#
for sr in subtag.rec:
  
  # Get the current record fields
  r = sr[1]
  
  # Skip if not a language subtag record
  if r['type'] != 'language':
    continue
  
  # Skip if record has no preferred-value mapping
  if 'preferred-value' not in r:
    continue
  
  # Check length of language subtag to determine what to do
  if len(r['subtag']) == 2:
    # Archaic tag mapping, so add it to the dictionary
    rmd[r['subtag']] = r['preferred-value']
    
  elif len(r['subtag']) == 3:
    # Regular mapping, so check that it is in the ISO-639-3 retirements
    # table and that it has a mapping
    if r['subtag'] not in iso3.code_retire:
      print('Subtag mappings are not proper subset!')
      sys.exit(1)
    
    if 'mapping' not in iso3.code_retire[r['subtag']][1]:
      print('Subtag mappings are inconsistent with ISO-639-3!')
      sys.exit(1)
    
    # Except for the code "adp", check that ISO-639-3 retirements table
    # has an equivalent mapping; for "adp", add the mapping from the
    # subtag registry
    if r['subtag'] == 'adp':
      rmd[r['subtag']] = r['preferred-value']
    
    else:
      if r['preferred-value'] != \
          iso3.code_retire[r['subtag']][1]['mapping']:
        print('Subtag mappings are inconsistent with ISO-639-3!')
        sys.exit(1)
    
  else:
    # Shouldn't happen
    print('Invalid subtag found in subtag registry!')
    sys.exit(1)

# Go through all the records in the ISO-639-3 retirements table and add
# them to the dictionary
#
for rr in iso3.rec_retire:
  
  # Get the current record fields
  r = rr[1]
  
  # Skip if no mapping field
  if 'mapping' not in r:
    continue
  
  # For exceptional case of adp, skip because we added the mapping
  # earlier from the subtag registry
  if r['code3'] == 'adp':
    continue
  
  # If we get here, record the mapping normally; the iso3 module has
  # automatically performed the needed corrections for us
  rmd[r['code3']] = r['mapping']

# Begin the JSON output
#
jsr = io.StringIO()
jsr.write('{')

# Get a list of all the remapped language subtags and sort them
#
tl = list(rmd)
tl.sort()

# Write all the mappings to the JSON file
#
first_rec = True
for k in tl:
  
  # Get the remapped value
  v = rmd[k]
  
  # Write the appropriate record separator, if necessary
  if first_rec:
    jsr.write('\n')
    first_rec = False
  else:
    jsr.write(',\n')
  
  # Write the mapping -- no escaping is necessary since language subtags
  # just have lowercase ASCII letters
  jsr.write('  "')
  jsr.write(k)
  jsr.write('": "')
  jsr.write(v)
  jsr.write('"')

# End the JSON output
#
jsr.write('\n}')

# Write the full JSON object to output
#
print(jsr.getvalue())
