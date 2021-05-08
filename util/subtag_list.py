#
# subtag_list.py
# ==============
#
# Syntax:
#
#   python3 subtag_list.py [datapath] ([category])
#   python3 subtag_list.py [datapath] remap ([category])
#
#   The [datapath] parameter is the file path to the subtag registry
#   file that will be parsed with the subtag.py module.  See the
#   documentation in that module for further information.
#
#   The optional [category] parameter is either "language", "extlang",
#   "script", "region", "variant", "grandfathered" or "redundant".  If
#   specified, only records matching the given type will be displayed.
#   If the parameter is not given, all records will be displayed.
#
#   The [category] parameter also allows for a special virtual category
#   called "uvar".  This is a subset of "variant" that only includes
#   variant records that have no prefixes.
#
#   The remap invocation displays only record remappings.
#
# Operation
# ---------
#
# First, the subtag registry is parsed into records using the subtag.py
# module.
#
# Second, this module lists the tags or subtags of all the records.  If
# the optional [category] parameter was provided to the program, only
# records matching that type will be listed.
#

# Import modules
#
import subtag
import sys

#
# Local functions
# ---------------
#

# Check whether the given parameter is a string that is a case-sensitive
# match for one of the valid category names.
#
# Parameters:
#
#   cname : str | mixed - the value to check
#
# Return:
#
#   True if value is a string that is recognized, False otherwise
#
def valid_category(cname):
  if not isinstance(cname, str):
    return False
  if (cname == 'language') or (cname == 'extlang') or \
      (cname =='script') or (cname == 'region') or \
      (cname == 'variant') or (cname == 'grandfathered') or \
      (cname == 'redundant'):
    return True
  else:
    return False

#
# Program entrypoint
# ------------------
#

# Check parameter count
#
if (len(sys.argv) < 2) or (len(sys.argv) > 4):
  print('Wrong number of program arguments!')
  sys.exit(1)

# Get the arguments
#
arg_data_path = sys.argv[1]

arg_remap = False
arg_uvar = False
arg_category = None

if len(sys.argv) >= 4:
  if sys.argv[2] != 'remap':
    print('Unrecognized argument!')
    sys.exit(1)
  arg_remap = True
  arg_category = sys.argv[3]
  
elif len(sys.argv) == 3:
  if sys.argv[2] == 'remap':
    arg_remap = True
  else:
    arg_category = sys.argv[2]

# If we got a category argument, convert to lowercase, trim, and make
# sure it is one of the approved types; also, handle the virtual
# category uvar
#
if arg_category is not None:
  arg_category = arg_category.strip(' \t')
  arg_category = arg_category.lower()
  if arg_category == 'uvar':
    arg_uvar = True
    arg_category = 'variant'
  if not valid_category(arg_category):
    print('Invalid category name!')
    sys.exit(1)

# Parse the input data file
#
try:
  subtag.parse(arg_data_path)
except subtag.SubtagError as se:
  print(se)
  sys.exit(1)

# Go through all parsed records
#
for r in subtag.rec:
  
  # Get fields of parsed record
  f = r[1]
  
  # Get type value
  tval = f['type']
  
  # Read either tag or subtag field
  tname = None
  if (tval == 'grandfathered') or (tval == 'redundant'):
    tname = f['tag']
  else:
    tname = f['subtag']
  
  # If this category is filtered out, skip to next record
  if arg_category is not None:
    if tval != arg_category:
      continue
  
  # If we are remapping, filter out if not remapped
  if arg_remap:
    if 'preferred-value' not in f:
      continue
  
  # If uvar flag is on, filter out if there are prefixes
  if arg_uvar:
    if 'prefix' in f:
      continue
  
  # Print out this record
  if arg_remap:
    if tval == 'extlang':
      print('extlang', tname, 'remap at line', r[0])
    else:
      print(tname, '->', f['preferred-value'], 'at line', r[0])
  else:
    print(tname, 'at line', r[0])
