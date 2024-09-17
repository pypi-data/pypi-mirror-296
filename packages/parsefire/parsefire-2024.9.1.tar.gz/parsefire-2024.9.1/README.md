# `parsefire`

## Overview

The `parsefire` package is a python package for consistent data mining from unstructured text documents.  
It provides tools for parsing text files based on specified lexicons. It supports parsing simple fields, nested sections, 
tables, and custom regex patterns.  The parsing specifications are defined in a lexicon, which is a dictionary of 
containing fields.  Fields are specified using a simple syntax that includes the field name, type and optionally field
size and even custom regular expressions.  The package the uses the specification to generate regular expressions
for parsing the text and converting the parsed data into a dictionary of the specified type.

Specifications can be written into YAML files and loaded for parsing by the `TextParser` class.

For example, the following lexicon specifies two fields, `age` and `name`, which are parsed from the text `Age: 25\nName: John Doe`.
As fields in a YAML file:

```yaml
fields:
  - "Age: <int:age>"
  - "Name: <str:name>"
```

As a python dictionary:

```python
specs = {
    'fields': [
        "Age: <int:age>",
        "Name: <str:name>"
    ]
}
```


## Modules

### `parsefire.parser`

#### Functions

- **`parse_file(data_file: Union[str, Path], specs: dict, size: int = -1) -> dict`**

  Parses a text file and returns a dictionary of matched key-value pairs.

  **Parameters:**
  - `data_file`: The file path or name.
  - `specs`: A nested dictionary of specifications.
  - `size`: Maximum size of the file to parse in bytes (default is -1, which means no limit).

  **Returns:**
  - A nested dictionary of key-value pairs.

- **`parse_text(specs: dict, text: str) -> dict`**

  Parses the given text using the provided specifications.

  **Parameters:**
  - `specs`: A dictionary of specifications.
  - `text`: The text to parse.

  **Returns:**
  - A dictionary of parsed key-value pairs.

#### Classes

- **`TextParser`**

  A class for parsing text files using a lexicon.

  **Class Methods:**
  - `parse(cls, filename: str, silent=False) -> dict`
    - Parses the provided file and returns a dictionary.
    - **Parameters:**
      - `filename`: The text file to parse.
      - `silent`: If `True`, returns an empty dictionary instead of throwing exceptions.
    - **Returns:**
      - A dictionary of parsed key-value pairs.

  - `parse_text(cls, text: str, lexicon: dict) -> Any`
    - Parses the given text using the lexicon dictionary.
    - **Parameters:**
      - `text`: The text to parse.
      - `lexicon`: The lexicon specification dictionary.
    - **Returns:**
      - Parsed data.

  - `get_lexicon(cls, filename) -> dict`
    - Returns the lexicon specified for a given file.
    - **Parameters:**
      - `filename`: The name of the file.
    - **Returns:**
      - A dictionary of lexicon specifications.

- **`MissingLexicon`**

  Exception raised when a lexicon is missing.

- **`FilesMissing`**

  Exception raised when files are missing.

## Usage Examples

### Parsing Simple Fields

```python
from parsefire.parser import parse_text

specs = {
    'fields': [
        "Age: <int:age>",
        "Name: <str:name>"
    ]
}
text = "Age: 25\nName: John Doe"
result = parse_text(specs, text)
print(result)  # Output: {'age': 25, 'name': 'John Doe'}
```

### Parsing Nested Sections

```python
from parsefire.parser import parse_text

specs = {
    'sections': {
        'person': {
            'fields': [
                "Age: <int:age>",
                "Name: <str:name>"
            ]
        }
    }
}
text = "Age: 25\nName: John Doe"
result = parse_text(specs, text)
print(result)  # Output: {'person': {'age': 25, 'name': 'John Doe'}}
```

### Parsing Tables

```python
from parsefire.parser import parse_text

specs = {
    'table': "Row: <int:id> <str:name>"
}
text = "Row: 1 John\nRow: 2 Jane"
result = parse_text(specs, text)
print(result)  # Output: [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
```

### Parsing with Custom Regex

