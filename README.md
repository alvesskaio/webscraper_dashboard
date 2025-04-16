# News Scraper Dashboard

A real-time news aggregator dashboard built with Python and Streamlit that scrapes news from various sources across different categories.

## Features

- Real-time news scraping from multiple sources
- Five main categories: Technology, Business, Astronomy, Economy, and Cryptocurrencies
- Clean and intuitive Streamlit interface
- Category filtering
- Clickable news links
- Source statistics
- Auto-refresh capability

## Installation

1. Ensure you have Python 3.11 installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)
3. Select a news category from the dropdown menu
4. Click the refresh button to fetch fresh news

## Project Structure

```
webscraper_dashboard/
├── scrapers/
│   └── noticias.py     # News scraping functions
├── data/               # Directory for data storage
├── utils.py            # Utility functions
├── app.py             # Main Streamlit application
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## News Sources

- Technology: Olhar Digital, Canaltech
- Business: Exame, CNN Brazil
- Astronomy: Space.com, Galileu
- Economy: CNN Brazil Economy, Exame
- Cryptocurrencies: Livecoins, Cointelegraph Brazil

## Dependencies

- Python 3.11
- requests
- beautifulsoup4
- pandas
- streamlit
- python-dotenv
- lxml

## Notes

- News data is cached for 5 minutes to prevent excessive requests to source websites
- The application includes error handling for failed requests
- All links open in new tabs for better user experience
