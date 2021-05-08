#
# subtag.py
# =========
#
# Python-3 module for loading and parsing the Language Subtag Registry
# from IANA.
#
# A current copy of the registry can be downloaded from IANA at the
# following address:
#
#   https://www.iana.org/assignments/
#   language-subtag-registry/language-subtag-registry
#
# The format of this registry file is defined in RFC 5646 "Tags for
# Identifying Languages"
#
# To use this module, import subtag and then call subtag.parse() with
# the path to the IANA data file.  If this is successful, the result
# will be placed in the subtag.rec variable.
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
# All exceptions defined by this module are subclasses of SubtagError.
#

class SubtagError(Exception):
  def __str__(self):
    return 'Unknown subtag parsing error!'

class BadContinueLine(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Invalid location for continuation line!'
    else:
      return 'Invalid location for continuation line!'

class BadDataFile(SubtagError):
  def __str__(self):
    return 'Subtag data file has invalid UTF-8 encoding!'

class BadExtlangRemap(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'extlang record has improper remap!'
    else:
      return 'extlang record has improper remap!'

class BadExtlangSubtag(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'extlang subtag ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid extlang subtag!'
      
    else:
      return 'Record has invalid extlang subtag!'

class BadLanguageSubtag(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Language subtag ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid language subtag!'
      
    else:
      return 'Record has invalid language subtag!'

class BadPrefix(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Prefix ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid prefix!'
      
    else:
      return 'Record has invalid prefix!'

class BadRecordType(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record type ' + self.m_tname + ' is unrecognized!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has unrecognized type!'
      
    else:
      return 'Record has unrecognized type!'

class BadRegionSubtag(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Region subtag ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid region subtag!'
      
    else:
      return 'Record has invalid region subtag!'

class BadScriptSubtag(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Script subtag ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid script subtag!'
      
    else:
      return 'Record has invalid script subtag!'

class BadScriptSuppress(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Script suppression ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid script suppression!'
      
    else:
      return 'Record has invalid script suppression!'

class BadTagFormat(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Tag ' + self.m_tname + ' has invalid format!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid tag format!'
      
    else:
      return 'Record has invalid tag format!'

class BadVariantSubtag(SubtagError):
  def __init__(self, line=None, tname=None):
    self.m_line = line
    self.m_tname = tname
  def __str__(self):
    if (self.m_line is not None) and (self.m_tname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Variant subtag ' + self.m_tname + ' is invalid!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid variant subtag!'
      
    else:
      return 'Record has invalid variant subtag!'

class EmptyFieldName(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'One of the record field names is empty!'
    else:
      return 'One of the record field names is empty!'

class InvalidFieldName(SubtagError):
  def __init__(self, line=None, fname=None):
    self.m_line = line
    self.m_fname = fname
  def __str__(self):
    if (self.m_line is not None) and (self.m_fname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record field ' + self.m_fname + ' has invalid field name!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has invalid field name!'
      
    else:
      return 'Record has invalid field name!'

class LogicError(SubtagError):
  def __str__(self):
    return 'Internal logic error within subtag module!'

class MissingKeyError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has broken foreign key!'
    else:
      return 'Record has broken foreign key!'

class MissingTypeError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record is missing a Type field!'
    else:
      return 'Record is missing a Type field!'

class MultiFieldError(SubtagError):
  def __init__(self, line=None, fname=None):
    self.m_line = line
    self.m_fname = fname
  def __str__(self):
    if (self.m_line is not None) and (self.m_fname is not None):
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record field ' + self.m_fname + ' is defined more than once!'
    
    elif self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has redefined field!'
      
    else:
      return 'Record has redefined field!'
  
class NoColonError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag record at line ' + str(self.m_line) + ': ' + \
        'Record has line without colon!'
    else:
      return 'Record has line without colon!'

class NoDataFileError(SubtagError):
  def __init__(self, fpath=None):
    self.m_fpath = fpath
  def __str__(self):
    if self.m_fpath is not None:
      return 'Can\'t find subtag data file ' + self.m_fpath
    else:
      return 'Can\'t find subtag data file!'

class PrefixContextError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Prefix field can\'t be used with this kind of record!'
    else:
      return 'Prefix field can\'t be used with this kind of record!'

class PrefixMultiError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Multiple prefixes can\'t be used on this kind of record!'
    else:
      return 'Multiple prefixes can\'t be used on this kind of record!'

class RecursiveMappingError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Record has recursive remapping!'
    else:
      return 'Record has recursive remapping!'

class RedefinitionError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Record redefines key from previous record!'
    else:
      return 'Record redefines key from previous record!'

class ScriptContextError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Script suppression can\'t be used on this kind of record!'
    else:
      return 'Script suppression can\'t be used on this kind of record!'

class WrongTagTypeError(SubtagError):
  def __init__(self, line=None):
    self.m_line = line
  def __str__(self):
    if self.m_line is not None:
      return 'Subtag data line ' + str(self.m_line) + ': ' + \
        'Record has wrong type of tag data!'
    else:
      return 'Record has wrong type of tag data!'

#
# Module-level variables
# ----------------------
#

# The module-level variable that stores the result of parsing the data
# file, or None if the file hasn't been parsed yet.
#
# Use the parse() function to set this variable.  Once it is set
# successfully, it will be a list of zero or more records, stored in the
# order they appear in the data file.  However, the first record in the
# file will NOT be included in this list, so the first element in this
# list is actually the second record in the file.  This is because the
# first record in the file is an exceptional record that simply provides
# a timestamp for when the data file was generated.
#
# Each record is a tuple with two elements.  The first element is an
# integer that stores the line number of the first line of the record in
# the data file.  The second element is a dictionary that maps field
# names to field values.
#
# The field names are the same as the field names given in the data
# file, except that they are converted to lowercase so that they are
# case insensitive.  Field names do NOT include the colon.
#
# The field values are the same as the field values given in the data
# file.  Continuation lines have been assembled so that a field value
# that appears across multiple lines in the input data file will be a
# single line in the value here, with each line break replaced by a
# single space character.  The value will be trimmed of leading and
# trailing spaces, tabs, and line breaks.
#
# The fields named 'description' 'comments' and 'prefix' are special
# because multiple instances of the field is allowed in a single record.
# To handle this, the parsed field values of these fields will be a list
# of strings.  If there is just one instance of the field, there will be
# a one-element list.  This only applies to these three special field
# values.  All other field values will be strings.
#
rec = None

#
# Local functions
# ---------------
#

# Check whether the given parameter is a string that contains a single
# lowercase ASCII letter.
#
# Parameters:
#
#   c : str | mixed - the value to check
#
# Return:
#
#   True if c is a lowercase ASCII letter, False otherwise
#
def is_lower_letter(c):
  if not isinstance(c, str):
    return False
  if len(c) != 1:
    return False
  c = ord(c)
  if (c >= ord('a')) and (c <= ord('z')):
    return True
  else:
    return False

# Check whether the given parameter is a string that contains a single
# uppercase ASCII letter.
#
# Parameters:
#
#   c : str | mixed - the value to check
#
# Return:
#
#   True if c is a uppercase ASCII letter, False otherwise
#
def is_upper_letter(c):
  if not isinstance(c, str):
    return False
  if len(c) != 1:
    return False
  c = ord(c)
  if (c >= ord('A')) and (c <= ord('Z')):
    return True
  else:
    return False

# Check whether the given parameter is a string that contains a single
# ASCII decimal digit.
#
# Parameters:
#
#   c : str | mixed - the value to check
#
# Return:
#
#   True if c is an ASCII decimal digit, False otherwise
#
def is_digit(c):
  if not isinstance(c, str):
    return False
  if len(c) != 1:
    return False
  c = ord(c)
  if (c >= ord('0')) and (c <= ord('9')):
    return True
  else:
    return False

# Check whether the given parameter is a string that contains a validly
# formatted tag.
#
# Parameters:
#
#   t : str | mixed - the value to check
#
# Return:
#
#   True if t is a validly formatted tag, False otherwise
#
def is_format_tag(t):
  
  # Check that t is a string
  if not isinstance(t, str):
    return False
  
  # Check that t is not empty
  if len(t) < 1:
    return False
  
  # Check that t contains only ASCII alphanumerics and hyphens, and
  # furthermore that hyphen is neither first nor last character, nor
  # does a hyphen ever occur immediately after another hyphen
  tl = len(t)
  for x in range(0, tl):
    c = t[x]
    if (not is_upper_letter(c)) and \
        (not is_lower_letter(c)) and \
        (not is_digit(c)) and \
        (c != '-'):
      return False
    if c == '-':
      if (x < 1) or (x >= tl - 1):
        return False
      if t[x - 1] == '-':
        return False
  
  # Split the tag into subtags using hyphen as separator
  ta = t.split('-')
  
  # Check subtag formatting
  first_tag = True
  found_singleton = False
  for tg in ta:
    
    # If this is the first tag, then just check that it doesn't have any
    # uppercase letters, clear first_tag, set found_singleton if the
    # first tag is only one character, and skip rest of checks
    if first_tag:
      first_tag = False
      for c in tg:
        if is_upper_letter(c):
          return False
      if len(tg) <= 1:
        found_singleton = True
      continue
    
    # If we've encountered a singleton, then just make sure there are no
    # uppercase letters and skip rest of checks
    if found_singleton:
      for c in tg:
        if is_upper_letter(c):
          return False
      continue
    
    # Different handling depending on length of subtag
    if len(tg) < 2:
      # Found a singleton, so set found_singleton flag and make sure not
      # an uppercase letter
      if is_upper_letter(tg):
        return False
      found_singleton = True
      
    elif len(tg) == 2:
      # Two-character subtag that is not first subtag and not after a
      # singleton, so must not have lowercase letters
      for c in tg:
        if is_lower_letter(c):
          return False
      
    elif len(tg) == 4:
      # Four-character subtag that is not first subtag and not after a
      # singleton, so first character must not be lowercase and rest of
      # characters must not be uppercase
      if is_lower_letter(tg[0]) or \
          is_upper_letter(tg[1]) or \
          is_upper_letter(tg[2]) or \
          is_upper_letter(tg[3]):
        return False
      
    else:
      # In all other cases, do not allow uppercase letters
      for c in tg:
        if is_upper_letter(c):
          return False
  
  # If we got all the way here, tag checks out
  return True

# Check whether the given parameter is a string that contains a validly
# formatted tag, without extensions or private-use or grandfathered
# formats.
#
# Parameters:
#
#   t : str | mixed - the value to check
#
# Return:
#
#   True if t is a validly formatted core tag, False otherwise
#
def is_core_tag(t):
  
  # If not a formatted tag, then return False
  if not is_format_tag(t):
    return False
  
  # Split the tag into subtags using hyphen as separator
  ta = t.split('-')
  
  # Make sure there are no singletons or private use flags
  for tg in ta:
    if len(tg) < 2:
      return False
  
  # If we got here, tag checks out
  return True

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

# Check whether the given string value has leading or trailing padding.
#
# This returns True if the first or last character is a space, tab, or
# line break.  Otherwise, it returns False.  Empty strings return False.
# Non-strings cause an exception.
#
# Parameters:
#
#   s : str - the string value to check
#
# Return:
#
#   True if value is padded, False if not
#
def has_padding(s):
  
  # Check parameter
  if not isinstance(s, str):
    raise LogicError()
  
  # Empty strings return False
  if len(s) < 1:
    return False
  
  # Check first and last character
  for x in range(0, 2):
    # Get appropriate character
    c = None
    if x == 0:
      c = s[0]
    elif x == 1:
      c = s[-1]
    else:
      raise LogicError()  # shouldn't happen
    
    # Check that character is not space, tab, or line break
    if (c == ' ') or (c == '\t') or (c == '\n'):
      return True
  
  # If we got here, string is not padded
  return False

# Check that a parsed record conforms to various expectations.
#
# Exceptions are thrown if there are problems with the record.  The
# LogicError exception is used for situations that should never be
# possible from any input data.
#
# Parameters:
#
#   lnum : int - a line number, greater than zero, at which the record
#   starts, which is used for error reporting
#
#   f : dict - maps lowercased record field names to their values
#
def check_record(lnum, f):
  
  # Check parameters
  if not isinstance(lnum, int):
    raise LogicError()
  if lnum < 1:
    raise LogicError()
  if not isinstance(f, dict):
    raise LogicError()
  
  # Main check of all keys and values in dictionary
  for k in list(f):
    # Each key must be a string
    if not isinstance(k, str):
      raise LogicError()
    
    # Each key should be non-empty
    if len(k) < 1:
      raise EmptyFieldName(lnum)
    
    # Each key must be non-padded
    if has_padding(k):
      raise LogicError()
    
    # Each key must be only in lowercase and have at least one lowercase
    # letter
    if not k.islower():
      raise InvalidFieldName(lnum, k)
    
    # Each value must be a string without padding, except that
    # "description" "comments" and "prefix" field values must be
    # non-empty lists of strings without padding
    val = f[k]
    if (k == 'description') or (k == 'comments') or (k == 'prefix'):
      # Value must be non-empty list of strings without padding
      if not isinstance(val, list):
        raise LogicError()
      if len(val) < 1:
        raise LogicError()
      for e in val:
        if not isinstance(e, str):
          raise LogicError()
        if has_padding(e):
          raise LogicError()
      
    else:
      # Value must be string without padding
      if not isinstance(val, str):
        raise LogicError()
      if has_padding(val):
        raise LogicError()
    
  # All records must have a "type" field that is one of the recognized
  # categories
  if 'type' not in f:
    raise MissingTypeError(lnum)
  if not valid_category(f['type']):
    raise BadRecordType(lnum, f['type'])
  
  # Grandfathered or redundant records must have a "tag" field but not a
  # "subtag" field, while all other records must have a "subtag" field
  # but not a "tag" field
  if (f['type'] == 'grandfathered') or (f['type'] == 'redundant'):
    # Must have tag field but not subtag
    if ('tag' not in f) or ('subtag' in f):
      raise WrongTagTypeError(lnum)
    
  else:
    # Must have subtag field but not tag
    if ('subtag' not in f) or ('tag' in f):
      raise WrongTagTypeError(lnum)
  
  # If this is a subtag record, check the subtag value format
  if 'subtag' in f:
    ft = f['type']
    sv = f['subtag']
    if ft == 'language':
      # Languages must be two or three lowercase ASCII letters (language
      # tags that are longer are not used in practice); the only
      # exception is 8-character language ranges where the first three
      # chars are lowercase letters, the last three chars are lowercase
      # letters, and the middle two chars are ".."
      if ((len(sv) < 2) or (len(sv) > 3)) and (len(sv) != 8):
        raise BadLanguageSubtag(lnum, sv)
      if len(sv) == 8:
        if (not is_lower_letter(sv[0])) or \
            (not is_lower_letter(sv[1])) or \
            (not is_lower_letter(sv[2])) or \
            (sv[3] != '.') or (sv[4] != '.') or \
            (not is_lower_letter(sv[5])) or \
            (not is_lower_letter(sv[6])) or \
            (not is_lower_letter(sv[7])):
          raise BadLanguageSubtag(lnum, sv)
      else:
        for c in sv:
          if not is_lower_letter(c):
            raise BadLanguageSubtag(lnum, sv)
      
    
    elif ft == 'extlang':
      # extlang subtags must be three lowercase ASCII letters
      if len(sv) != 3:
        raise BadExtlangSubtag(lnum, sv)
      for c in sv:
        if not is_lower_letter(c):
          raise BadExtlangSubtag(lnum, sv)
      
    elif ft == 'script':
      # Script subtags must be four ASCII letters, the first of which is
      # uppercase and the rest of which are lowercase; the only
      # exception is 10-character script subtag ranges, where the first
      # four letters are a valid script tag, the last four letters are a
      # valid script subtag, and the middle two characters are ".."
      if len(sv) == 4:
        if (not is_upper_letter(sv[0])) or \
            (not is_lower_letter(sv[1])) or \
            (not is_lower_letter(sv[2])) or \
            (not is_lower_letter(sv[3])):
          raise BadScriptSubtag(lnum, sv)
      elif len(sv) == 10:
        if (not is_upper_letter(sv[0])) or \
            (not is_lower_letter(sv[1])) or \
            (not is_lower_letter(sv[2])) or \
            (not is_lower_letter(sv[3])) or \
            (sv[4] != '.') or (sv[5] != '.') or \
            (not is_upper_letter(sv[6])) or \
            (not is_lower_letter(sv[7])) or \
            (not is_lower_letter(sv[8])) or \
            (not is_lower_letter(sv[9])):
          raise BadScriptSubtag(lnum, sv)
      else:
        raise BadScriptSubtag(lnum, sv)
    
    elif ft == 'region':
      # Region subtags must be two uppercase ASCII letters or three
      # ASCII digits or they must be a range
      if len(sv) == 2:
        if (not is_upper_letter(sv[0])) or (not is_upper_letter(sv[1])):
          raise BadRegionSubtag(lnum, sv)
        
      elif len(sv) == 3:
        for c in sv:
          if not is_digit(c):
            raise BadRegionSubtag(lnum, sv)
      
      elif len(sv) == 6:
        if (not is_upper_letter(sv[0])) or \
            (not is_upper_letter(sv[1])) or \
            (sv[2] != '.') or (sv[3] != '.') or \
            (not is_upper_letter(sv[4])) or \
            (not is_upper_letter(sv[5])):
          raise BadRegionSubtag(lnum, sv)
      
      else:
        raise BadRegionSubtag(lnum, sv)
    
    elif ft == 'variant':
      # Variants must either be four lowercase ASCII alphanumerics and
      # begin with a digit, or 5-8 lowercase ASCII alphanumerics
      if (len(sv) < 4) or (len(sv) > 8):
        raise BadVariantSubtag(lnum, sv)
      if len(sv) == 4:
        if not is_digit(sv[0]):
          raise BadVariantSubtag(lnum, sv)
      for c in sv:
        if (not is_lower_letter(c)) and (not is_digit(c)):
          raise BadVariantSubtag(lnum, sv)
      
    else:
      raise LogicError()  # shouldn't happen
  
  # If this is a tag record, check tag format
  if 'tag' in f:
    if not is_format_tag(f['tag']):
      raise BadTagFormat(lnum, f['tag'])
  
  # If this record has prefixes, additional checks
  if 'prefix' in f:
    # Prefixes only possible on extlang and variant records
    if (f['type'] != 'extlang') and (f['type'] != 'variant'):
      raise PrefixContextError(lnum)
    
    # If this is an extlang record, no more than one prefix allowed
    if f['type'] == 'extlang':
      if len(f['prefix']) > 1:
        raise PrefixMultiError(lnum)
    
    # All prefix values must be two or three lowercase letters for
    # extlang prefixes
    if f['type'] == 'extlang':
      for p in f['prefix']:
        if (len(p) < 2) or (len(p) > 3):
          raise BadPrefix(lnum, p)
        for c in p:
          if not is_lower_letter(c):
            raise BadPrefix(lnum, p)
            
    # All prefix values must be core tags for variant records
    if f['type'] == 'variant':
      for p in f['prefix']:
        if not is_core_tag(p):
          raise BadPrefix(lnum, p)
  
  # If this record has a suppress-script, additional checks
  if 'suppress-script' in f:
    # Script suppression only possible on language and extlang records
    if (f['type'] != 'language') and (f['type'] != 'extlang'):
      raise ScriptContextError(lnum)
    
    # Script name must be four characters, first uppercase letter and
    # the rest lowercase letters
    sn = f['suppress-script']
    if len(sn) != 4:
      raise BadScriptSuppress(lnum, sn)
    if (not is_upper_letter(sn[0])) or \
        (not is_lower_letter(sn[1])) or \
        (not is_lower_letter(sn[2])) or \
        (not is_lower_letter(sn[3])):
      raise BadScriptSuppress(lnum, sn)

# Function that processes a raw record.
#
# A raw record requires an array of record lines.  Trailing whitespace
# and line breaks should have been stripped from these lines already.
# Furthermore, continuation lines should be assembled so that the lines
# here are logical record lines rather than the physical record lines
# that occur in the file.
#
# The module-level rec variable must already be defined as a list.  If
# successful, this function adds the parsed record on to the list.
#
# Parameters:
#
#   lnum : int - a line number, greater than zero, at which the record
#   starts, which is used for error reporting
#
#   lines : list of strings - the logical lines of the record
#
def raw_record(lnum, lines):
  
  global rec
  
  # Check state
  if not isinstance(rec, list):
    raise LogicError()
  
  # Check parameters
  if not isinstance(lnum, int):
    raise LogicError()
  if lnum < 1:
    raise LogicError()
  if not isinstance(lines, list):
    raise LogicError()
  for e in lines:
    if not isinstance(e, str):
      raise LogicError()

  # Convert each logical line into a mapping of field names in lowercase
  # to field values 
  rp = dict()
  for e in lines:
    
    # Find the location of the first : character, which must be present
    ci = e.find(':')
    if ci < 0:
      raise NoColonError(lnum)
    
    # Split into a field name and a field value around the colon
    fname = ''
    fval = ''
    if ci > 0:
      fname = e[0:ci]
    if ci < len(e) - 1:
      fval = e[ci + 1:]
    
    # Trim field name and field value of leading and trailing space
    fname = fname.strip(' \t\n')
    fval = fval.strip(' \t\n')
    
    # Convert field name to lowercase
    fname = fname.lower()
    
    # Different handling based on whether the field name is a special
    # field that can occur multiple times
    if (fname == 'description') or (fname == 'comments') or \
        (fname == 'prefix'):
      # This field can occur multiple times, so check if already present
      # and handle differently
      if fname in rp:
        # We already have a previous instance of this field, so just add
        # the new value as another array element
        rp[fname].append(fval)
        
      else:
        # We don't have a previous instance of this field, so create a
        # new field entry with our value as the first element of a list
        rp[fname] = [fval]
      
    else:
      # This field can only occur once, so make sure it's not already
      # present
      if fname in rp:
        raise MultiFieldError(lnum, fname)
      
      # Add a mapping for this field name to value
      rp[fname] = fval
  
  # We got a mapping of field names to values, so check the record and
  # store the record as a pair with record line number and record fields
  check_record(lnum, rp)
  rec.append((lnum, rp))

#
# Public functions
# ----------------
#

# Parse the given subtag data file and store the parsed result in the
# module-level rec variable.
#
# See the module documentation and the documentation of the rec variable
# for further information.
#
# If the rec value is already set, this function call will be ignored.
#
# If the function fails, the rec value will be set to None.
#
# Parameters:
#
#   fpath : string - the path to the subtag data file
#
def parse(fpath):

  global rec

  # Ignore call if rec already set
  if rec is not None:
    return

  # Check parameter
  if not isinstance(fpath, str):
    rec = None
    raise LogicError()

  # Clear the records variable to an empty list
  rec = []

  # Open the input file as a text file in UTF-8 encoding and parse all
  # the records
  try:
    with open(fpath, mode='rt',
              encoding='utf-8', errors='strict') as fin:
  
      # We have the input file open -- read line by line
      lbuf = []     # Buffers record lines
      line_num = 0  # Current line number
      rec_line = 1  # Line at start of current record
      for line in fin:
        
        # Update line count
        line_num = line_num + 1
        
        # Trim trailing whitespace and linebreaks, but NOT leading
        # whitespace, which is significant in case of line continuations
        line = line.rstrip(' \t\n')
        
        # Filter out blank lines that are empty or contain only spaces,
        # tabs, and line breaks
        if len(line) < 1:
          continue
        
        # If this line is %% then handle end of record and continue to
        # next record
        if line == '%%':
          # If the record line of this record is 1, then just clear the
          # line buffer, update the record line, and continue to next
          # line without any further processing so that we skip the
          # special first record
          if rec_line <= 1:
            lbuf = []
            rec_line = line_num + 1
            continue
          
          # If we got here, we're not in the special case of the first
          # record, so we want to process the raw record
          raw_record(rec_line, lbuf)
          
          # Clear the line buffer and update the record line
          lbuf = []
          rec_line = line_num + 1
          
          # Continue on to next line
          continue
        
        # If the first character of this line is a tab or a space, then
        # we have a continuation line, so process that and continue to
        # next line
        fchar = line[0]
        if (fchar == ' ') or (fchar == '\t'):
          # Continuation line, so this must not be first line of record
          if len(lbuf) < 1:
            raise BadContinueLine(line_num)
          
          # Drop leading whitespace and replace with a single leading
          # space
          line = ' ' + line.lstrip(' \t')
          
          # Add this line to the end of the last line in the record line
          # buffer
          lbuf[-1] = lbuf[-1] + line
          
          # Continue on to next line
          continue
        
        # If we got here, we have a regular record line, so just add
        # that to the line buffer
        lbuf.append(line)
    
      # If after the loop will still have something in the record
      # buffer, flush this last record
      if len(lbuf) > 0:
        raw_record(rec_line, lbuf)
        lbuf = []
    
    # All records have been read in and *individually* verified; now we
    # need to build indices of each record type so we can begin
    # validating table consistency across all records
    index_language = dict()
    index_extlang = dict()
    index_script = dict()
    index_region = dict()
    index_variant = dict()
    index_grandfathered = dict()
    index_redundant = dict()
    
    #  Build the indices
    rlen = len(rec)
    for i in range(0, rlen):
      r = rec[i][1]
      vt = r['type']
      if vt == 'language':
        vn = r['subtag']
        if vn in index_language:
          raise RedefinitionError(rec[i][0])
        index_language[vn] = i
        
      elif vt == 'extlang':
        vn = r['subtag']
        if vn in index_extlang:
          raise RedefinitionError(rec[i][0])
        index_extlang[vn] = i
        
      elif vt == 'script':
        vn = r['subtag']
        if vn in index_script:
          raise RedefinitionError(rec[i][0])
        index_script[vn] = i
        
      elif vt == 'region':
        vn = r['subtag']
        if vn in index_region:
          raise RedefinitionError(rec[i][0])
        index_region[vn] = i
        
      elif vt == 'variant':
        vn = r['subtag']
        if vn in index_variant:
          raise RedefinitionError(rec[i][0])
        index_variant[vn] = i
      
      elif vt == 'grandfathered':
        vn = r['tag']
        if vn in index_grandfathered:
          raise RedefinitionError(rec[i][0])
        index_grandfathered[vn] = i
        
      elif vt == 'redundant':
        vn = r['tag']
        if vn in index_redundant:
          raise RedefinitionError(rec[i][0])
        index_redundant[vn] = i
        
      else:
        raise LogicError()
  
    # Now we can verify the foreign keys in each record to finish
    # verifying the structural integrity of the data
    for rf in rec:
      r = rf[1]
      rt = r['type']
      
      # If record has a suppress-script field, make sure that it
      # references an existing script
      if 'suppress-script' in r:
        if r['suppress-script'] not in index_script:
          raise MissingKeyError(rf[0])
  
      # If we have a prefix in an extlang record, make sure it
      # references a language
      if ('prefix' in r) and (rt == 'extlang'):
        for p in r['prefix']:
          if p not in index_language:
            raise MissingKeyError(rf[0])
      
      # If we have prefixes in a variant record, check their references
      if ('prefix' in r) and (rt == 'variant'):
        for p in r['prefix']:
          # Split prefix into components around the hyphens
          pa = p.split('-')
          
          # Make sure first component is a defined language
          if pa[0] not in index_language:
            raise MissingKeyError(rf[0])
          
          # Start at next component (if there is one) and proceed until
          # all components checked
          i = 1
          pt = 'extlang'
          while i < len(pa):
            if pt == 'extlang':
              # Check any extlang tags
              if (len(pa[i]) == 3) and is_lower_letter(pa[i][0]):
                if pa[i] in index_extlang:
                  i = i + 1
                  pt = 'script'
                else:
                  raise MissingKeyError(rf[0])
              else:
                pt = 'script'
              
            elif pt == 'script':
              # Check any script tags
              if (len(pa[i]) == 4) and is_upper_letter(pa[i][0]):
                if pa[i] in index_script:
                  i = i + 1
                  pt = 'region'
                else:
                  raise MissingKeyError(rf[0])
              else:
                pt = 'region'
              
            elif pt == 'region':
              # Check any region tags
              if (len(pa[i]) == 2) or \
                  ((len(pa[i]) == 3) and is_digit(pa[i][0])):
                if pa[i] in index_region:
                  i = i + 1
                  pt = 'variant'
                else:
                  raise MissingKeyError(rf[0])
              else:
                pt = 'variant'
              
            elif pt == 'variant':
              # Check any variant tags
              if ((len(pa[i]) == 4) and is_digit(pa[i][0])) or \
                  (len(pa[i]) > 4):
                if pa[i] in index_variant:
                  i = i + 1
                else:
                  raise MissingKeyError(rf[0])
              else:
                raise MissingKeyError(rf[0])
              
            else:
              raise LogicError()
  
      # If we have a preferred-value mapping, check that it references
      # a record, and that the referenced record does not itself have a
      # preferred value
      if 'preferred-value' in r:
        pv = r['preferred-value']
        if rt == 'language':
          # Language must refer to an existing language
          if pv not in index_language:
            raise MissingKeyError(rf[0])
          
          # Referenced language must not have preferred value
          if 'preferred-value' in rec[index_language[pv]][1]:
            raise RecursiveMappingError(rf[0])
          
        elif rt == 'script':
          # Script must refer to an existing script
          if pv not in index_script:
            raise MissingKeyError(rf[0])
          
          # Referenced script must not have preferred value
          if 'preferred-value' in rec[index_script[pv]][1]:
            raise RecursiveMappingError(rf[0])
          
        elif rt == 'region':
          # Region must refer to an existing region
          if pv not in index_region:
            raise MissingKeyError(rf[0])
            
          # Referenced region must not have preferred value
          if 'preferred-value' in rec[index_region[pv]][1]:
            raise RecursiveMappingError(rf[0])
          
        elif rt == 'variant':
          # Variant must refer to an existing variant
          if pv not in index_variant:
            raise MissingKeyError(rf[0])
            
          # Referenced variant must not have preferred value
          if 'preferred-value' in rec[index_variant[pv]][1]:
            raise RecursiveMappingError(rf[0])
          
        elif rt == 'extlang':
          # extlang must refer to an existing language
          if pv not in index_language:
            raise MissingKeyError(rf[0])
          
          # Referenced language must not have preferred value
          if 'preferred-value' in rec[index_language[pv]][1]:
            raise RecursiveMappingError(rf[0])
          
        elif rt == 'grandfathered':
          # Grandfathered records must map to language that doesn't have
          # its own preferred mapping; the weird en-GB-oxendict
          # preferred value is an exception
          if pv in index_language:
            if 'preferred-value' in rec[index_language[pv]][1]:
              raise RecursiveMappingError(rf[0])
          
          elif pv == 'en-GB-oxendict':
            if 'en' not in index_language:
              raise MissingKeyError(rf[0])
            if 'GB' not in index_region:
              raise MissingKeyError(rf[0])
            if 'oxendict' not in index_variant:
              raise MissingKeyError(rf[0])
            
            if ('preferred-value' in rec[index_language['en']][1]) or \
                ('preferred-value' in rec[index_region['GB']][1]) or \
                ('preferred-value' in \
                    rec[index_variant['oxendict']][1]):
              raise RecursiveMappingError(rf[0])
          
          else:
            raise MissingKeyError(rf[0])
          
        elif rt == 'redundant':
          # Redundant mappings must refer to existing language that is
          # not itself remapped, except for cmn-Hans and cmn-Hant
          if pv in index_language:
            if 'preferred-value' in rec[index_language[pv]][1]:
              raise RecursiveMappingError(rf[0])
            
          elif pv == 'cmn-Hans':
            if 'cmn' not in index_language:
              raise MissingKeyError(rf[0])
            if 'Hans' not in index_script:
              raise MissingKeyError(rf[0])
            
            if ('preferred-value' in rec[index_language['cmn']][1]) or \
                ('preferred-value' in rec[index_script['Hans']][1]):
              raise RecursiveMappingError(rf[0])
            
          elif pv == 'cmn-Hant':
            if 'cmn' not in index_language:
              raise MissingKeyError(rf[0])
            if 'Hant' not in index_script:
              raise MissingKeyError(rf[0])
            
            if ('preferred-value' in rec[index_language['cmn']][1]) or \
                ('preferred-value' in rec[index_script['Hant']][1]):
              raise RecursiveMappingError(rf[0])
            
          else:
            raise MissingKeyError(rf[0])
          
        else:
          raise LogicError()
  
      # If record is for an extlang, make sure it has a preferred-value
      # and that the preferred-value (language) is equal to the extlang
      # subtag
      if rt == 'extlang':
        if 'preferred-value' not in r:
          raise BadExtlangRemap(rf[0])
        if r['preferred-value'] != r['subtag']:
          raise BadExtlangRemap(rf[0])
  
  except FileNotFoundError:
    rec = None
    raise NoDataFileError(fpath)
  
  except ValueError:
    rec = None
    raise BadDataFile()
    
  except SubtagError as se:
    rec = None
    raise se
  
  except Exception as exc:
    rec = None
    raise SubtagError() from exc
