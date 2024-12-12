import re
import csv
import json
from bs4 import BeautifulSoup

# Fayl yolları
access_log_path = "C:\\Users\\Admin\\Desktop\\lab2\\access_log.txt"
thread_feed_path = "C:\\Users\\Admin\\Desktop\\lab2\\threat_feed.html"
url_status_report_path = "url_status_report.txt"
malware_candidates_path = "malware_candidates.csv"
alert_json_path = "alert.json"
summary_report_json_path = "summary_report.json"

# 1. Log faylından məlumat oxuma və URL/status çıxarma
error_404_count = {}
url_status = []
blacklisted_domains = []

# Log faylından məlumatı oxuyub 404 səhvləri toplamaq
with open(access_log_path, "r") as log_file:
    for log in log_file:
        match = re.search(r'"[A-Z]+ (http[s]?://[^\s]+) HTTP/[\d.]+" (\d+)', log)
        if match:
            url, status = match.group(1), int(match.group(2))
            url_status.append((url, status))
            if status == 404:
                error_404_count[url] = error_404_count.get(url, 0) + 1

# 2. HTML faylından qara siyahı domenlərini oxuma
with open(thread_feed_path, "r") as html_file:
    soup = BeautifulSoup(html_file.read(), "html.parser")
    blacklisted_domains = [li.get_text() for li in soup.find_all("li")]

# 3. URL-ləri qara siyahı ilə müqayisə et və nəticələri JSON faylında saxla
alerts = [
    {"url": url, "status": status, "occurrences": error_404_count.get(url, 1)}
    for url, status in url_status
    if any(domain in url for domain in blacklisted_domains)
]

# 4. Nəticələri fayllara yazma
# URL-ləri və status kodlarını yaz
with open(url_status_report_path, "w") as report_file:
    report_file.writelines(f"{url} {status}\n" for url, status in url_status)

# 404 kodlu URL-ləri CSV faylında saxla
with open(malware_candidates_path, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["URL", "404 Count"])
    csv_writer.writerows(error_404_count.items())

# Qara siyahıya alınmış URL-ləri JSON faylında saxla
with open(alert_json_path, "w") as json_file:
    json.dump(alerts, json_file, indent=4)

# Statistikaları JSON faylında saxla
summary = {
    "total_urls": len(url_status),
    "total_404s": sum(error_404_count.values()),
    "blacklisted_matches": len(alerts)
}

with open(summary_report_json_path, "w") as summary_file:
    json.dump(summary, summary_file, indent=4)

print("Proses tamamlandı!")