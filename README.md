# Distro Watcher

A Python script that monitors [DistroWatch](https://distrowatch.com/) for new Linux distribution releases and sends desktop notifications for your watched distributions.

## Features

- **Web Scraping**: Automatically scrapes DistroWatch for the latest distribution releases
- **Duplicate Detection**: Maintains a CSV file to avoid tracking the same release multiple times
- **Selective Alerts**: Watches for specific Linux distributions (e.g., MX Linux, Debian)
- **Desktop Notifications**: Sends `notify-send` desktop popups when a watched distro is released
- **Data Persistence**: Stores all discovered releases in a CSV file for historical tracking

## Requirements

- Python 3.6+
- `requests` library
- `beautifulsoup4` library
- `notify-send` (usually pre-installed on most Linux distributions)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Cheddabob420/Distro_Watcher.git
cd Distro_Watcher
```

2. Install required Python packages:
```bash
pip install requests beautifulsoup4
```

## Usage

Run the script manually:
```bash
python Distro_Watch.py
```

### Customizing Your Watch List

Edit the `watch_list` variable in the `check_and_alert()` function to monitor different distributions:

```python
watch_list = ["mx linux", "debian", "fedora", "ubuntu"]
```

## How It Works

1. **Scraping**: Fetches the latest news from DistroWatch's main page
2. **Deduplication**: Checks existing `distro_main_releases.csv` to skip previously recorded releases
3. **Matching**: Compares new releases against your watch list
4. **Notifications**: Sends a desktop notification if a watched distribution is found
5. **Storage**: Saves new releases to CSV for future reference

## Automation

To run this script automatically on a schedule, use `cron`:

```bash
# Edit your crontab
crontab -e

# Run every hour
0 * * * * /usr/bin/python3 /path/to/Distro_Watch.py

# Run every 6 hours
0 */6 * * * /usr/bin/python3 /path/to/Distro_Watch.py
```

## Output

The script creates a CSV file (`distro_main_releases.csv`) with the following columns:
- **Release Date**: The date the distribution was released
- **Distro Release**: The name of the distribution release
- **Link**: Direct link to the DistroWatch news article

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests!