```python
from parsefire.parser import parse_text

specs = {
    'fields': [
        r"Code: <str:code:([A-Z]{3}-\d{3})>"
    ]
}
text = "Code: ABC-123"
result = parse_text(specs, text)
print(result)  # Output: {'code': 'ABC-123'}
```

### Parsing with Domains
A domain is a section of text that is matched by a regular expression. The domain is used to extract the text that will be parsed.

```python
from parsefire.parser import parse_text

specs = {
    'domain': r"Inside:(.*?)(?=Outside|$)",
    'fields': [
        "Age: <int:age>",
        "Name: <str:name>"
    ]
}
text = (
    "Inside:\n"
    "Age: 25\n"
    "Name: John Doe\n"
    "Outside:\n"
    "Age: 30\n"
    "Name: Jane Doe"
)
result = parse_text(specs, text)
print(result)  # Output: {'age': 25, 'name': 'John Doe'}
```

### A more complex example

Here is an example of how to parse a text file with multiple sections and tables.

```yaml
root:
  sections:
    quality:
      domain: "REFINEMENT OF DIFFRACTION PARAMETERS USING ALL IMAGES(.+?)THE DATA COLLECTION STATISTICS REPORTED BELOW ASSUMES"
      fields:
        - " STANDARD DEVIATION OF SPOT    POSITION (PIXELS)  <float:pixel_error>"
        - " STANDARD DEVIATION OF SPINDLE POSITION (DEGREES) <float:angle_error>"
        - " CRYSTAL MOSAICITY (DEGREES) <float:mosaicity>"

    statistics:
      domain: "STATISTICS OF SAVED DATA SET .*? WITH SIGNAL/NOISE >= -3.0(.+?)NUMBER OF REFLECTIONS IN SELECTED"
      table: " <float:shell> <int:observed> <int:unique> <int:possible> <float:completeness>% <float:r_obs>% <float:r_exp>% <int:compared> <float:i_sigma> <float:r_meas>% <float:cc_half><char:signif> <int:cor_ano><char:asignif> <float:sig_ano> <int:Nano>"

    summary:
      domain: "STATISTICS OF SAVED DATA SET .*? WITH SIGNAL/NOISE >= -3.0(.+?)WILSON STATISTICS OF DATA SET"
      fields:
        - "    total <int:observed> <int:unique> <int:possible> <float:completeness>% <float:r_obs>% <float:r_exp>% <int:compared> <float:i_sigma> <float:r_meas>% <float:cc_half><char:signif> <int:cor_ano><char:asignif> <float:sig_ano> <int:Nano>"
        - " NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES <int:reflections>"
        - " NUMBER OF SYSTEMATIC ABSENT REFLECTIONS <int:absent>"
        - " NUMBER OF REJECTED MISFITS <int:misfits>"
```

And here is a snippet of the corresponding text file:

