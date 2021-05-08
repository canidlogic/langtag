#
# fulldb.py
# =========
#
# Python-3 module for loading all the language databases and performing
# interdatabase checks to make sure the databases are consistent with
# each other.
#
# Use the parse_all function to load all the individual database modules
# and check consistency across them.
#
# For corrected records, see the fix_ functions.
#
# This makes use of the following imported modules:
#
import iso2
import iso3
import iso5
import subtag

#
# Exceptions
# ----------
#
# Each exception overloads the __str__ operator so that it can be
# printed as a user-friendly error message.  The error message has
# punctuation at the end, but it does NOT have a line break at the end.
#
# All exceptions defined by this module are subclasses of FullDBError.
#

# Utility function that forms the error message prefix for all the
# exceptions defined in this class.
#
# All parameters are optional and may be left at None.  The prefix
# always includes the text "FullDB" and the prefix always
# ends in a colon and a space.
#
# If invalid parameters are given, they are replaced by None.
#
# Parameters:
#
#   val : str | None - if provided, the specific value that caused an
#   error
#
# Return:
#
#   a string containing the proper exception message prefix
#
def ex_msg_prefix(val=None):
  # Check and fix parameters
  if not isinstance(val, str):
    val = None
  
  # If value given, escape " in value as ""
  if val is not None:
    val = val.replace('"', '""')
  
  # Form the proper prefix
  if val is not None:
    return 'FullDB value "' + val + '": '
  else:
    return 'FullDB: '

class FullDBError(Exception):
  def __str__(self):
    return ex_msg_prefix() + 'Unknown full database error!'

class LogicError(FullDBError):
  def __str__(self):
    return ex_msg_prefix() + 'Internal logic error!'

class ISO2MappingError(FullDBError):
  def __init__(self, val=None):
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_val) + \
      'ISO-639-2 language code doesn\'t upgrade properly!'

class RemappingError(FullDBError):
  def __init__(self, val=None):
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_val) + \
      'Subtag registry language remapping doesn\'t map properly!'

class SubtagMappingError(FullDBError):
  def __init__(self, val=None):
    self.m_val = val
  def __str__(self):
    return ex_msg_prefix(self.m_val) + \
      'Subtag registry language code doesn\'t map properly!'

#
# Class definitions
# -----------------
#

