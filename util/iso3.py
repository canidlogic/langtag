#
# iso3.py
# =======
#
# Python-3 module for loading and parsing the ISO-639-3 data files.
#
# A current copy of the data files is available at the ISO-639-3
# registrar:
#
#   https://iso639-3.sil.org/
#
# IMPORTANT:  Use the UTF-8 version of the data files.
#
# Four separate data files are needed:
#
#   (1) Code set table [the main table]
#   (2) Language names index
#   (3) Macrolanguage mappings
#   (4) Deprecated/retired code element mappings
#
# NOTE: the official deprecated/retired code table has some erroneous
# records in it.  The fix_retire() function is used to correct these
# records within this source file.  See that function for further
# information.
#
# The names of the tables used in this source file are:
#
#   (1) code
#   (2) name
#   (3) macro
#   (4) retire
#
# Documentation of the format of these tables is available at:
#
#   https://iso639-3.sil.org/code_tables/download_tables
#
# To use this module, import iso3 and then call iso3.parse() with the
# paths to the data files.  If this is successful, the result will be
# placed in the appropriate module variables -- see the module-level
# variables section for further information.
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
# All exceptions defined by this module are subclasses of ISO3Error.
#

# Utility function that forms the error message prefix for all the
# exceptions defined in this class.
#
# All parameters are optional and may be left at None.  The prefix
# always includes the text "ISO-639-3 data table" and the prefix always
# ends in a colon and a space.
#
# If invalid parameters are given, they are replaced by None.
#
# Parameters:
#
#   df : str | None - if provided, the specific data table that the
#   error originates in, which must be one of the four table names
#   defined at the top of this source file
#
#   line : int | None - if provided, the line number within the data
#   file that is relevant to the error
#
#   val : str | None - if provided, the specific value that caused an
#   error
#
# Return:
#
#   a string containing the proper exception message prefix
#
def ex_msg_prefix(df=None, line=None, val=None):
  # Check and fix parameters
  if isinstance(df, str):
    if (df != 'code') and (df != 'name') and \
        (df != 'macro') and (df != 'retire'):
      df = None
  else:
    df = None
  
  if isinstance(line, int):
    if (line < 1):
      line = None
  else:
    line = None
  
  if not isinstance(val, str):
    val = None
  
  # Begin the prefix with the table ID (if known), else a generic
  # message
  pfx = None
  if df is not None:
    pfx = 'ISO-639-3 ' + df + ' table'
  else:
    pfx = 'ISO-639-3 data table'
  
  # If line number given, add information
  if line is not None:
    pfx = pfx + ' line ' + str(line)
  
  # If value given, escape " in value as ""
  if val is not None:
    val = val.replace('"', '""')
  
  # If value given, add information
  if val is not None:
    pfx = pfx + ' value "' + val + '"'
  
  # Add the final colon and space
  pfx = pfx + ': '
  
  # Return prefix
  return pfx

class ISO3Error(Exception):
  def __str__(self):
    return ex_msg_prefix() + 'Unknown parsing error!'

