#
# iso2.py
# =======
#
# Python-3 module for loading and parsing the ISO-639-2 data file.
#
# A current copy of the data file is available at the ISO-639-2
# registrar:
#
#   https://www.loc.gov/standards/iso639-2/
#
# IMPORTANT:  Use the UTF-8 version of the data file.
#
# To use this module, import iso2 and then call iso2.parse() with the
# path to the data file.  If this is successful, the result will be
# placed in the iso2.rec variable.  The iso2.code variable will then
# also hold a mapping of all language codes to their records.
#
# The private use range record is skipped.  This is the range qaa-qtz
# which is "Reserved for local use"
#

#
# Exceptions
# ----------
#
# Each exception overloads the __str__ operator so that it can be
# printed as a user-friendly error message.  The error message includes
# line number information if relevant.  It has punctuation at the end,
# but it does NOT have a line break at the end.
#
# All exceptions defined by this module are subclasses of ISO2Error.
#

class ISO2Error(Exception):
  def __str__(self):
    return 'Unknown ISO-639-2 parsing error!'

class BadCode(ISO2Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-2 data line ' + str(self.m_line) + ': ' + \
        'Invalid language code!'
    else:
      return 'Invalid language code!'

class BadDataFile(ISO2Error):
  def __str__(self):
    return 'ISO-639-2 data file must be the UTF-8 version!'

class BadRecord(ISO2Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-2 data line ' + str(self.m_line) + ': ' + \
        'Invalid record syntax!'
    else:
      return 'Invalid record syntax!'

class DoubleCodeError(ISO2Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-2 data line ' + str(self.m_line) + ': ' + \
        'Record has doubled code!'
    else:
      return 'Record has doubled code!'

class FieldMissingError(ISO2Error):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'ISO-639-2 data line ' + str(self.m_line) + ': ' + \
        'Record missing required field!'
    else:
      return 'Record missing required field!'

class LogicError(ISO2Error):
  def __str__(self):
    return 'Internal logic error within ISO-639-2 module!'

class NoDataFileError(ISO2Error):
  def __init__(self, fpath=None):
    self.m_fpath = fpath
  def __str__(self):
    if self.m_fpath is not None:
      return 'Can\'t find ISO-639-2 data file ' + self.m_fpath
    else:
      return 'Can\'t find ISO-639-2 data file!'

class RedefineError(ISO2Error):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'ISO-639-2 record at line ' + str(self.m_line) + ': ' + \
        'Language code ' + self.m_tname + ' is already defined!'
    
    elif self.m_line is not None:
      return 'ISO-639-2 record at line ' + str(self.m_line) + ': ' + \
        'Language code is already defined!'
      
    else:
      return 'Language code is already defined!'

#
# Module-level variables
# ----------------------
#

# The module-level variable that stores the result of parsing the data
# file, or None if the file hasn't been parsed yet.
#
# Use the parse() function to set this variable.  Once it is set
# successfully, it will be a list of zero or more records, stored in the
# order they appear in the data file.
#
# Each record is a tuple with two elements.  The first element is an
# integer that stores the line number of the first line of the record in
# the data file.  The second element is a dictionary that maps field
# names to field values.
#
# The official data file does not have any header line identifying the
# name of the columns.  The following field names are defined by this
# module for sake of identification:
#
#   biblio3 - the three-letter bibliographic language code
#   term3   - the three-letter terminologic language code
#   code2   - the two-letter language code
#   en      - the English name of the language record
#   fr      - the French name of the language record
#
# The term3 and code2 fields are optional and are not present in all
# records.  All other fields are required and present in all records.
#
rec = None

# The module-level variable that stores the index of language codes to
# parsed records, or None if the file hasn't been parsed yet.
#
# Use the parse() function to set this variable.  Once it is set
# successfully, it will be a dictionary with string keys and values that
# are the same tuple objects used in the rec module-level variable.
#
# Multiple keys may map to the same tuple object.
#
code = None

#
# Local functions
# ---------------
#

# Verify that a given string is a two-letter code with both letters
# being lowercase ASCII letters.
#
# Parameters:
#
#   cd : string | mixed - the value to check
#
# Return:
#
#   True if valid two-letter code, False otherwise
#
def check_code_2(cd):
  if not isinstance(cd, str):
    return False
  if len(cd) != 2:
    return False
  for c in cd:
    if (ord(c) < ord('a')) or (ord(c) > ord('z')):
      return False
  return True

# Verify that a given string is a three-letter code with all letters
# being lowercase ASCII letters.
#
# Parameters:
#
#   cd : string | mixed - the value to check
#
# Return:
#
#   True if valid three-letter code, False otherwise
#
def check_code_3(cd):
  if not isinstance(cd, str):
    return False
  if len(cd) != 3:
    return False
  for c in cd:
    if (ord(c) < ord('a')) or (ord(c) > ord('z')):
      return False
  return True

# Check whether the given language code is one of the private-use
# language codes.
#
# Parameters:
#
#   cd : string | mixed - the value to check
#
# Return:
#
#   True if a private-use code, False otherwise
#
def is_private(cd):
  
  # If parameter isn't string, it isn't a private-use code
  if not isinstance(cd, str):
    return False
  
  # If code isn't exactly three characters, it isn't private-use
  if len(cd) != 3:
    return False
  
  # Language code matching is case-insensitive, so make the given
  # language code lowercase
  cd = cd.lower()
  
  # If first letter of language code isn't q, then it isn't private-use
  if cd[0] != 'q':
    return False
  
  # In order to be private use, second character must be in range a-t
  # and third character must be in range a-z
  if (ord(cd[1]) >= ord('a')) and (ord(cd[1]) <= ord('t')) and \
      (ord(cd[2]) >= ord('a')) and (ord(cd[2]) <= ord('z')):
    return True
  else:
    return False

# Given a string holding the first line of text in a file, strip a
# leading UTF-8 Byte Order Mark (BOM) if present.
#
# Only use this function on the very first line of the file, as that is
# the only place a BOM may be present.
#
# The return value is the string as-is if there is no BOM.
#
# Parameters:
#
#   line : string - the first line to process
#
# Return:
#
#   the first line, with the BOM stripped out if present
#
def strip_bom(line):
  if not isinstance(line, str):
    raise LogicError()
  if len(line) < 1:
    return line
  if ord(line[0]) == 0xfeff:
    if len(line) > 1:
      return line[1:]
    else:
      return ''
  else:
    return line

#
# Public functions
# ----------------
#

# Parse the given ISO-639-2 data file and store the parsed result in the
# module-level rec and code variables.
#
# See the module documentation and the documentation of the rec variable
# for further information.
#
# If the rec value is already set, this function call will be ignored.
#
# If the function fails, the rec and code values will be set to None.
#
# Parameters:
#
#   fpath : string - the path to the data file
#
def parse(fpath):

  global rec, code

  # Ignore call if rec already set
  if rec is not None:
    return

  # Check parameter
  if not isinstance(fpath, str):
    rec = None
    code = None
    raise LogicError()

  # Clear the records variable to an empty list and set the code
  # dictionary to an empty dictionary
  rec = []
  code = dict()

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  try:
    with open(fpath, mode='rt',
              encoding='utf-8', errors='strict') as fin:
  
      # We have the input file open -- read line by line
      line_num = 0  # Current line number
      for line in fin:
        
        # Update line count
        line_num = line_num + 1
        
        # If this is the first line, remove UTF-8 Byte Order Mark (BOM)
        # if present
        if line_num <= 1:
          line = strip_bom(line)
        
        # Trim leading and trailing whitespace and linebreaks
        line = line.strip(' \t\n')
        
        # Filter out blank lines that are empty or contain only spaces,
        # tabs, and line breaks
        if len(line) < 1:
          continue
        
        # We have a content line, so parse into fields using the
        # vertical bar as separator
        fv = line.split('|')
        
        # Each record should have exactly five fields
        if len(fv) != 5:
          raise BadRecord(line_num)
        
        # Trim each field of leading and trailing whitespace
        for i in range(0, len(fv)):
          fv[i] = fv[i].strip(' \t')
        
        # Make sure the required fields are not empty
        if (len(fv[0]) < 1) or \
            (len(fv[3]) < 1) or \
            (len(fv[4]) < 1):
          raise FieldMissingError(line_num)
        
        # Create a new record and assign the required fields
        r = dict()
        r['biblio3'] = fv[0]
        r['en'] = fv[3]
        r['fr'] = fv[4]
        
        # Assign the optional fields only if not empty
        if len(fv[1]) > 0:
          r['term3'] = fv[1]
        if len(fv[2]) > 0:
          r['code2'] = fv[2]
        
        # If this is the reserved range, skip this record
        if r['biblio3'] == 'qaa-qtz':
          continue
        
        # Check the language code formats
        if not check_code_3(r['biblio3']):
          raise BadCode(line_num)
        if 'term3' in r:
          if not check_code_3(r['term3']):
            raise BadCode(line_num)
        if 'code2' in r:
          if not check_code_2(r['code2']):
            raise BadCode(line_num)
        
        # Make sure that if term3 is given, it isn't equal to biblio3
        if 'term3' in r:
          if r['biblio3'] == r['term3']:
            raise DoubleCodeError(line_num)
        
        # Make sure that none of the language codes are in the index yet
        # and that they aren't in reserved private range
        if r['biblio3'] in code:
          raise RedefineError(line_num, r['biblio3'])
        if is_private(r['biblio3']):
          raise RedefineError(line_num, r['biblio3'])
        if 'term3' in r:
          if r['term3'] in code:
            raise RedefineError(line_num, r['term3'])
          if is_private(r['term3']):
            raise RedefineError(line_num, r['term3'])
        if 'code2' in r:
          if r['code2'] in code:
            raise RedefineError(line_num, r['code2'])
  
        # Define the tuple pair of the line number and the record
        pr = (line_num, r)
        
        # Add the tuple to the parsed variables
        rec.append(pr)
        code[r['biblio3']] = pr
        if 'term3' in r:
          code[r['term3']] = pr
        if 'code2' in r:
          code[r['code2']] = pr
  
  except FileNotFoundError:
    rec = None
    code = None
    raise NoDataFileError(fpath)
  
  except ValueError:
    rec = None
    code = None
    raise BadDataFile()
    
  except ISO2Error as se:
    rec = None
    code = None
    raise se
  
  except Exception as exc:
    rec = None
    code = None
    raise ISO2Error() from exc
