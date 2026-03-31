import requests
from bs4 import BeautifulSoup
import csv
import os
import subprocess

# Settings
URL = "https://distrowatch.com/"
CSV_FILE = "distro_main_releases.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def get_existing_links(filename):
    """Reads the CSV to find links we already have."""
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return {row['Link'] for row in reader}

def scrape_main_feed():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headlines = soup.find_all('td', class_='NewsHeadline')
        dates = soup.find_all('td', class_='NewsDate')
        
        new_entries = []
        existing_links = get_existing_links(CSV_FILE)

        for headline, date_tag in zip(headlines, dates):
            link_tag = headline.find('a')
            if link_tag:
                # Get the raw text
                raw_title = link_tag.text.strip()
                
                # Strip the specific prefix. 
                # Note: DistroWatch often uses a non-breaking space (\xa0)
                title = raw_title.replace("Distribution Release: ", "").replace("Distribution Release:\xa0", "").strip()
                
                link = "https://distrowatch.com/" + link_tag['href']
                release_date = date_tag.text.strip()

                if link not in existing_links:
                    new_entries.append({
                        "Release Date": release_date,
                        "Distro Release": title,
                        "Link": link
                    })

        return new_entries

    except Exception as e:
        print(f"Error: {e}")
        return []


def send_notification(distro_name):
    """Triggers a desktop popup alert."""
    try:
        subprocess.run([
            "notify-send",
            "New Distro Release Found!",
            f"Alert: {distro_name} is now available on DistroWatch."
        ])
    except Exception as e:
        print(f"Notification error: {e}")

def check_and_alert(new_entries):
    """Checks new releases for specific keywords and alerts the user."""
    # List of distros you want to watch for
    watch_list = ["mx linux", "debian"]

    for entry in new_entries:
        release_name = entry["Distro Release"].lower()
        if any(distro in release_name for distro in watch_list):
            print(f"MATCH FOUND: {entry['Distro Release']}")
            send_notification(entry["Distro Release"])

# Update your main block to call the alert check
if __name__ == "__main__":
    updates = scrape_main_feed()
    if updates:
        # 1. Check for MX Linux or Debian in the new updates
        check_and_alert(updates)

        # 2. Save data as usual
        save_new_data(updates[::-1])
    else:
        print("No new releases found today.")