```
 ******************************************************************************
      MEAN DISCREPANCIES BETWEEN OBSERVED AND CALCULATED SPOT LOCATIONS
 ******************************************************************************

 The discrepancies in X- and Y-coordinates of the spots are depicted in the
 two images DX-CORRECTIONS.cbf and DY-CORRECTIONS.cbf for inspection with
 the XDS-Viewer.



 ******************************************************************************
  REFINEMENT OF DIFFRACTION PARAMETERS USING ALL IMAGES
 ******************************************************************************


 REFINED VALUES OF DIFFRACTION PARAMETERS DERIVED FROM     50627 INDEXED SPOTS
 REFINED PARAMETERS:   POSITION BEAM AXIS ORIENTATION CELL
 STANDARD DEVIATION OF SPOT    POSITION (PIXELS)     1.99
 STANDARD DEVIATION OF SPINDLE POSITION (DEGREES)    0.43
 SPACE GROUP NUMBER      1
 UNIT CELL PARAMETERS     57.578    58.086   148.620  89.360  89.832  89.615
 E.S.D. OF CELL PARAMETERS  1.3E-01 1.6E-01 3.5E-01 1.7E-01 6.1E-02 9.4E-02
 REC. CELL PARAMETERS   0.017368  0.017217  0.006729  90.639  90.164  90.383
 COORDINATES OF UNIT CELL A-AXIS   -12.315    34.160    44.684
 COORDINATES OF UNIT CELL B-AXIS   -37.590   -39.382    20.249
 COORDINATES OF UNIT CELL C-AXIS   107.768   -64.427    79.517
 CRYSTAL MOSAICITY (DEGREES)     0.301
 LAB COORDINATES OF ROTATION AXIS  0.999999  0.001263 -0.000442
 DIRECT BEAM COORDINATES (REC. ANGSTROEM)   0.001820  0.001247  0.806579
 DETECTOR COORDINATES (PIXELS) OF DIRECT BEAM    1279.44   1261.60
 DETECTOR ORIGIN (PIXELS) AT                     1276.19   1259.38
 CRYSTAL TO DETECTOR DISTANCE (mm)       247.52
 LAB COORDINATES OF DETECTOR X-AXIS  1.000000  0.000000  0.000000
 LAB COORDINATES OF DETECTOR Y-AXIS  0.000000  1.000000  0.000000

...
 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     201
 ******************************************************************************


          COMPLETENESS AND QUALITY OF DATA SET
          ------------------------------------

 R-FACTOR
 observed = (SUM(ABS(I(h,i)-I(h))))/(SUM(I(h,i)))
 expected = expected R-FACTOR derived from Sigma(I)

 COMPARED = number of reflections used for calculating R-FACTOR
 I/SIGMA  = mean of intensity/Sigma(I) of unique reflections
            (after merging symmetry-related observations)
 Sigma(I) = standard deviation of reflection intensity I
            estimated from sample statistics

 R-meas   = redundancy independent R-factor (intensities)
            Diederichs & Karplus (1997), Nature Struct. Biol. 4, 269-275.

 CC(1/2)  = percentage of correlation between intensities from
            random half-datasets. Correlation significant at
            the 0.1% level is marked by an asterisk.
            Karplus & Diederichs (2012), Science 336, 1030-33
 Anomal   = percentage of correlation between random half-sets
  Corr      of anomalous intensity differences. Correlation
            significant at the 0.1% level is marked.
 SigAno   = mean anomalous difference in units of its estimated
            standard deviation (|F(+)-F(-)|/Sigma). F(+), F(-)
            are structure factor estimates obtained from the
            merged intensity observations in each parity class.
  Nano    = Number of unique reflections used to calculate
            Anomal_Corr & SigAno. At least two observations
            for each (+ and -) parity are required.


 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     4.62        4309    3073     10593       29.0%     463.8%   1726.2%     2472    0.14    655.9%     2.1      0    0.000       0
     3.27        7484    6163     19118       32.2%     126.4%    169.2%     2642    0.29    178.8%    -9.3      0    0.000       0
     2.67        9554    8499     24772       34.3%     120.0%    159.2%     2110    0.29    169.7%    -0.5      0    0.000       0
     2.32       11329   10542     29236       36.1%     126.2%    180.5%     1574    0.23    178.5%    -7.2      0    0.000       0
     2.07       12693   12240     33223       36.8%     125.2%    169.5%      906    0.21    177.1%    -9.3      0    0.000       0
     1.89       13718   13520     36735       36.8%     159.8%    393.6%      396    0.16    226.0%    -6.2      0    0.000       0
     1.75       15033   14992     39873       37.6%     216.9%    846.8%       82    0.14    306.8%     5.2      0    0.000       0
     1.64        9949    9947     42876       23.2%      92.6%     93.6%        4    0.05    130.9%     0.0      0    0.000       0
     1.55        3810    3810     45658        8.3%     -99.9%    -99.9%        0    0.00    -99.9%     0.0      0    0.000       0
    total       87879   82786    282084       29.3%     148.8%    283.9%    10186    0.17    210.4%    -0.2      0    0.000       0


 NUMBER OF REFLECTIONS IN SELECTED SUBSET OF IMAGES     87879
 NUMBER OF REJECTED MISFITS                                 0
 NUMBER OF SYSTEMATIC ABSENT REFLECTIONS                    0
 NUMBER OF ACCEPTED OBSERVATIONS                        87879
 NUMBER OF UNIQUE ACCEPTED REFLECTIONS                  82786



 ******************************************************************************
  SUMMARY OF DATA SET STATISTICS FOR IMAGE   DATA_RANGE=       1     401
 ******************************************************************************

```
