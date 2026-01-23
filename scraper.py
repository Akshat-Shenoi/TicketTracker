"""
Scrapes Vivid Seats pages to extract the lowest available ticket price.
Vivid Seats is more accessible than Ticketmaster and shows prices clearly.
"""

import requests
from bs4 import BeautifulSoup
import re
import time


def get_lowest_price(url):
    """
    Scrapes a Vivid Seats URL and returns the lowest available ticket price.
    
    Args:
        url: The Vivid Seats event URL to scrape
        
    Returns:
        float: The lowest ticket price found, or None if unable to find price
    """
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # Set headers to mimic a real browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://www.google.com/',
        }
        
        print(f"Fetching Vivid Seats page: {url}")
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        price = None
        
        # Method 1: Look for "tickets start at $X" pattern
        # Vivid Seats often displays this prominently on the page
        page_text = soup.get_text()
        
        # Pattern: "tickets start at $84" or "start at $84"
        start_at_pattern = re.search(r'(?:tickets\s+)?start\s+at\s+\$?([\d,]+\.?\d*)', page_text, re.IGNORECASE)
        if start_at_pattern:
            try:
                price = float(start_at_pattern.group(1).replace(',', ''))
                print(f"Found 'start at' price: ${price:.2f}")
                return price
            except ValueError:
                pass
        
        # Method 2: Look for "What is the lowest price?" section
        # Vivid Seats has a FAQ section that shows the lowest price
        lowest_price_pattern = re.search(r'lowest\s+price[^$]*\$?([\d,]+\.?\d*)', page_text, re.IGNORECASE)
        if lowest_price_pattern:
            try:
                price = float(lowest_price_pattern.group(1).replace(',', ''))
                print(f"Found 'lowest price' text: ${price:.2f}")
                return price
            except ValueError:
                pass
        
        # Method 3: Look for price in structured data (JSON-LD)
        script_tags = soup.find_all('script', type='application/ld+json')
        for script in script_tags:
            try:
                import json
                data = json.loads(script.string)
                # Look for offers or price information in structured data
                if isinstance(data, dict):
                    if 'offers' in data:
                        offers = data['offers']
                        if isinstance(offers, list) and offers:
                            price_str = offers[0].get('price', '')
                        elif isinstance(offers, dict):
                            price_str = offers.get('price', '')
                        if price_str:
                            price = float(str(price_str).replace(',', ''))
                            print(f"Found price in structured data: ${price:.2f}")
                            return price
            except (json.JSONDecodeError, ValueError, KeyError, AttributeError):
                continue
        
        # Method 4: Look for price elements with common Vivid Seats classes
        # Try to find price in specific elements
        price_selectors = [
            {'class': re.compile(r'price', re.I)},
            {'data-testid': re.compile(r'price', re.I)},
            {'class': re.compile(r'lowest', re.I)},
            {'class': re.compile(r'cost', re.I)},
        ]
        
        for selector in price_selectors:
            price_elements = soup.find_all(['span', 'div', 'p'], selector)
            for element in price_elements:
                price_text = element.get_text()
                # Look for dollar amounts in the text
                price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text.replace(',', ''))
                if price_match:
                    try:
                        found_price = float(price_match.group(1))
                        # Reasonable price range for concert tickets
                        if 10 <= found_price <= 10000:
                            if price is None or found_price < price:
                                price = found_price
                    except ValueError:
                        continue
        
        # Method 5: Find all prices on page and take the minimum
        if price is None:
            # Search entire page for price patterns like $84 or $84.00
            price_patterns = re.findall(r'\$([\d,]+\.?\d*)', page_text)
            prices = []
            for pattern in price_patterns:
                try:
                    price_value = float(pattern.replace(',', ''))
                    # Reasonable price range for concert tickets
                    if 10 <= price_value <= 10000:
                        prices.append(price_value)
                except ValueError:
                    continue
            
            if prices:
                price = min(prices)  # Get the lowest price found
                print(f"Found lowest price from all prices on page: ${price:.2f}")
        
        if price is None:
            print("Warning: Could not find price on Vivid Seats page.")
            print("The page structure may have changed, or the event may not have tickets available.")
            return None
        
        print(f"Found lowest price: ${price:.2f}")
        return price
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    except Exception as e:
        print(f"Error parsing page: {e}")
        return None
