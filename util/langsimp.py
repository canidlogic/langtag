#
# langsimp.py
# ===========
#
# Generate the language subtag simplification dictionary as a JSON
# object, using the full language tag database.
#
# Syntax
# ------
#
#   python3 langsimp.py [subtag] [iso2] [iso3code] [iso3name]
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
# Then, the program adds the exceptional simplification mapping of "bih"
# to "bh" to the simplification dictionary.
#
# Next, the program iterates through all records in the main ISO-639-3
# code table and adds all additional simplification mappings from those
# records.
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

# Start the simplification dictionary out with just the exceptional
# mapping of bih to bh
#
smd = dict()
smd['bih'] = 'bh'

# Go through all the records in the ISO-639-3 main code table and add
# the necessary mappings to the dictionary
#
for rr in iso3.rec_code:
  
  # Get the current record fields
  r = rr[1]
  
  # Determine record type
  if ('code2' in r) and ('biblio3' in r):
    # Both a code2 and a unique biblio3 code, so map the main code and
    # the biblio3 code to the code2
    smd[r['code3']] = r['code2']
    smd[r['biblio3']] = r['code2']
    
  elif 'code2' in r:
    # Code2 but no unique biblio3 code, map the main code to code2
    smd[r['code3']] = r['code2']
    
  elif 'biblio3' in r:
    # Unique biblio3 code but no code2, so map the biblio3 code to the
    # main code
    smd[r['biblio3']] = r['code3']
    
  else:
    # Other kinds of records don't have any mappings
    pass

# Begin the JSON output
#
jsr = io.StringIO()
jsr.write('{')

# Get a list of all the remapped language subtags and sort them
#
tl = list(smd)
tl.sort()

# Write all the mappings to the JSON file
#
first_rec = True
for k in tl:
  
  # Get the remapped value
  v = smd[k]
  
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
