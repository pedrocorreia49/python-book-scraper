# 📚 E-Commerce Price Tracker (Web Scraper)

A robust Python script that extracts product data from e-commerce websites and exports it to CSV/Excel.

## 🚀 Features
- **Multi-page Scraping:** Handles pagination automatically.
- **Data Export:** Saves clean data to CSV using Pandas.
- **Error Handling:** Gracefully handles network errors.
- **Logging:** Detailed console logs for monitoring.

## 🛠 Tech Stack
- Python 3.9+
- BeautifulSoup4
- Requests
- Pandas

## 📖 Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scraper.py --pages 2 --output data.csv