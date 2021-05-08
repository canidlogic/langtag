# Language tag utilities

This directory contains the utility scripts for working with language tag databases.

## Important notes

(1) Some of these scripts rely on the `langtag.py` module, which is in the root directory of this project.  You must either copy that file into this directory or somehow make it available to import for scripts in this directory or some of these scripts won't work!

(2)  You will need to download copies of the data tables in order to use these utilities.  The utilities will ask for the paths to these data tables as program arguments.  The needed data tables, the parsing modules that use them, and links to where you can get them are shown in the table below:

Data table | Module | Source link
-----------|--------|------------
IANA Language Subtag Registry | `subtag.py` | https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
ISO-639-2 | `iso2.py` | https://www.loc.gov/standards/iso639-2/
ISO-639-3 main code table | `iso3.py` | https://iso639-3.sil.org/
ISO-639-3 language names index | `iso3.py` | https://iso639-3.sil.org/
ISO-639-3 macrolanguage table | `iso3.py` | https://iso639-3.sil.org/
ISO-639-3 deprecated/retired codes table | `iso3.py` | https://iso639-3.sil.org/
ISO-639-5 | `iso5.py` | https://www.loc.gov/standards/iso639-5/

(3) When given a choice, always use the UTF-8 versions of the data tables.  The utilities will **not** work if you provide the Latin-1 or ISO-8859-1 version of any of the data tables.

## Parsing modules

The following modules in this directory are for parsing the data tables.  You do not need to use them directly, unless you are writing your own custom utilities to work with the language tag databases:

Parsing module | Description
---------------|------------
`fulldb.py` | Loads all parsing modules and performs consistency checks
`iso2.py` | Parses the ISO-639-2 data table
`iso3.py` | Parses the ISO-639-3 data tables
`iso5.py` | Parses the ISO-639-5 data table
`subtag.py` | Parses the IANA language subtag registry

See the documentation within those scripts for further information.  Also see the Langtag specification in the `doc` directory of this project for a more in-depth explanation.

## Utility programs

The following scripts are utility programs that use the parsing modules to parse the data files and generate useful data.  Remember that some of these import the `langtag.py` module from the root directory, so you must somehow make that available for import here, either by copying that script into this directory or some other means.  Here are the utility programs:

Utility program | Description
----------------|------------
`dropscript.py` | Generates the script suppression dictionary
`elaremap.py` | Generates the elaboration remapping dictionary
`langremap.py` | Generates the language subtag remapping dictionary
`langsimp.py` | Generates the language subtag simplification dictionary
`macrolang.py` | Generates the macrolanguage dictionary
`namelang.py` | Generates the language name dictionary
`subtag_list.py` | Displays sets of records from the subtag registry
`tagremap.py` | Generates the tag remapping dictionary

See the documentation within those scripts for further information.  Also see the Langtag specification in the `doc` directory of this project for a more in-depth explanation.
