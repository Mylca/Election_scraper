# Election Scraper

This script is used to download election data from [Election results 2017 CZ](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) the column "Výběr obce" and save it to a CSV file.

## Requirements

To run the script correctly, you need Python 3.6+ and the following libraries:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/Mylca/Election_scraper.git
   cd Election_scraper
   ```
2. Install the required libraries (if you haven't already):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line with the following arguments:

```bash
python scraper.py 'URL' 'output_file.csv'
```

### Example:
```bash
python scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "praha.csv"
```

If incorrect arguments are provided, the program will display an error message and terminate.

## Output

The script generates a CSV file containing election data, where each row corresponds to a municipality.

## Code Structure

- `scraper.py` – main script
- `requirements.txt` – list of required libraries



