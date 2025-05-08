"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

autor: Milan Komůrka

email: komurka.milan@email.cz

discord: Milan K.

"""

import argparse
import csv
import random
import sys
import time
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

request_count = 0


def get_arguments():
    # Parses and validates command-line arguments
    parser = argparse.ArgumentParser(description='Election scraper', add_help=False)
    parser.add_argument('url', nargs='?', help='URL address')  # '?' makes it optional
    parser.add_argument('output_file', nargs='?', help='File designation')

    args = parser.parse_args()

    # Check if both arguments are provided
    if not args.url or not args.output_file:
        print('Error: You must specify both the URL and the name of the output file.')
        sys.exit(1)

    return args


def save_to_csv(data, filename):
    print(f'Saved as: {filename}')

    # Verify the data is not empty
    if not data:
        print('No file to save.')
        return None

    # Getting keys (header) from the first record in the data
    keys = data[0].keys() if data else []

    # Saving to csv file
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def random_sleep(min_seconds=1, max_seconds=3):
    # Delay between requests
    wait_time = random.uniform(min_seconds, max_seconds)
    time.sleep(wait_time)


def get_response(url):
    # Server status response with error handling
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'An error occurred: {req_err}')
    return None


def get_html(url):
    # HTML to BS object
    global request_count
    request_count += 1
    html_text = get_response(url)
    return BeautifulSoup(html_text, 'html.parser') if html_text else None


def get_relative_urls(html) -> dict:
    # Create dict with relative urls
    relative_links = {
        a.get_text(): a.get('href')
        for a in html.select('div#outer a')
        if a.get_text() != 'X'
    }
    return relative_links


def get_final_urls(links, base_url) -> list:
    # Save final urls
    final_urls = []
    for href in links.values():
        full_url = urljoin(base_url, href)
        final_urls.append(full_url)
    print(f'Generated URLs: {len(final_urls)}')
    return final_urls


def get_codes_and_municipalities(url) -> list:
    # Code and Municipality from first page
    html = get_html(url)
    if not html:
        return []

    municipalities = []
    rows = html.select('div.topline tr')[2:]

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            municipalities.append({
                'code': cells[0].get_text(strip=True),
                'city': cells[1].get_text(strip=True)
            })
    print(f'Collected municipalities: {len(municipalities)}')
    return municipalities


def get_2_page_data(html) -> dict:
    # Retrieve election data
    result_dict = {
        'registered': html.select_one('td[headers="sa2"]').get_text(strip=True) if html.select_one(
            'td[headers="sa2"]') else None,
        'envelopes': html.select_one('td[headers="sa5"]').get_text(strip=True) if html.select_one(
            'td[headers="sa5"]') else None,
        'valids': html.select_one('td[headers="sa6"]').get_text(strip=True) if html.select_one(
            'td[headers="sa6"]') else None
    }

    # Left table parsing
    result_dict.update({
        row.select_one('td[headers="t1sa1 t1sb2"]').get_text(strip=True): row.select_one(
            'td[headers="t1sa2 t1sb3"]').get_text(strip=True)
        for row in html.select('tr')
        if row.select_one('td[headers="t1sa1 t1sb2"]') and row.select_one('td[headers="t1sa2 t1sb3"]')
    })

    # Right table parsing
    result_dict.update({
        row.select_one('td[headers="t2sa1 t2sb2"]').get_text(strip=True): row.select_one(
            'td[headers="t2sa2 t2sb3"]').get_text(strip=True)
        for row in html.select('tr')
        if row.select_one('td[headers="t2sa1 t2sb2"]') and row.select_one('td[headers="t2sa2 t2sb3"]')
    })
    return result_dict


def election_data(url) -> dict:
    # Scrapes election data and returns it as a dict {code: data}.
    html = get_html(url)
    if not html:
        return {}

    rel_links = get_relative_urls(html)
    fin_links = get_final_urls(rel_links, url)

    all_data = {}
    for link in tqdm(fin_links, desc='Downloading election data', unit='url'):
        html = get_html(link)
        if not html:
            continue
        data = get_2_page_data(html)

        # Extracting the municipality code from a URL
        parsed_url = urlparse(link)
        query_params = parse_qs(parsed_url.query)
        code = query_params.get("xobec", [""])[0]

        if code:
            all_data[code] = data
        random_sleep()
    return all_data


def main():
    args = get_arguments()
    municipalities = get_codes_and_municipalities(args.url)
    data = election_data(args.url)

    # Merge by code
    combined_list = [
        {**m, **data.get(m['code'], {})} for m in municipalities
    ]

    save_to_csv(combined_list, args.output_file)

    print(f'Requests to the server was: {request_count}')


if __name__ == "__main__":
    main()