class BadCode(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'Invalid language code!'

class BadDataFile(ISO3Error):
  def __init__(self, df=None):
    self.m_df = df
  def __str__(self):
    return ex_msg_prefix(self.m_df) + \
      'Data file must be the UTF-8 version!'

class BadFieldValue(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'Data field has invalid value!'

class BadForeignKey(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'Foreign key check failed!'

class BadHeader(ISO3Error):
  def __init__(self, df=None):
    self.m_df = df
  def __str__(self):
    return ex_msg_prefix(self.m_df) + \
      'Data file has invalid header line!'

class BadMappingContext(ISO3Error):
  def __init__(self, df=None, line=None):
    self.m_df = df
    self.m_line = line
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line) + \
      'Remapping field can\'t be used with this kind of record!'

class FieldMissingError(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'Record missing required field!'

class InconsistentSpecialError(ISO3Error):
  def __init__(self, df=None, line=None):
    self.m_df = df
    self.m_line = line
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line) + \
      'Special records must have special contexts and types!'

class ISOMissingError(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'ISO 639-2 terminology code missing when biblio code present!'

class ISOSyncError(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'ISO 639-2 terminology code doesn\'t match ISO-639-3 code!'

class LogicError(ISO3Error):
  def __str__(self):
    return ex_msg_prefix() + \
      'Internal logic error within module!'

class MissingNameError(ISO3Error):
  def __init__(self, df=None, val=None):
    self.m_df = df
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, None, self.m_val) + \
      'Language code in main table is missing a name record!'

class NoDataFileError(ISO3Error):
  def __init__(self, df=None):
    self.m_df = df
  def __str__(self):
    return ex_msg_prefix(self.m_df) + \
      'Can\'t find data file!'

class RedefineError(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'Language code is already defined!'

class SelfMappingError(ISO3Error):
  def __init__(self, df=None, line=None):
    self.m_df = df
    self.m_line = line
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line) + \
      'Retirement record can\'t remap language code to itself!'

class UnretiredError(ISO3Error):
  def __init__(self, df=None, line=None, val=None):
    self.m_df = df
    self.m_line = line
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_df, self.m_line, self.m_val) + \
      'Retired language code is also in main code table!'

#
# Module-level variables
# ----------------------
#
# The module-level variables storing parsed result all have the same
# kind of format.
#
# First, there is a rec_ variable for each table.  Second, there is a
# code_ variable for each table.  Each of these variables has one of the
# four table names defined at the top of this source file suffixed to it
# to identify which table it is for.
#
# The rec_ variables are lists of records.  The code_ variables are
# dictionaries that map language code strings to records within the
# table.  Multiple language codes may map to the same record in the code
# table.  In the macro table, the language code maps to the unique
# language entry.  The macrolanguage codes are *not* included in the
# index for the macro table -- only the individual language codes are.
# For the retire table each language code maps to a unique record.
#
# The name table index is different because a single language code can
# have multiple names.  Therefore the values in code_name are lists of
# records rather than individual records as in the other tables.
# 
# The values of these module-level variables are set to None initially.
# Use the parse() function to parse all the data files and set these
# variables.
#
# For each of the four tables, the documentation below in this section
# gives the official column names that are used in the data files, the
# field names that these map to in the parsed records below, and whether
# the field is required or optional.  If optional, then when not present
# the field will be absent from the record dictionary.
#

# The code table mapping of official columns to field names:
#
#   Official name | Dictionary field name | Required
#   --------------|-----------------------|----------
#   Id            | code3                 |    Y
#   Part2B        | biblio3               |    N
#   Part2T        | term3                 |    N
#   Part1         | code2                 |    N
#   Scope         | scope                 |    Y
#   Language_Type | ltype                 |    Y
#   Ref_Name      | name                  |    Y
#   Comment       | comment               |    N
#
# code3, biblio3, term3 if present are strings of exactly three
# lowercase ASCII letters.
#
# code2 if present is string of exactly two lowercase ASCII letters.
#
# scope is one of the following values:
#
#   Scope code | Description
#   -----------|--------------
#        I     | Individual
#        M     | Macrolanguage
#        S     | Special
#
# ltype is one of the following values:
#
#   ltype code | Description
#   -----------|-------------
#        A     | Ancient
#        C     | Constructed
#        E     | Extinct
#        H     | Historical
#        L     | Living
#        S     | Special
#
# Note that although a reference name is given in this table, the more
# normative table to use is the name table for language names.
#
rec_code = None
code_code = None

# The name table mapping of official columns to field names:
#
#   Official name | Dictionary field name | Required
#   --------------|-----------------------|----------
#   Id            | code3                 |    Y
#   Print_Name    | name                  |    Y
#   Inverted_Name | iname                 |    Y
#
# The code3 field is a foreign key that references a record in the main
# code table.  There may be more than one name mapped to a single code3
# value.
#
# The name and iname fields are both always present.  The iname field
# tries to re-order the name elements so that the most general language
# label is first.  iname is sometimes equal to name.
#
# Note that the values in code_name are lists of records rather than
# just a record object.  This is because a single language code can have
# multiple names mapped to it.
#
rec_name = None
code_name = None

# The macro table mapping of official columns to field names:
#
#   Official name | Dictionary field name | Required
#   --------------|-----------------------|----------
#   M_Id          | macro3                |    Y
#   I_Id          | code3                 |    Y
#   I_Status      | active                |    Y
#
# The macro3 field is a foreign key that references a record in the main
# code table.  This referenced record must be for a macrolanguage.
#
# The code3 field is a foreign key that references a record either in
# the main code table or in the retire table.  If a record is referenced
# in the main code table, it must be for an individual language.
#
# The active field is True if code3 is in the main code table or False
# if code3 is in the retire table.  These are translations of the 'A'
# field value for Active and the 'R' field value for Retired.
#
rec_macro = None
code_macro = None

# The retire table mapping of official columns to field names:
#
#   Official name | Dictionary field name | Required
#   --------------|-----------------------|----------
#   Id            | code3                 |    Y
#   Ref_Name      | name                  |    Y
#   Ret_Reason    | reason                |    Y
#   Change_To     | mapping               |   (*)
#   Ret_Remedy    | comment               |    N
#   Effective     | date                  |    Y
#
# The code3 field must be a string of exactly three lowercase digits.
# It must NOT appear in the code table.
#
# The name field is the name of the retired language entry.
#
# The reason field must be one of the following values:
#
#   Reason code | Description
#   ------------|-------------
#        C      | Change
#        D      | Duplicate
#        N      | Non-existent
#        S      | Split
#        M      | Merge
#
# The mapping field MUST be present if the reason is C, D, or M.  The
# mapping field MUST NOT be present for the other reasons.  If present,
# it must be a foreign key that selects a record in the code table that
# this old language tag should be mapped to.
#
# The comment field is optional, and is used for the S reason to
# describe the different modern choices for the language key.
#
rec_retire = None
code_retire = None

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

# Given a parsed record from the retire table that hasn't been checked
# yet, perform corrections on the record.
#
# This function is necessary because some of the records in the official
# table have errors in them.  This function will fix these erroneous
# records.
#
# If the function returns False, then the record is a complete error and
# it should be skipped and not added to the parsed results.  If the
# function returns True then record verification and processing can
# proceed; if there was an error in the record, this function will make
# the necessary changes to the record values.
#
# Parameters:
#
#   r : dict - the parsed record mapping of field names to field values
#
# Return:
#
#   True if processing can continue with the (possibly modified) record,
#   False if the record should be skipped entirely
#
def fix_retire(r):
  
  # Check parameter
  if not isinstance(r, dict):
    raise LogicError()
  
  # Only process if there is a code3 field; else just return True
  # because we can't look up any fixes
  if 'code3' not in r:
    return True
  
  # Use the code3 field to look up any corrections, else return True if
  # we don't have any corrections
  c = r['code3']
  if (c == 'chs'):
    # The chs "Chumash" record is incomplete in the official data file,
    # lacking a reason code -- only proceed with correction if this is
    # still the case, otherwise the data has been updated so do not
    # correct
    if 'reason' not in r:
      # Record is still missing a reason code and is thus erroneous;
      # this "Chumash" is a language family rather than a language, and
      # the codes for the individual languages are found in the main
      # table, so it should be safe to drop the record entirely
      return False
    
  elif (c == 'lcq'):
    # There is an erroneous record mapping lcq to ppr, when the proper
    # mapping of ppr to lcq is already in the retirement table; check
    # that this erroneous record hasn't been updated by making sure
    # there is a mapping to 'ppr'
    if 'mapping' in r:
      if r['mapping'] == 'ppr':
        # Drop this erroneous mapping
        return False
    
  elif (c == 'ymt'):
    # There is an erroneous mapping of ymt to itself; if this is still
    # the case, fix it to map to mtm instead, which is the correct value
    # determined from the IANA subtag registry
    if 'mapping' in r:
      if r['mapping'] == 'ymt':
        r['mapping'] = 'mtm'
        return True
    
  elif (c == 'guv'):
    # There is an erroneous mapping of guv to itself; if this is still
    # the case, fix it to map to duz instead, which is the correct value
    # determined from the IANA subtag registry
    if 'mapping' in r:
      if r['mapping'] == 'guv':
        r['mapping'] = 'duz'
        return True
    
  # If we got here, no known corrections needed
  return True

# Parse the code table from the given ISO-639-3 data file that stores
# the main code table and store the parsed result in the module-level
# rec_code and code_code variables.
#
# See the module documentation and the documentation of the module-level
# variables for further information.
#
# If the function fails, the module-level variables are in an undefined
# state.
#
# Parameters:
#
#   fpath : string - the path to the data file
#
def parse_code(fpath):

  global rec_code, code_code
  
  # Check parameter
  if not isinstance(fpath, str):
    raise LogicError()

  # Clear the records variable to an empty list and set the code
  # dictionary to an empty dictionary
  rec_code = []
  code_code = dict()

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  with open(fpath, mode='rt',
            encoding='utf-8', errors='strict') as fin:

    # We have the input file open -- read line by line
    line_num = 0  # Current line number
    fmap = None   # Mapping of fields to column indices
    for line in fin:
      
      # Update line count
      line_num = line_num + 1
      
      # If this is the first line, remove UTF-8 Byte Order Mark (BOM)
      # if present
      if line_num <= 1:
        line = strip_bom(line)
      
      # Trim trailing whitespace and linebreaks
      line = line.rstrip(' \t\n')
      
      # If this is the first line, set up fmap and skip rest of
      # processing
      if line_num <= 1:
        
        # Parse into columns
        cn = line.split('\t')
        
        # Should be at least eight columns
        if len(cn) < 8:
          raise BadHeader('code')
          
        # Trim all column names and make them lowercase
        for x in range(0, len(cn)):
          cn[x] = cn[x].strip(' \t').lower()
        
        # Set fmap variable
        fmap = dict()
        for i in range(0, len(cn)):
          # Get current column name
          n = cn[i]
          
          # Only process this column if one of the recognized column
          # names (in lowercase)
          if (n == 'id') or (n == 'part2b') or (n == 'part2t') or \
              (n == 'part1') or (n == 'scope') or \
              (n == 'language_type') or (n == 'ref_name') or \
              (n == 'comment'):
            
            # Map name to standard dictionary name
            if (n == 'id'):
              n = 'code3'
            elif (n == 'part2b'):
              n = 'biblio3'
            elif (n == 'part2t'):
              n = 'term3'
            elif (n == 'part1'):
              n = 'code2'
            elif (n == 'scope'):
              n = 'scope'
            elif (n == 'language_type'):
              n = 'ltype'
            elif (n == 'ref_name'):
              n = 'name'
            elif (n == 'comment'):
              n = 'comment'
            else:
              raise LogicError()
            
            # Make sure name not already mapped
            if n in fmap:
              raise BadHeader('code')
            
            # Store name to column index mapping
            fmap[n] = i
        
        # Make sure we found all the required columns
        if ('code3' not in fmap) or ('biblio3' not in fmap) or \
            ('term3' not in fmap) or ('code2' not in fmap) or \
            ('scope' not in fmap) or ('ltype' not in fmap) or \
            ('name' not in fmap) or ('comment' not in fmap):
          raise BadHeader('code')
        
        # Skip rest of processing
        continue
      
      # Filter out blank lines that are empty or contain only spaces,
      # tabs, and line breaks
      if len(line) < 1:
        continue
      
      # We have a content line, so parse into fields using the
      # horizontal tab as separator
      fv = line.split('\t')
      
      # Trim each field of leading and trailing whitespace
      for i in range(0, len(fv)):
        fv[i] = fv[i].strip(' \t')
      
      # Create a new record and assign all the fields that are present
      r = dict()
      for fnm in fmap:
        if len(fv) > fmap[fnm]:
          if len(fv[fmap[fnm]]) > 0:
            r[fnm] = fv[fmap[fnm]]
      
      # Make sure the required fields are present
      if 'code3' not in r:
        raise FieldMissingError('code', line_num, 'code3')
      if 'scope' not in r:
        raise FieldMissingError('code', line_num, 'scope')
      if 'ltype' not in r:
        raise FieldMissingError('code', line_num, 'ltype')
      if 'name' not in r:
        raise FieldMissingError('code', line_num, 'name')
      
      # Check the raw format of the language codes
      if not check_code_3(r['code3']):
        raise BadCode('code', line_num, r['code3'])
      
      if 'biblio3' in r:
        if not check_code_3(r['biblio3']):
          raise BadCode('code', line_num, r['biblio3'])
      
      if 'term3' in r:
        if not check_code_3(r['term3']):
          raise BadCode('code', line_num, r['term3'])
      
      if 'code2' in r:
        if not check_code_2(r['code2']):
          raise BadCode('code', line_num, r['code2'])
      
      # If the term3 code is present, it must be equal to the main code
      if 'term3' in r:
        if r['term3'] != r['code3']:
          raise ISOSyncError('code', line_num, r['term3'])
      
      # For better consistency with ISO-639-2, remove the biblio3 code
      # if it is the same as the term3 code
      if ('biblio3' in r) and ('term3' in r):
        if r['biblio3'] == r['term3']:
          del r['biblio3']
      
      # If biblio3 is still present, term3 must also be present
      if 'biblio3' in r:
        if 'term3' not in r:
          raise ISOMissingError('code', line_num, r['biblio3'])
      
      # Check the scope field
      s = r['scope']
      if (s != 'I') and (s != 'M') and (s != 'S'):
        raise BadFieldValue('code', line_num, s)
      
      # Check the language type field
      s = r['ltype']
      if (s != 'A') and (s != 'C') and (s != 'E') and \
          (s != 'H') and (s != 'L') and (s != 'S'):
        raise BadFieldValue('code', line_num, s)
      
      # If scope or language is special, both must be special
      if (r['scope'] == 'S') or (r['ltype'] == 'S'):
        if (r['scope'] != 'S') or (r['ltype'] != 'S'):
          raise InconsistentSpecialError('code', line_num)
      
      # Make sure that none of the language codes are private or already
      # in the index
      if (r['code3'] in code_code) or is_private(r['code3']):
        raise RedefineError('code', line_num, r['code3'])
      
      if 'biblio3' in r:
        if (r['biblio3'] in code_code) or is_private(r['biblio3']):
          raise RedefineError('code', line_num, r['biblio3'])
      
      if 'term3' in r:
        if (r['term3'] in code_code) or is_private(r['term3']):
          raise RedefineError('code', line_num, r['term3'])
      
      if 'code2' in r:
        if r['code2'] in code_code:
          raise RedefineError('code', line_num, r['code2'])
      
      # Define the tuple pair of the line number and the record
      pr = (line_num, r)
      
      # Add the tuple to the parsed variables
      rec_code.append(pr)
      code_code[r['code3']] = pr
      if 'biblio3' in r:
        code_code[r['biblio3']] = pr
      if 'term3' in r:
        code_code[r['term3']] = pr
      if 'code2' in r:
        code_code[r['code2']] = pr

# Parse the retire table from the given ISO-639-3 data file that stores
# the retired code table and store the parsed result in the module-level
# rec_retire and code_retire variables.
#
# You must use parse_code() before this function because this function
# requires the main code table to already be parsed so that its records
# can be cross-checked.
#
# See the module documentation and the documentation of the module-level
# variables for further information.
#
# If the function fails, the module-level variables are in an undefined
# state.
#
# Parameters:
#
#   fpath : string - the path to the data file
#
def parse_retire(fpath):

  global rec_retire, code_retire
  global rec_code, code_code
  
  # Check state
  if (rec_code is None) or (code_code is None):
    raise LogicError()
  
  # Check parameter
  if not isinstance(fpath, str):
    raise LogicError()

  # Clear the records variable to an empty list and set the code
  # dictionary to an empty dictionary
  rec_retire = []
  code_retire = dict()

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  with open(fpath, mode='rt',
            encoding='utf-8', errors='strict') as fin:

    # We have the input file open -- read line by line
    line_num = 0  # Current line number
    fmap = None   # Mapping of fields to column indices
    for line in fin:
      
      # Update line count
      line_num = line_num + 1
      
      # If this is the first line, remove UTF-8 Byte Order Mark (BOM)
      # if present
      if line_num <= 1:
        line = strip_bom(line)
      
      # Trim trailing whitespace and linebreaks
      line = line.rstrip(' \t\n')
      
      # If this is the first line, set up fmap and skip rest of
      # processing
      if line_num <= 1:
        
        # Parse into columns
        cn = line.split('\t')
        
        # Should be at least six columns
        if len(cn) < 6:
          raise BadHeader('retire')
          
        # Trim all column names and make them lowercase
        for x in range(0, len(cn)):
          cn[x] = cn[x].strip(' \t').lower()
        
        # Set fmap variable
        fmap = dict()
        for i in range(0, len(cn)):
          # Get current column name
          n = cn[i]
          
          # Only process this column if one of the recognized column
          # names (in lowercase)
          if (n == 'id') or (n == 'ref_name') or \
              (n == 'ret_reason') or (n == 'change_to') or \
              (n == 'ret_remedy') or (n == 'effective'):
            
            # Map name to standard dictionary name
            if (n == 'id'):
              n = 'code3'
            elif (n == 'ref_name'):
              n = 'name'
            elif (n == 'ret_reason'):
              n = 'reason'
            elif (n == 'change_to'):
              n = 'mapping'
            elif (n == 'ret_remedy'):
              n = 'comment'
            elif (n == 'effective'):
              n = 'date'
            else:
              raise LogicError()
            
            # Make sure name not already mapped
            if n in fmap:
              raise BadHeader('retire')
            
            # Store name to column index mapping
            fmap[n] = i
        
        # Make sure we found all the required columns
        if ('code3' not in fmap) or ('name' not in fmap) or \
            ('reason' not in fmap) or ('mapping' not in fmap) or \
            ('comment' not in fmap) or ('date' not in fmap):
          raise BadHeader('retire')
        
        # Skip rest of processing
        continue
      
      # Filter out blank lines that are empty or contain only spaces,
      # tabs, and line breaks
      if len(line) < 1:
        continue
      
      # We have a content line, so parse into fields using the
      # horizontal tab as separator
      fv = line.split('\t')
      
      # Trim each field of leading and trailing whitespace
      for i in range(0, len(fv)):
        fv[i] = fv[i].strip(' \t')
      
      # Create a new record and assign all the fields that are present
      r = dict()
      for fnm in fmap:
        if len(fv) > fmap[fnm]:
          if len(fv[fmap[fnm]]) > 0:
            r[fnm] = fv[fmap[fnm]]
      
      # Perform any corrections to the records and skip record entirely
      # if it should be dropped
      if not fix_retire(r):
        continue
      
      # Make sure the required fields are present
      if 'code3' not in r:
        raise FieldMissingError('retire', line_num, 'code3')
      if 'name' not in r:
        raise FieldMissingError('retire', line_num, 'name')
      if 'reason' not in r:
        raise FieldMissingError('retire', line_num, 'reason')
      if 'date' not in r:
        raise FieldMissingError('retire', line_num, 'date')
      
      # Check the reason code
      s = r['reason']
      if (s != 'C') and (s != 'D') and (s != 'N') and \
          (s != 'S') and (s != 'M'):
        raise BadFieldValue('retire', line_num, s)
      
      # If reason is C D or M then mapping field MUST be present;
      # otherwise, it MUST NOT be present
      s = r['reason']
      if (s == 'C') or (s == 'D') or (s == 'M'):
        if 'mapping' not in r:
          raise FieldMissingError('retire', line_num, 'mapping')
      else:
        if 'mapping' in r:
          raise BadMappingContext('retire', line_num)
      
      # Check the raw format of the language codes
      if not check_code_3(r['code3']):
        raise BadCode('retire', line_num, r['code3'])
      
      if 'mapping' in r:
        if not check_code_3(r['mapping']):
          raise BadCode('retire', line_num, r['mapping'])
      
      # The retired code must not be in the main table unless it is a
      # duplicate, in which case it must just not equal the mapping
      if r['reason'] != 'D':
        if r['code3'] in code_code:
          raise UnretiredError('retire', line_num, r['code3'])
      else:
        if r['code3'] == r['mapping']:
          raise SelfMappingError('retire', line_num)
      
      # If mapping is present, it must be in the main table AND it must
      # map to a code3 column value
      if 'mapping' in r:
        if r['mapping'] not in code_code:
          raise BadForeignKey('retire', line_num, r['mapping'])
        if code_code[r['mapping']][1]['code3'] != r['mapping']:
          raise BadForeignKey('retire', line_num, r['mapping'])
      
      # Make sure that the retired language code is not private and not
      # already in the index
      if (r['code3'] in code_retire) or is_private(r['code3']):
        raise RedefineError('retire', line_num, r['code3'])
      
      # Define the tuple pair of the line number and the record
      pr = (line_num, r)
      
      # Add the tuple to the parsed variables
      rec_retire.append(pr)
      code_retire[r['code3']] = pr

# Parse the name table from the given ISO-639-3 data file that stores
# the name table and store the parsed result in the module-level 
# rec_name and code_name variables.
#
# You must use parse_code() before this function because this function
# requires the main code table to already be parsed so that its records
# can be cross-checked.
#
# See the module documentation and the documentation of the module-level
# variables for further information.
#
# If the function fails, the module-level variables are in an undefined
# state.
#
# Parameters:
#
#   fpath : string - the path to the data file
#
def parse_name(fpath):

  global rec_name, code_name
  global rec_code, code_code
  
  # Check state
  if (rec_code is None) or (code_code is None):
    raise LogicError()
  
  # Check parameter
  if not isinstance(fpath, str):
    raise LogicError()

  # Clear the records variable to an empty list and set the code
  # dictionary to an empty dictionary
  rec_name = []
  code_name = dict()

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  with open(fpath, mode='rt',
            encoding='utf-8', errors='strict') as fin:

    # We have the input file open -- read line by line
    line_num = 0  # Current line number
    fmap = None   # Mapping of fields to column indices
    for line in fin:
      
      # Update line count
      line_num = line_num + 1
      
      # If this is the first line, remove UTF-8 Byte Order Mark (BOM)
      # if present
      if line_num <= 1:
        line = strip_bom(line)
      
      # Trim trailing whitespace and linebreaks
      line = line.rstrip(' \t\n')
      
      # If this is the first line, set up fmap and skip rest of
      # processing
      if line_num <= 1:
        
        # Parse into columns
        cn = line.split('\t')
        
        # Should be at least three columns
        if len(cn) < 3:
          raise BadHeader('name')
          
        # Trim all column names and make them lowercase
        for x in range(0, len(cn)):
          cn[x] = cn[x].strip(' \t').lower()
        
        # Set fmap variable
        fmap = dict()
        for i in range(0, len(cn)):
          # Get current column name
          n = cn[i]
          
          # Only process this column if one of the recognized column
          # names (in lowercase)
          if (n == 'id') or (n == 'print_name') or \
              (n == 'inverted_name'):
            
            # Map name to standard dictionary name
            if (n == 'id'):
              n = 'code3'
            elif (n == 'print_name'):
              n = 'name'
            elif (n == 'inverted_name'):
              n = 'iname'
            else:
              raise LogicError()
            
            # Make sure name not already mapped
            if n in fmap:
              raise BadHeader('name')
            
            # Store name to column index mapping
            fmap[n] = i
        
        # Make sure we found all the required columns
        if ('code3' not in fmap) or ('name' not in fmap) or \
            ('iname' not in fmap):
          raise BadHeader('name')
        
        # Skip rest of processing
        continue
      
      # Filter out blank lines that are empty or contain only spaces,
      # tabs, and line breaks
      if len(line) < 1:
        continue
      
      # We have a content line, so parse into fields using the
      # horizontal tab as separator
      fv = line.split('\t')
      
      # Trim each field of leading and trailing whitespace
      for i in range(0, len(fv)):
        fv[i] = fv[i].strip(' \t')
      
      # Create a new record and assign all the fields that are present
      r = dict()
      for fnm in fmap:
        if len(fv) > fmap[fnm]:
          if len(fv[fmap[fnm]]) > 0:
            r[fnm] = fv[fmap[fnm]]
      
      # Make sure the required fields are present
      if 'code3' not in r:
        raise FieldMissingError('name', line_num, 'code3')
      if 'name' not in r:
        raise FieldMissingError('name', line_num, 'name')
      if 'iname' not in r:
        raise FieldMissingError('name', line_num, 'iname')
      
      # Check the raw format of the language code
      if not check_code_3(r['code3']):
        raise BadCode('name', line_num, r['code3'])
      
      # The language code must be in the main table AND it must map to
      # a code3 language code
      if r['code3'] not in code_code:
        raise BadForeignKey('name', line_num, r['code3'])
      if code_code[r['code3']][1]['code3'] != r['code3']:
        raise BadForeignKey('name', line_num, r['code3'])
      
      # Make sure that the language code is not private
      if is_private(r['code3']):
        raise RedefineError('name', line_num, r['code3'])
      
      # Define the tuple pair of the line number and the record
      pr = (line_num, r)
      
      # Add the tuple to the parsed variables -- for the name index,
      # however, remember that it has to be a list of records rather
      # than just a record since multiple names can map to the same
      # language code
      rec_name.append(pr)
      if r['code3'] in code_name:
        code_name[r['code3']].append(pr)
      else:
        code_name[r['code3']] = [pr]

  # Make sure that every language code3 in the main code table has a
  # name record
  for rr in rec_code:
    if rr[1]['code3'] not in code_name:
      raise MissingNameError('name', rr[1]['code3'])

# Parse the macro table from the given ISO-639-3 data file that stores
# the macrolanguage table and store the parsed result in the
# module-level rec_macro and code_macro variables.
#
# You must use both parse_code() and parse_retire() before this function
# because this function requires the main code table and the retired
# code table to already be parsed so that records can be cross-checked.
#
# See the module documentation and the documentation of the module-level
# variables for further information.
#
# If the function fails, the module-level variables are in an undefined
# state.
#
# Parameters:
#
#   fpath : string - the path to the data file
#
def parse_macro(fpath):

  global rec_macro, code_macro
  global rec_code, code_code
  global rec_retire, code_retire
  
  # Check state
  if (rec_code is None) or (code_code is None):
    raise LogicError()
  if (rec_retire is None) or (code_retire is None):
    raise LogicError()
  
  # Check parameter
  if not isinstance(fpath, str):
    raise LogicError()

  # Clear the records variable to an empty list and set the code
  # dictionary to an empty dictionary
  rec_macro = []
  code_macro = dict()

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  with open(fpath, mode='rt',
            encoding='utf-8', errors='strict') as fin:

    # We have the input file open -- read line by line
    line_num = 0  # Current line number
    fmap = None   # Mapping of fields to column indices
    for line in fin:
      
      # Update line count
      line_num = line_num + 1
      
      # If this is the first line, remove UTF-8 Byte Order Mark (BOM)
      # if present
      if line_num <= 1:
        line = strip_bom(line)
      
      # Trim trailing whitespace and linebreaks
      line = line.rstrip(' \t\n')
      
      # If this is the first line, set up fmap and skip rest of
      # processing
      if line_num <= 1:
        
        # Parse into columns
        cn = line.split('\t')
        
        # Should be at least three columns
        if len(cn) < 3:
          raise BadHeader('macro')
          
        # Trim all column names and make them lowercase
        for x in range(0, len(cn)):
          cn[x] = cn[x].strip(' \t').lower()
        
        # Set fmap variable
        fmap = dict()
        for i in range(0, len(cn)):
          # Get current column name
          n = cn[i]
          
          # Only process this column if one of the recognized column
          # names (in lowercase)
          if (n == 'm_id') or (n == 'i_id') or (n == 'i_status'):
            
            # Map name to standard dictionary name
            if (n == 'm_id'):
              n = 'macro3'
            elif (n == 'i_id'):
              n = 'code3'
            elif (n == 'i_status'):
              n = 'active'
            else:
              raise LogicError()
            
            # Make sure name not already mapped
            if n in fmap:
              raise BadHeader('macro')
            
            # Store name to column index mapping
            fmap[n] = i
        
        # Make sure we found all the required columns
        if ('macro3' not in fmap) or ('code3' not in fmap) or \
            ('active' not in fmap):
          raise BadHeader('macro')
        
        # Skip rest of processing
        continue
      
      # Filter out blank lines that are empty or contain only spaces,
      # tabs, and line breaks
      if len(line) < 1:
        continue
      
      # We have a content line, so parse into fields using the
      # horizontal tab as separator
      fv = line.split('\t')
      
      # Trim each field of leading and trailing whitespace
      for i in range(0, len(fv)):
        fv[i] = fv[i].strip(' \t')
      
      # Create a new record and assign all the fields that are present
      r = dict()
      for fnm in fmap:
        if len(fv) > fmap[fnm]:
          if len(fv[fmap[fnm]]) > 0:
            r[fnm] = fv[fmap[fnm]]
      
      # Make sure the required fields are present
      if 'macro3' not in r:
        raise FieldMissingError('macro', line_num, 'macro3')
      if 'code3' not in r:
        raise FieldMissingError('macro', line_num, 'code3')
      if 'active' not in r:
        raise FieldMissingError('macro', line_num, 'active')
      
      # Check the raw format of the language codes
      if not check_code_3(r['macro3']):
        raise BadCode('macro', line_num, r['macro3'])
      if not check_code_3(r['code3']):
        raise BadCode('macro', line_num, r['code3'])
      
      # Check the active field value and convert to boolean
      if r['active'] == 'A':
        r['active'] = True
      elif r['active'] == 'R':
        r['active'] = False
      else:
        raise BadFieldValue('macro', line_num, r['active'])
      
      # The macro code must be in the main table AND it must map to
      # code3 language code AND the record it maps to must be a
      # macrolanguage record
      if r['macro3'] not in code_code:
        raise BadForeignKey('macro', line_num, r['macro3'])
      if code_code[r['macro3']][1]['code3'] != r['macro3']:
        raise BadForeignKey('macro', line_num, r['macro3'])
      if code_code[r['macro3']][1]['scope'] != 'M':
        raise BadForeignKey('macro', line_num, r['macro3'])
      
      # If the record is active, the code3 must be in the main table AND
      # it must map to code3 language code AND the record it maps to
      # must be an individual language; if the record is not active, the
      # code3 must NOT be in the main table but it MUST be in the retire
      # table
      if r['active']:
        if r['code3'] not in code_code:
          raise BadForeignKey('macro', line_num, r['code3'])
        if code_code[r['code3']][1]['code3'] != r['code3']:
          raise BadForeignKey('macro', line_num, r['code3'])
        if code_code[r['code3']][1]['scope'] != 'I':
          raise BadForeignKey('macro', line_num, r['code3'])
      
      else:
        if r['code3'] in code_code:
          raise BadForeignKey('macro', line_num, r['code3'])
        if r['code3'] not in code_retire:
          raise BadForeignKey('macro', line_num, r['code3'])
      
      # Make sure that the individual language code is not private and
      # not already in the index
      if (r['code3'] in code_macro) or is_private(r['code3']):
        raise RedefineError('macro', line_num, r['code3'])
      
      # Define the tuple pair of the line number and the record
      pr = (line_num, r)
      
      # Add the tuple to the parsed variables
      rec_macro.append(pr)
      code_macro[r['code3']] = pr

# Function that sets all the module-level variables to None.
#
def blank_vars():
  
  global rec_code, code_code
  global rec_name, code_name
  global rec_macro, code_macro
  global rec_retire, code_retire
  
  rec_code = None
  code_code = None
  
  rec_name = None
  code_name = None
  
  rec_macro = None
  code_macro = None
  
  rec_retire = None
  code_retire = None

#
# Public functions
# ----------------
#

# Parse the given ISO-639-3 data files and store the parsed results in
# the module-level rec_ and code_ variables.
#
# See the module documentation and the module-level variables
# documentation for further information.
#
# If all the parsed variables are not None, then the call is ignored.
#
# If the function fails, all the rec and code values will be set to
# None.
#
# Parameters:
#
#   fpath_code : str - the path to the data file holding the main 
#   ISO-639-3 code table
#
#   fpath_name : str - the path to the data file holding the ISO-639-3
#   name table
#
#   fpath_macro : str - the path to the data file holding the ISO-639-3
#   macrolangauge table
#
#   fpath_retire : str - the path to the data file holding the ISO-639-3
#   retire table
#
def parse(fpath_code, fpath_name, fpath_macro, fpath_retire):

  global rec_code, code_code
  global rec_name, code_name
  global rec_macro, code_macro
  global rec_retire, code_retire

  # Ignore call if all variables already set
  if (rec_code is not None) and (code_code is not None) and \
      (rec_name is not None) and (code_name is not None) and \
      (rec_macro is not None) and (code_macro is not None) and \
      (rec_retire is not None) and (code_retire is not None):
    return

  # Blank all the module-level variables
  blank_vars()

  # Check parameters
  if (not isinstance(fpath_code, str)) or \
      (not isinstance(fpath_retire, str)) or \
      (not isinstance(fpath_name, str)) or \
      (not isinstance(fpath_macro, str)):
    raise LogicError()

  # Try to parse all the tables in the proper parsing order
  try:
    
    try:
      parse_code(fpath_code)
    except FileNotFoundError:
      raise NoDataFileError('code')
    except ValueError:
      raise BadDataFile('code')
    
    try:
      parse_retire(fpath_retire)
    except FileNotFoundError:
      raise NoDataFileError('retire')
    except ValueError:
      raise BadDataFile('retire')
      
    try:
      parse_name(fpath_name)
    except FileNotFoundError:
      raise NoDataFileError('name')
    except ValueError:
      raise BadDataFile('name')
      
    try:
      parse_macro(fpath_macro)
    except FileNotFoundError:
      raise NoDataFileError('macro')
    except ValueError:
      raise BadDataFile('macro')
    
  except ISO3Error as se:
    blank_vars()
    raise se
  
  except Exception as exc:
    blank_vars()
    raise ISO3Error() from exc

# @@TODO:
parse('data/iso-639-3.tab', 'data/iso-639-3_Name_Index.tab', 'data/iso-639-3-macrolanguages.tab', 'data/iso-639-3_Retirements.tab')
