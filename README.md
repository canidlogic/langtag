# Langtag

Python-3 utilities for working with language tags.

The standalone `langtag.py` script in this root directory contains utility functions for parsing, normalizing, and validating standard language tags that follow RFC-5646 (BCP 47).  However, the script does *not* include a function for mapping language tags to a user-friendly name, because the name dictionary required for that is rather large.

The `names.json` file in this root directory is a generated JSON dictionary that maps normalized language codes to an array of one or two strings.  One-string arrays just store the name of the language.  Two-string arrays add an "inverted name" as the second element.  For example, "Swiss German" has an inverted name of "German, Swiss".  If you need to map language tags to language names, you can use this JSON file to fill in a database table.

The `langtag.py` script has embedded data tables and the `names.json` file is auto-generated.  The scripts for generating this data, based on official data tables, are in the `util` directory of this project.  See the README in that directory for further information.

See the Langtag specification in the `doc` directory for a more complete discussion about this project.
