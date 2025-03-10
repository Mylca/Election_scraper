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

#### Expected console output:

```
Collected municipalities: 57
Generated URLs: 57
Downloading election data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 57/57 [01:58<00:00,  2.09s/url]
Saved as: praha.csv
Requests to the server was: 59
```

If incorrect arguments are provided, the program will display an error message and terminate.

## Output

The script generates a CSV file containing election data, where each row corresponds to a municipality.

### Example:

[csv_image_example](csv_example.png)

## Code Structure

- `scraper.py` – main script
- `requirements.txt` – list of required libraries



