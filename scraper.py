from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import schedule

def initialize_driver():
    """
    Initializes the Selenium WebDriver.
    
    Returns:
    WebDriver: Selenium WebDriver instance.
    """
    return webdriver.Chrome()

def scrape_twitter_account(driver, url, ticker):
    """
    Scrapes a Twitter account for mentions of the specified stock ticker using Selenium.
    
    Parameters:
    driver (WebDriver): Selenium WebDriver instance.
    url (str): URL of the Twitter account.
    ticker (str): Stock ticker to look for.

    Returns:
    int: Count of ticker mentions.
    """
    print(f"Scraping tweets from {url}...")
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load
        
        tweets = driver.find_elements(By.CSS_SELECTOR, 'div[lang]')  # Adjusted to find all tweets
        count = sum(1 for tweet in tweets if re.search(r'\b' + re.escape(ticker) + r'\b', tweet.text, re.IGNORECASE))
        return count
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return 0

def main(accounts, ticker, interval):
    """
    Main function to run the scraper and display results.
    
    Parameters:
    accounts (list): List of Twitter account URLs.
    ticker (str): Stock ticker to look for.
    interval (int): Time interval in minutes for scraping.
    """
    driver = initialize_driver()
    
    print(f"Starting Twitter Scraper for {ticker}...")
    total_count = 0
    for account in accounts:
        count = scrape_twitter_account(driver, account, ticker)
        total_count += count
        print(f"{ticker} was mentioned {count} times on {account}")
    print(f'Total mentions of "{ticker}" in the last {interval} minutes: {total_count}')
    
    driver.quit()

if __name__ == "__main__":
    accounts = [
        "https://twitter.com/Mr_Derivatives",
        "https://twitter.com/warrior0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades",
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox"
    ]
    
    ticker = input("Enter the stock symbol (e.g., $TSLA, $SOFI, $AAPL): ").strip()
    interval = int(input("Enter the time interval in minutes: ").strip())

    schedule.every(interval).minutes.do(main, accounts, ticker, interval)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scraping stopped.")
