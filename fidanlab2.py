import os
import re
import csv
import json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

# Çıxış faylları üçün yollar
OUTPUT_FOLDER = "output_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
URL_STATUS_REPORT_FILE = os.path.join(OUTPUT_FOLDER, "url_status_report.txt")
MALWARE_CANDIDATES_FILE = os.path.join(OUTPUT_FOLDER, "malware_candidates.csv")
ALERT_JSON_FILE = os.path.join(OUTPUT_FOLDER, "alert.json")
SUMMARY_REPORT_FILE = os.path.join(OUTPUT_FOLDER, "summary_report.json")

# Log analiz və məlumat yazımı
log_file = 'access_log.txt'
blacklist_url = 'http://127.0.0.1:8000'

def parse_access_log(file_path):
    url_status = []
    with open(file_path, 'r') as file:
        for line in tqdm(file, desc="Log analiz edilir"):
            match = re.search(r'\S+ \S+ \S+ \[.*?\] \".*? (\S+) .*?\" (\d{3})', line)
            if match:
                url_status.append((match.group(1), match.group(2)))
    return url_status

def count_and_write(url_status):
    counts = defaultdict(int)
    with open(URL_STATUS_REPORT_FILE, 'w') as file:
        for url, status in tqdm(url_status, desc="URL-lər fayla yazılır"):
            file.write(f"{url} {status}\n")
            if status == '404':
                counts[url] += 1
    with open(MALWARE_CANDIDATES_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', '404_count'])
        writer.writerows(counts.items())
    return counts

def scrape_blacklist(url):
    driver = webdriver.Chrome()
    driver.get(url)
    blacklist = [element.text for element in driver.find_elements(By.XPATH, "//li")]
    driver.quit()
    return blacklist

def compare_and_write(url_status, blacklist):
    matches = [(url, status) for url, status in url_status if re.sub(r'https?://(www\.)?', '', url).split('/')[0] in blacklist]
    with open(ALERT_JSON_FILE, 'w') as json_file:
        json.dump([{'url': url, 'status': status} for url, status in matches], json_file, indent=4)
    return matches

def write_summary(url_status, counts):
    summary = {
        'total_urls': len(url_status),
        'total_404': sum(counts.values()),
        'unique_404_urls': len(counts)
    }
    with open(SUMMARY_REPORT_FILE, 'w') as json_file:
        json.dump(summary, json_file, indent=4)

def main():
    url_status = parse_access_log(log_file)
    counts = count_and_write(url_status)
    blacklist = scrape_blacklist(blacklist_url)
    compare_and_write(url_status, blacklist)
    write_summary(url_status, counts)
    print("✅ Analiz tamamlandı!")

if __name__ == "__main__":
    main()
