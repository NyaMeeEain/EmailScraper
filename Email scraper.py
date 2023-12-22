#!/usr/bin/env python3

"""
Author: NyaMeeEain
Version: 0.1
"""

import sys
import re
import requests
import csv
import pandas as pd
import hashlib

def print_banner():
    banner = """
    Author: NyaMeeEain
    Version: 0.1
    
    """
    print(banner)

def strip_tags(text):
    finished = False
    while not finished:
        finished = True
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start + stop + 1:]
                finished = False
    return text

def get_emails_from_google(domain_name, is_groups=True):
    emails_dict = {}
    page_counter = 0
    search_type = "groups" if is_groups else "web"

    try:
        while page_counter < 100:  
            results_url = f'http://groups.google.com/groups?q={domain_name}&hl=en&lr=&ie=UTF-8&start={page_counter}&sa=N' if is_groups else f'http://www.google.com/search?q=%40{domain_name}&hl=en&lr=&ie=UTF-8&start={page_counter}&sa=N'
            
            response = requests.get(results_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'})

            text = response.text
            emails = re.findall('([\w\.\-]+@' + domain_name + ')', strip_tags(text))

            for email in emails:
                emails_dict[email] = 1

            page_counter += 10

    except requests.RequestException:
        print(f"Cannot connect to Google {search_type}. Please check your internet connection or try again later.")
        sys.exit(1)

    return emails_dict.keys()

def get_emails_from_hunter(domain_name, hunter_api_key):
    hunter_url = f'https://api.hunter.io/v2/domain-search?domain={domain_name}&api_key={hunter_api_key}'
    try:
        response = requests.get(hunter_url)
        response.raise_for_status() 
        data = response.json()
        hunter_emails = [email['value'] for email in data.get('data', {}).get('emails', [])]
        return hunter_emails
    except requests.RequestException:
        print(f" Please check your internet connection or Hunter API.")
        sys.exit(1)

def extract_name_from_email(email):
    parts = email.split('@')[0].split('.')
    first_name = parts[0].capitalize() if parts else ''
    last_name = parts[-1].capitalize() if len(parts) > 1 else ''
    return first_name, last_name

def check_haveibeenpwned(email):
    sha1_hash = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    pwned_url = f'https://api.pwnedpasswords.com/range/{prefix}'
    try:
        response = requests.get(pwned_url)
        response.raise_for_status()  
    except requests.RequestException:
        print(f"Please check your internet connection or Pwned API")
        sys.exit(1)
    
    return suffix in response.text

if __name__ == "__main__":
    print_banner()

    target_domain = input("Enter the target domain: ")
    hunter_api_key = input("Enter your Hunter.io API key: ")

    google_emails = get_emails_from_google(target_domain, is_groups=True)
    hunter_emails = get_emails_from_hunter(target_domain, hunter_api_key)

    unique_emails = set(google_emails).union(set(hunter_emails))
    
    csv_filename = 'output.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['First Name', 'Last Name', 'Email', 'Compromised']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for email in unique_emails:
            first_name, last_name = extract_name_from_email(email)
            compromised = check_haveibeenpwned(email)
            writer.writerow({'First Name': first_name, 'Last Name': last_name, 'Email': email, 'Compromised': compromised})

    print(f"Output saved to {csv_filename}")

    Data = pd.read_csv(csv_filename)
    print("\nCollected Emails :")
    print(Data)
