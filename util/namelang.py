#
# namelang.py
# ===========
#
# Generate the language name dictionary as a JSON object, using the full
# language tag database.
#
# Syntax
# ------
#
#   python3 namelang.py [subtag] [iso2] [iso3code] [iso3name]
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
# Then, the program adds the "him" record from ISO-639-2 that isn't
# present in the later standards, as well as the GG2 and GG3
# grandfathered records from the subtag registry
#
# Next, the program adds all the code to name mappings from ISO-639-5,
# except that language codes are normalized using the langtag module
# before they are written to the dictionary.
#
# Then, the program adds all the code to name mappings from the name
# table in ISO-639-3, except that language codes are normalized using
# the langtag module before they are written to the dictionary.  Also,
# if the inverted name is the same as the regular name, the inverted
# name is dropped so that there is no unnecessary duplication.
#
# The value of language code keys in the result dictionary is an array
# of either one or two strings.  If there is one string, it is the name
# of the language to use in all contexts.  If there are two strings, the
# second string is the "inverted" name.  For example, "Swiss German" has
# an inverted name of "German, Swiss".
#
# Names are normalized and escaped properly for inclusion in JSON string
# literals, using the prep() function defined below.  All extended
# Unicode characters are encoded using JSON Unicode escapes, so that the
# resulting data file is plain ASCII even though the names can include
# extended Unicode codepoints.
#
# Finally, the program prints the generated language name dictionary out
# to standard output as JSON text.
#

import fulldb
import io
import iso2
import iso3
import iso5
import langtag
import subtag
import sys
import unicodedata

# Function to prepare and check a name for storage in a JSON literal.
#
# This also properly escapes double quote and backslash characters.
#
# If there is a problem, an error message is displayed and the program
# is stopped.
#
# Parameters:
#
#   s : str - the name to prepare and check
#
# Return:
#
#   the prepared name, ready for storage in a JSON string literal
#
def prep(s):
  
  # Check parameter type
  if not isinstance(s, str):
    print('Invalid language name!')
    sys.exit(1)
  
  # Trim name and normalize to NFC
  s = unicodedata.normalize('NFC', s.strip())
  
  # Check that name not empty
  if len(s) < 1:
    print('Language name may not be empty!')
    sys.exit(1)
  
  # Check that no ASCII control codes, no supplementals, and no
  # surrogates
  for cc in s:
    # Get current character code
    c = ord(cc)
    
    # Check range
    if (c < 0x20) or (c == 0x7f) or \
        ((c >= 0xd800) and (c <= 0xdfff)) or \
        (c > 0xffff):
      print('Language name contains invalid codepoints!')
      sys.exit(1)
    
  # Escape backslash and double quotes
  s = s.replace('\\', '\\\\')
  s = s.replace('"', '\\"')
  
  # Escape any extended characters
  buf_size = 0
  result = ''
  for i in range(0, len(s)):
    
    # Get current character code
    c = ord(s[i])
    
    # If character code is in ASCII range, just buffer it and continue
    if c < 0x80:
      buf_size = buf_size + 1
      continue
    
    # If we got here, we need an escape, so first of all add any
    # buffered characters to result and reset buffer
    if buf_size > 0:
      result = result + s[i - buf_size:i]
      buf_size = 0
    
    # Add the Unicode escape to the result
    result += '\\u%04x' % (c)
  
  # If anything left over in buffer, add to result
  if buf_size > 0:
    result = result + s[len(s) - buf_size:len(s)]
    buf_size = 0
  
  # Return result
  return result

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

# Start the name dictionary out with just the exceptional name for "him"
# which is present in ISO-639-2 but not later standards
#
nmd = dict()
exn = iso2.code['him'][1]['en']
exn = prep(exn)
exk = langtag.norm('him')
nmd[exk] = [exn]

# Go through the subtag database and add names for grandfathered tags
# that have no preferred mapping
#
for rr in subtag.rec:
  
  # Get record fields
  r = rr[1]
  
  # Skip if not a grandfathered record
  if r['type'] != 'grandfathered':
    continue
  
  # Skip if record has a preferred mapping
  if 'preferred-value' in r:
    continue
  
  # We got a GG2 or GG3 grandfathered record, so make sure we have a
  # description and that there is only one description
  if 'description' not in r:
    print('Grandfathered tag lacks description:', r['tag'])
    sys.exit(1)
  
  if len(r['description']) != 1:
    print('Grandfathered tag has multiple descriptions:', r['tag'])
    sys.exit(1)
  
  # Add the name mapping
  exn = r['description'][0]
  exn = prep(exn)
  nmd[r['tag']] = [exn]

# Go through the ISO-639-5 database and add names for language families
#
for rr in iso5.rec:
  
  # Get record fields
  r = rr[1]
  
  # Add the name mapping
  exn = r['en']
  exn = prep(exn)
  exk = langtag.norm(r['code'])
  nmd[exk] = [exn]

# Go through the ISO-639-3 database and add everything in the name table
#
for rr in iso3.rec_name:
  
  # Get record fields
  r = rr[1]
  
  # Get relevant fields
  exk = langtag.norm(r['code3'])
  exn = prep(r['name'])
  iexn = prep(r['iname'])
  
  # Add record, but drop inverted name if same as regular name
  if exn == iexn:
    nmd[exk] = [exn]
  else:
    nmd[exk] = [exn, iexn]

# Begin the JSON output
#
jsr = io.StringIO()
jsr.write('{')

# Get a list of all the language code keys and sort them
#
tl = list(nmd)
tl.sort()

# Write all the mappings to the JSON file
#
first_rec = True
for k in tl:
  
  # Get the remapped value array
  v = nmd[k]
  
  # Write the appropriate record separator, if necessary
  if first_rec:
    jsr.write('\n')
    first_rec = False
  else:
    jsr.write(',\n')
  
  # Write the mapping
  jsr.write('  "')
  jsr.write(langtag.norm(k))
  jsr.write('": ["')
  jsr.write(v[0])
  if len(v) > 1:
    jsr.write('", "')
    jsr.write(v[1])
  jsr.write('"]')

# End the JSON output
#
jsr.write('\n}')

# Write the full JSON object to output
#
print(jsr.getvalue())