# Class for storing a complete set of file paths to data files.
#
# The following properties are defined:
#
#   .subtag_path
#   .iso2_path
#   .iso3_code_path
#   .iso3_name_path
#   .iso3_macro_path
#   .iso3_retire_path
#   .iso5_path
#
# Each of these is initially set to None.  Property "set" methods check
# that the given value is a non-empty string, throwing an exception if
# it is not.  Property "get" methods throw an exception if an attempt is
# made to read a property that hasn't been set yet.  Attempts to delete
# any of the properties cause exceptions.
#
# The completed() function only returns True if all fields have been
# filled in and all properties can be accessed without exceptions.
#
class DataFilePaths:
  
  # Constructor just initializes all fields to None
  #
  def __init__(self):
    self.m_subtag = None
    self.m_iso2 = None
    self.m_iso3_code = None
    self.m_iso3_name = None
    self.m_iso3_macro = None
    self.m_iso3_retire = None
    self.m_iso5 = None
  
  # Function to check whether all the fields have been filled in.
  #
  # Return:
  #
  #   True if everything filled in, False otherwise
  #
  def completed(self):
    if (self.m_subtag is not None) and \
        (self.m_iso2 is not None) and \
        (self.m_iso3_code is not None) and \
        (self.m_iso3_name is not None) and \
        (self.m_iso3_macro is not None) and \
        (self.m_iso3_retire is not None) and \
        (self.m_iso5 is not None):
      return True
    else:
      return False
  
  # Set methods 
  #
  def set_subtag(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_subtag = value
  
  def set_iso2(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_iso2 = value
  
  def set_iso3_code(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_iso3_code = value
  
  def set_iso3_name(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_iso3_name = value
  
  def set_iso3_macro(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_iso3_macro = value
  
  def set_iso3_retire(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_iso3_retire = value
  
  def set_iso5(self, value):
    if not isinstance(value, str):
      raise LogicError()
    if len(value) < 1:
      raise LogicError()
    self.m_iso5 = value
  
  # Get methods
  #
  def get_subtag(self):
    value = self.m_subtag
    if value is not None:
      return value
    else:
      raise LogicError()
  
  def get_iso2(self):
    value = self.m_iso2
    if value is not None:
      return value
    else:
      raise LogicError()
  
  def get_iso3_code(self):
    value = self.m_iso3_code
    if value is not None:
      return value
    else:
      raise LogicError()
  
  def get_iso3_name(self):
    value = self.m_iso3_name
    if value is not None:
      return value
    else:
      raise LogicError()
  
  def get_iso3_macro(self):
    value = self.m_iso3_macro
    if value is not None:
      return value
    else:
      raise LogicError()

  def get_iso3_retire(self):
    value = self.m_iso3_retire
    if value is not None:
      return value
    else:
      raise LogicError()
  
  def get_iso5(self):
    value = self.m_iso5
    if value is not None:
      return value
    else:
      raise LogicError()
  
  # Delete methods
  #
  def del_subtag(self):
    raise LogicError()
    
  def del_iso2(self):
    raise LogicError()
  
  def del_iso3_code(self):
    raise LogicError()
  
  def del_iso3_name(self):
    raise LogicError()
  
  def del_iso3_macro(self):
    raise LogicError()
  
  def del_iso3_retire(self):
    raise LogicError()
  
  def del_iso5(self):
    raise LogicError()
  
  # Define properties
  #
  subtag_path = property(get_subtag, set_subtag, del_subtag)
  iso2_path = property(get_iso2, set_iso2, del_iso2)
  iso3_code_path = property(get_iso3_code, set_iso3_code, del_iso3_code)
  iso3_name_path = property(get_iso3_name, set_iso3_name, del_iso3_name)
  iso3_macro_path = property(
                      get_iso3_macro, set_iso3_macro, del_iso3_macro)
  iso3_retire_path = property(
                      get_iso3_retire, set_iso3_retire, del_iso3_retire)
  iso5_path = property(get_iso5, set_iso5, del_iso5)
  
#
# Local functions
# ---------------
#

# Given a language code from ISO-639-2, check whether it is one of the
# language codes that does not properly map to ISO-639-3 or ISO-639-5.
#
# This only is the language code "him", which it seems should be in
# ISO-639-5 as it refers to a collection of languages.
#
# The given language code should be the term3 code if present, else the
# biblio3 code.
#
# Parameters:
#
#   k : str - the language code from ISO-639-2 to check
#
# Return:
#
#   True if this is one of the exceptional unmapped codes, False
#   otherwise
#
def fix_iso2_map(k):
  
  if not isinstance(k, str):
    raise LogicError()
  
  if (k == 'him'):
    return True
  else:
    return False

# Given a language code from ISO-639-2, check whether it is one of the
# language codes that has a code2 but is in ISO-639-5.
#
# This only is the language code "bih" which refers to a language group
# but has the code2 "bh", which is not recorded in ISO-639-5.
#
# The given language code should be the term3 code if present, else the
# biblio3 code.
#
# Parameters:
#
#   k : str - the language code from ISO-639-2 to check
#
# Return:
#
#   True if this is one of the exceptional ISO-639-2 codes with a code2
#   that is in ISO-639-5, False otherwise
#
def special_iso2_code2(k):
  
  if not isinstance(k, str):
    raise LogicError()
  
  if (k == 'bih'):
    return True
  else:
    return False

# Given a language code, check whether it is one of the "extra" language
# codes.
#
# These are the language codes from the exceptional records in the
# functions fix_iso2_map() and special_iso2_code2(), including alternate
# forms such as code2.
#
# Parameters:
#
#   k : str - the language code to check
#
# Return:
#
#   True if this is one of the extra codes, False otherwise
#
def extra_iso2_code(k):
  
  if not isinstance(k, str):
    raise LogicError()
  
  if (k == 'him') or (k == 'bih') or (k == 'bh'):
    return True
  else:
    return False

# Check whether a given language code is an archaic language tag found
# only in the subtag registry.
#
# Archaic tags are all two-letter tags, they are not found in the ISO
# tables, and all of them have mappings to modernized codes that are
# found in the ISO tables.
#
# Parameters:
#
#   k : str - the language code to check
#
# Return:
#
#   True if this is one of the archaic language tags, False otherwise
#
def archaic_langtag(k):
  
  if not isinstance(k, str):
    raise LogicError()
  
  if (k == 'in') or (k == 'iw') or \
      (k == 'ji') or (k == 'jw') or (k == 'mo'):
    return True
  else:
    return False

# Check whether a given language code has a "split remapping."
#
# A split remapping occurs when the language code is remapped one way in
# the subtag registry and a different way in the ISO-639-3 retire table.
#
# This happens in the lone case when the IANA registry remaps a
# three-letter language code to a two-letter language code.  The
# ISO-639-3 retire table can't document this kind of mapping, so it
# remaps to the equivalent three-letter language code instead.
#
# Parameters:
#
#   k : str - the language code to check
#
# Return:
#
#   True if this code has a split remapping, False otherwise
#
def split_remap(k):

  if not isinstance(k, str):
    raise LogicError()
  
  if k == 'adp':
    return True
  else:
    return False

#
# Public functions
# ----------------
#

# Parse all the database files and check consistency across databases.
#
# See the individual subtag, iso2, iso3, and iso5 module documentation
# for details about parsing each data file.
#
# Database files that are already loaded are not loaded again.
#
# If the function fails, the state of individual modules is undefined.
#
# Pass a DataFilePaths object that has been completed with all paths
# filled in.
#
# Parameters:
#
#   paths : DataFilePaths - the completed object storing all the data
#   file paths
#
def parse_all(paths):
  
  # Check parameter
  if not isinstance(paths, DataFilePaths):
    raise LogicError()
  if not paths.completed():
    raise LogicError()

  # Load all the individual databases
  subtag.parse(paths.subtag_path)
  iso2.parse(paths.iso2_path)
  iso3.parse(
      paths.iso3_code_path,
      paths.iso3_name_path,
      paths.iso3_macro_path,
      paths.iso3_retire_path)
  iso5.parse(paths.iso5_path)

  # Every record in the ISO-639-2 database must have an equivalent
  # record either in the ISO-639-3 main code table or ISO-639-5;
  # furthermore, this mapping must always be by the term3 code if given,
  # else by the biblio3 code; finally, any ISO-639-2 record that has a
  # term3 and/or a code2 must be in the ISO-639-3 main code table and
  # have these additional codes registered there; for exceptions, see
  # fix_iso2_map() and special_iso2_code2()
  for rr in iso2.rec:
    # Get the record fields
    r = rr[1]
    
    # Start with key as the biblio3 code, which is present in all
    # records
    k = r['biblio3']
    
    # If term3 code is present, then use that instead as the key
    if 'term3' in r:
      k = r['term3']
    
    # If this is one of the exception unmapped records, skip the check
    if fix_iso2_map(k):
      continue
    
    # Look for the record in one of the external databases
    if k in iso3.code_code:
      # Found the key in ISO-639-3 main code table -- make sure that the
      # key maps to the code3 column
      if iso3.code_code[k][1]['code3'] != k:
        raise ISO2MappingError(k)
      
      # Get the ISO-639-3 record
      ru = iso3.code_code[k][1]
      
      # If the ISO-639-2 record has a code2, the ISO-639-3 record must
      # have a matching one
      if 'code2' in r:
        if 'code2' not in ru:
          raise ISO2MappingError(k)
        if r['code2'] != ru['code2']:
          raise ISO2MappingError(k)
        
      # If the term3 code is present in the ISO-639-2 record, make sure
      # that the biblio3 code in ISO-639-2 has a matching biblio3 code
      # in ISO-639-3
      if 'term3' in r:
        if 'biblio3' not in ru:
          raise ISO2MappingError(k)
        if r['biblio3'] != ru['biblio3']:
          raise ISO2MappingError(k)
    
    elif k in iso5.code:
      # Found the key in ISO-639-5 -- must not have a term3 in the
      # record
      if 'term3' in r:
        raise ISO2MappingError(k)
      
      # Must not have a code2 in the record, unless it is one of the
      # exceptional records
      if not special_iso2_code2(k):
        if 'code2' in r:
          raise ISO2MappingError(k)
    
    else:
      # Did not find the key in any of the upgrade tables
      raise ISO2MappingError(k)

  # Every language subtag in the subtag registry must map to a code in
  # either the ISO-639-3 main code table, the ISO-639-3 retire table,
  # ISO-639-5, extra_iso2_code(), or archaic_langtag(); also, the subtag
  # record for the range of codes qaa..qtz for private use is skipped
  for rr in subtag.rec:
    # Get the record fields
    r = rr[1]
    
    # Skip this if not a language record
    if r['type'] != 'language':
      continue
    
    # Get the subtag
    sv = r['subtag']
    
    # Skip if range of records for private use
    if (sv == 'qaa..qtz'):
      continue
    
    # Check that it maps correctly
    if (sv not in iso3.code_code) and \
        (sv not in iso3.code_retire) and \
        (sv not in iso5.code) and \
        (not extra_iso2_code(sv)) and \
        (not archaic_langtag(sv)):
      raise SubtagMappingError(sv)

  # Every language subtag remapping in the subtag registry must also be
  # present in the ISO-639-3 retire table, except for the mappings of
  # the archaic_langtag() language subtags; also, all remappings must be
  # the same, except for language tags in split_remap()
  for rr in subtag.rec:
    # Get the record fields
    r = rr[1]
    
    # Skip this if not a language record
    if r['type'] != 'language':
      continue
    
    # Skip this if no preferred value
    if 'preferred-value' not in r:
      continue
    
    # Skip this if archaic language tag
    if archaic_langtag(r['subtag']):
      continue
    
    # Check that language tag is in retire table
    if r['subtag'] not in iso3.code_retire:
      raise RemappingError(r['subtag'])
    
    # Get the retire table record fields
    s = iso3.code_retire[r['subtag']][1]
    
    # The mapping field must be present
    if 'mapping' not in s:
      raise RemappingError(r['subtag'])
    
    # Don't verify that remappings are the same if this is a split
    # remapping
    if split_remap(r['subtag']):
      continue
    
    # The mapping must be the same
    if r['preferred-value'] != s['mapping']:
      raise RemappingError(r['preferred-value'])
