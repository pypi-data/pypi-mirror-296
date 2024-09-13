# Indala-Decoder

A Python library for decoding 32-bit Indala26 codes into facility code and card numbers, and vice versa
* [Installation](#installation)
    * [Via pip](#via-pip)
    * [From source](#from-source)
 * [Usage](#usage)
   * [As a library](#as-a-library)
   * [From commandline](#from-commandline)
 
## Installation

### Via pip
```bash
pip install indala-decoder
```

### From source
```bash
git clone https://github.com/muzak23/indala-decoder.git
```

## Usage

### As a library
```python
import indala_decoder as id

# Decode a 32-bit Indala26 code from hex
print(id.bin_to_summary(id.hex_to_bin('12:34:56:78')))

# FC: 35
# Card: 11414
# Checksum: -
# W26 Parity: -

# Encode a 32-bit Indala26 code from facility code and card number
print(id.summary_to_bin(1234, 5678))

# 01111111000000110100000110110000
```

### From commandline

Work in progress, hex must be in format 1a2b3c4d
```bash
$ py indala_decoder.py
Raw data to summary (r) or summary to raw data (s)?
r
Enter raw data (binary or hex):
12345678
FC: 35
Card: 11414
Checksum: -
W26 Parity: -

```