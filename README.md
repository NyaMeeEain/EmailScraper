# Emailscraper


Email scraper is an OSINT Python tool to extract email addresses for a given domain. I use a more realistic approach to collect targeted email addresses for phishing as we want to avoid guessing and constructing email since we need a valid email address associated with the domain. This tool uses two approaches to collect email addresses from Google and hunter.io. Collected results will be printed and save as CSV format.


The gathered email will be checked with haveibeenpwned, so you need to have haveibeenpwned' API to check whether the email is compromised or not; if you don't have that API, you can skip it.

### How to Use
I use a more realistic approach to Hunter's email address regarding phishing. We don't want to guess and construct email since we need a valid email address associated with the domain. 
Run the Python script and type your target domain and Hunter API key. If you don’t have Hunter API you can skip.Please look at the following screenshot; for demonstration purposes, I used uber.com for educational purposes.
![image text](https://github.com/NyaMeeEain/Emailscraper/blob/main/Simple.PNG)

### References:
I would like to credit the following authors and reference sources to achieve this project. I have gained knowledge and ideas from these sources to develop my code snippets and ideas.

https://github.com/serpapi/clauneck

https://github.com/oxylabs/amazon-scraper

https://github.com/nayeemnazmul/MailSpotter

https://github.com/ayushagarwalk/Email-Scraping
