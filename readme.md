# Web Scraping Tokopedia

Using Selenium dan BeautifoulSoup the output will be .csv file
## Requirements
- Python 3.x
- Selenium
- BeautifulSoup
- Chrome WebDriver (for Selenium)

## How to Run
Install the package if you don't have it
```bash
pip install -r requirements.txt
```
If you already have the package, just start this
```bash
python scrap_tokopedia.py
```
the default item is Rasbperry Pi 4, for specific Item use script below

```bash
python scrap_tokopedia.py Tas Ibu Ibu
```

## Limitation
- Just Only Search single pattern, ex: Raspberry Pi 4
- Not Pagination