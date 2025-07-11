#!/usr/bin/env python3
"""
Script to fetch HTML content from Elden Ring wiki pages.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import time
import gzip
import zlib

# Global rate limiting for bulk scraping
last_request_time = 0
MIN_REQUEST_INTERVAL = 15  # Minimum 15 seconds between requests

# Weapon types array based on gallery order
WEAPON_TYPES = [
    "Daggers",
    "Throwing Blades", 
    "Straight Swords",
    "Light Greatswords",
    "Greatswords",
    "Colossal Swords",
    "Thrusting Swords",
    "Heavy Thrusting Swords",
    "Curved Swords",
    "Curved Greatswords",
    "Backhand Blades",
    "Katanas",
    "Great Katanas",
    "Twinblades",
    "Axes",
    "Greataxes",
    "Hammers",
    "Flails",
    "Great Hammers",
    "Colossal Weapons",
    "Spears",
    "Great Spears",
    "Halberds",
    "Reapers",
    "Whips",
    "Fists",
    "Hand-to-Hand",
    "Claws",
    "Beast Claws",
    "Perfume Bottles",
    "Light Bows",
    "Bows",
    "Greatbows",
    "Crossbows",
    "Ballista",
    "Staves",
    "Sacred Seals",
    "Torches",
    "Small Shields",
    "Medium Shields",
    "Greatshields",
    "Thrusting Shields"
]

def read_local_html(filename):
    """
    Read HTML content from a local file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Successfully read local HTML file: {filename} ({len(content)} characters)")
        return content
    except FileNotFoundError:
        print(f"Local HTML file not found: {filename}")
        return None
    except Exception as e:
        print(f"Error reading local HTML file {filename}: {e}")
        return None

def get_headers():
    """
    Get consistent headers for all requests.
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',  # Request compressed content
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

def decompress_content(response):
    """
    Decompress response content based on encoding.
    """
    content_encoding = response.headers.get('content-encoding', '').lower()
    
    if content_encoding == 'gzip':
        try:
            decompressed_content = gzip.decompress(response.content).decode('utf-8')
            print(f"Successfully fetched and decompressed {len(decompressed_content)} characters (was {len(response.content)} compressed)")
            return decompressed_content
        except Exception as e:
            print(f"Gzip decompression failed: {e}. Falling back to raw content.")
            return response.text
    
    elif content_encoding == 'deflate':
        try:
            decompressed_content = zlib.decompress(response.content).decode('utf-8')
            print(f"Successfully fetched and decompressed {len(decompressed_content)} characters (was {len(response.content)} compressed)")
            return decompressed_content
        except Exception as e:
            print(f"Deflate decompression failed: {e}. Falling back to raw content.")
            return response.text
    
    elif content_encoding == 'br':
        try:
            import brotli
            decompressed_content = brotli.decompress(response.content).decode('utf-8')
            print(f"Successfully fetched and decompressed {len(decompressed_content)} characters (was {len(response.content)} compressed)")
            return decompressed_content
        except ImportError:
            print("Brotli compression detected but brotli library not installed. Falling back to uncompressed.")
            return response.text
        except Exception as e:
            print(f"Brotli decompression failed: {e}. Falling back to raw content.")
            return response.text
    
    else:
        print(f"Successfully fetched {len(response.text)} characters (uncompressed)")
        return response.text

def fetch_wiki_page(url):
    """
    Fetch HTML content from a wiki page with proper headers to avoid being blocked.
    Uses compression to reduce bandwidth and potentially avoid rate limiting.
    """
    # Apply rate limiting
    rate_limit()
    
    session = requests.Session()
    session.headers.update(get_headers())
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Fetching content from: {url} (attempt {attempt + 1}/{max_retries})")
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if we got HTML content
            if 'text/html' in response.headers.get('content-type', ''):
                return decompress_content(response)
            else:
                print(f"Warning: Response is not HTML. Content-Type: {response.headers.get('content-type')}")
                return response.text
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                # Longer wait time between retries to be respectful
                wait_time = (attempt + 1) * 30  # 30, 60, 90 seconds
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("All retry attempts failed")
                return None
    
    return None

def rate_limit():
    """
    Ensure minimum time between requests to respect rate limits.
    """
    global last_request_time
    current_time = time.time()
    time_since_last = current_time - last_request_time
    
    if time_since_last < MIN_REQUEST_INTERVAL:
        wait_time = MIN_REQUEST_INTERVAL - time_since_last
        print(f"Rate limiting: waiting {wait_time:.1f} seconds...")
        time.sleep(wait_time)
    
    last_request_time = time.time()

def save_html_content(html_content, filename):
    """
    Save HTML content to a file in the progress folder.
    """
    # Create progress folder if it doesn't exist
    progress_dir = "progress"
    if not os.path.exists(progress_dir):
        os.makedirs(progress_dir)
        print(f"Created progress directory: {progress_dir}")
    
    # Save file in progress folder
    filepath = os.path.join(progress_dir, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML content saved to: {filepath}")
        return True
    except Exception as e:
        print(f"Error saving file {filepath}: {e}")
        return False

def extract_weapon_name(html_content):
    """
    Extract weapon name from the h2 tag with data-source="title" attribute.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find h2 tag with data-source="title"
    title_h2 = soup.find('h2', attrs={'data-source': 'title'})
    
    if title_h2:
        weapon_name = title_h2.get_text(strip=True)
        print(f"Found weapon name: {weapon_name}")
        return weapon_name
    else:
        print("No h2 tag with data-source='title' found")
        return None

def extract_weapon_attributes(html_content):
    """
    Extract weapon attributes from the specific table structure.
    Looks for the second table with class mw-collapsible, rows 3-7 of tbody, second td, span tags.
    Stats order: strength, dexterity, intelligence, faith, arcane.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tables with class mw-collapsible
    collapsible_tables = soup.find_all('table', class_='mw-collapsible')
    
    if len(collapsible_tables) < 2:
        print(f"Not enough collapsible tables found. Found: {len(collapsible_tables)}")
        return None
    
    # Get the second table
    target_table = collapsible_tables[1]
    
    # Find the tbody
    tbody = target_table.find('tbody')
    if not tbody:
        print("No tbody found in the second collapsible table")
        return None
    
    # Get rows 3-7 (index 2-6, since we're 0-indexed)
    rows = tbody.find_all('tr')
    if len(rows) < 7:
        print(f"Not enough rows in tbody. Found: {len(rows)}")
        return None
    
    # Define the attribute names in order
    attribute_names = ['strength', 'dexterity', 'intelligence', 'faith', 'arcane']
    attributes = {}
    
    # Extract attributes from rows 3-7 (index 2-6)
    for i in range(5):  # 5 attributes
        row_index = i + 2  # Start from row 3 (index 2)
        if row_index < len(rows):
            row = rows[row_index]
            cells = row.find_all(['td', 'th'])
            
            if len(cells) >= 2:  # Need at least 2 cells
                # Get the second cell (index 1)
                second_cell = cells[1]
                
                # Find span tags in the second cell
                spans = second_cell.find_all('span')
                
                if spans:
                    # Get the text from the first span
                    attribute_value = spans[0].get_text(strip=True)
                else:
                    # If no spans, get the cell text directly
                    attribute_value = second_cell.get_text(strip=True)

                if not attribute_value or attribute_value == "-" or attribute_value == "":
                    attribute_value = 0
                
                # Special handling for strength attribute
                if attribute_names[i] == 'strength':
                    strength_obj = parse_strength_requirement(attribute_value)
                    attributes[attribute_names[i]] = strength_obj
                    print(f"Found {attribute_names[i]}: {strength_obj}")
                else:
                    attributes[attribute_names[i]] = int(attribute_value)
                    print(f"Found {attribute_names[i]}: {attribute_value}")
            else:
                print(f"Row {row_index + 1} doesn't have enough cells")
        else:
            print(f"Row {row_index + 1} not found")
    
    return attributes

def parse_strength_requirement(strength_text):
    """
    Parse strength requirement text into one-hand and two-hand values.
    Pattern: "[one_hand]\\1h[two_hand]\\2h" or single number.
    """
    print(f"Parsing strength requirement: {strength_text}")
    if not strength_text:
        return {"one_hand": 0, "two_hand": 0}
    
    # Check if the text contains the dual-hand pattern
    if "\\1h" in strength_text and "\\2h" in strength_text:
        try:
            # Split by "\\1h" to get the one-hand value
            parts = strength_text.split("\\1h")
            if len(parts) >= 2:
                one_hand = parts[0].strip()
                print(f"One-hand value: {one_hand}")
                # Get the two-hand value by splitting the remaining part
                two_hand_part = parts[1].split("\\2h")[0].strip()
                
                # Extract just the numeric values before the "\\1h" and "\\2h" markers
                one_hand_value = int(one_hand)
                two_hand_value = int(two_hand_part)
                
                return {
                    "one_hand": one_hand_value,
                    "two_hand": two_hand_value
                }
        except (ValueError, IndexError) as e:
            print(f"Error parsing strength requirement '{strength_text}': {e}")
            # Fallback to single value
            try:
                single_value = int(''.join(filter(str.isdigit, strength_text)))
                return {
                    "one_hand": single_value,
                    "two_hand": single_value
                }
            except ValueError:
                return {"one_hand": 0, "two_hand": 0}
    else:
        # Single value - use for both one-hand and two-hand
        try:
            single_value = int(''.join(filter(str.isdigit, strength_text)))
            return {
                "one_hand": single_value,
                "two_hand": single_value
            }
        except ValueError:
            return {"one_hand": 0, "two_hand": 0}

def extract_gallery_items(html_content):
    """
    Extract all list items from ul elements with the "gallery" class.
    Groups entries by list.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all ul elements with the "gallery" class
    gallery_lists = soup.find_all('ul', class_='gallery')
    
    gallery_data = []
    
    for i, gallery_list in enumerate(gallery_lists):
        # Get the list items from this gallery
        list_items = gallery_list.find_all('li')
        
        gallery_info = {
            'list_index': i,
            'list_items': []
        }
        
        for j, item in enumerate(list_items):
            # Extract text content and any links
            item_text = item.get_text(strip=True)
            
            # Look for links within the list item
            links = item.find_all('a')
            item_links = []
            
            for link in links:
                link_info = {
                    'text': link.get_text(strip=True),
                    'href': link.get('href', ''),
                    'title': link.get('title', '')
                }
                item_links.append(link_info)
            
            item_data = {
                'index': j,
                'text': item_text,
                'links': item_links,
                'raw_html': str(item)
            }
            
            gallery_info['list_items'].append(item_data)
        
        gallery_data.append(gallery_info)
    
    return gallery_data

def save_gallery_data(gallery_data, filename):
    """
    Save gallery data to a JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(gallery_data, f, indent=2, ensure_ascii=False)
        print(f"Gallery data saved to: {filename}")
        return True
    except Exception as e:
        print(f"Error saving gallery data: {e}")
        return False

def fetch_first_weapon_page(gallery_data, base_url="https://eldenring.wiki.gg"):
    """Fetch the webpage for the 1st item in the 1st gallery list."""
    if not gallery_data or len(gallery_data) == 0:
        print("No gallery data available")
        return None
    
    first_gallery = gallery_data[0]
    if not first_gallery['list_items'] or len(first_gallery['list_items']) == 0:
        print("No items in the first gallery")
        return None
    
    first_item = first_gallery['list_items'][1]
    
    print(f"\n=== First Weapon from First Gallery Details ===")
    print(f"Text: {first_item['text']}")
    print(f"Number of links: {len(first_item['links'])}")
    
    weapon_link = None
    for link in first_item['links']:
        if link['href'] and link['href'].startswith('/wiki/'):
            weapon_link = link
            break
    
    if not weapon_link:
        print("No valid weapon link found in the first item")
        return None
    
    print(f"Selected link: {weapon_link['text']} -> {weapon_link['href']}")
    weapon_url = urljoin(base_url, weapon_link['href'])
    print(f"Full URL: {weapon_url}")
    
    weapon_html = fetch_wiki_page(weapon_url)
    
    if weapon_html:
        print(f"\n=== Extracting Weapon Data ===")
        weapon_name = extract_weapon_name(weapon_html)
        weapon_type = get_weapon_type_from_gallery(0)  # First gallery (index 0)
        attributes = extract_weapon_attributes(weapon_html)
        damage_types = extract_damage_types(weapon_html)
        image = extract_weapon_images(weapon_html, weapon_name)
        
        print(f"\n=== Checking DLC Status ===")
        dlc_exclusive = check_dlc_exclusive(gallery_data, weapon_link)
        
        final_weapon_name = weapon_name or weapon_link['text']
        weapon_data_filename = f"weapon_{final_weapon_name.replace(' ', '_').replace('/', '_').lower()}_data.json"
                
        weapon_data = {
            'weapon_name': final_weapon_name,
            'weapon_type': weapon_type,
            'wikiGGLink': weapon_url,
            'wikiFextralifeLink': f"https://eldenring.wiki.fextralife.com/{final_weapon_name.replace(' ', '+')}",
            'attributes': attributes,
            'damage_types': damage_types,
            'attack_types': get_attack_types(final_weapon_name, weapon_type),
            'status_buildup': check_status_buildup(final_weapon_name),
            'image': image,
            'dlc_exclusive': dlc_exclusive
        }
        
        # Create progress folder if it doesn't exist
        progress_dir = "progress"
        if not os.path.exists(progress_dir):
            os.makedirs(progress_dir)
        
        # Save weapon data in progress folder
        weapon_data_filepath = os.path.join(progress_dir, weapon_data_filename)
        with open(weapon_data_filepath, 'w', encoding='utf-8') as f:
            json.dump(weapon_data, f, indent=2, ensure_ascii=False)
        print(f"Weapon data saved to: {weapon_data_filepath}")
        
        return weapon_data
    else:
        print("Failed to fetch weapon page")
        return None

def extract_weapon_images(html_content, weapon_name):
    """
    Extract the weapon image URL from the weapon page.
    Returns only the second image found, which is typically the weapon image itself.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    image = []
    
    # Look for image in various common locations
    # 1. Main content area image
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if content_div:
        # Find all img tags in the content
        img_tags = content_div.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            if src and not src.startswith('data:'):  # Skip data URLs
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://eldenring.wiki.gg' + src
                
                image_info = {
                    'src': src,
                    'alt': alt,
                    'title': weapon_name
                }
                image.append(image_info)
                # print(f"Found image: {src}")
    
    # 2. Look for specific weapon image (often in infoboxes)
    infoboxes = soup.find_all('table', class_='infobox')
    for infobox in infoboxes:
        img_tags = infobox.find_all('img')
        for img in img_tags:
            src = img.get('src', '')
            alt = img.get('alt', '')
            title = img.get('title', '')
            
            if src and not src.startswith('data:'):
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://eldenring.wiki.gg' + src
                
                image_info = {
                    'src': src,
                    'alt': alt,
                    'title': title
                }
                image.append(image_info)
                print(f"Found infobox image: {src}")
    
    # Remove duplicates based on src
    unique_images = []
    seen_srcs = set()
    for img in image:
        if img['src'] not in seen_srcs:
            unique_images.append(img)
            seen_srcs.add(img['src'])
    
    # Return only the second image (the weapon image itself)
    if len(unique_images) >= 2:
        weapon_image = unique_images[1]
        print(f"Selected weapon image: {weapon_image['src']}")
        return weapon_image
    elif len(unique_images) == 1:
        print(f"Only one image found, using: {unique_images[0]['src']}")
        return unique_images[0]
    else:
        print("No image found")
        return None

def extract_damage_types(html_content):
    """
    Extract damage types from the first table with mw-collapsible class.
    Rows 3-7 contain damage values in order: physical, magic, fire, lightning, holy.
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tables with class mw-collapsible
    collapsible_tables = soup.find_all('table', class_='mw-collapsible')
    
    if len(collapsible_tables) == 0:
        print("No collapsible tables found")
        return None
    
    # Get the first table
    target_table = collapsible_tables[0]
    
    # Find the tbody
    tbody = target_table.find('tbody')
    if not tbody:
        print("No tbody found in the first collapsible table")
        return None
    
    # Get rows 3-7 (index 2-6, since we're 0-indexed)
    rows = tbody.find_all('tr')
    if len(rows) < 7:
        print(f"Not enough rows in tbody. Found: {len(rows)}")
        return None
    
    # Define damage types in order
    damage_types = ['Physical', 'Magic', 'Fire', 'Lightning', 'Holy']
    damage_values = {}
    
    # Extract damage values from rows 3-7 (index 2-6)
    for i in range(5):  # 5 damage types
        row_index = i + 2  # Start from row 3 (index 2)
        if row_index < len(rows):
            row = rows[row_index]
            cells = row.find_all(['td', 'th'])
            
            if len(cells) >= 2:  # Need at least 2 cells
                # Get the second cell (index 1)
                second_cell = cells[1]
                
                # Find span tags in the second cell
                spans = second_cell.find_all('span')
                
                if spans:
                    # Get the text from the first span
                    try:
                        damage_value = int(spans[0].get_text(strip=True))
                        damage_values[damage_types[i]] = damage_value
                        print(f"Found {damage_types[i]} damage: {damage_value}")
                    except ValueError:
                        print(f"Could not parse {damage_types[i]} damage value")
                else:
                    print(f"No span found in row {row_index + 1}")
            else:
                print(f"Row {row_index + 1} doesn't have enough cells")
        else:
            print(f"Row {row_index + 1} not found")
    
    if not damage_values:
        print("No damage values found")
        return None
    
    # Find the major damage type (highest value)
    major_type = max(damage_values, key=damage_values.get)
    major_value = damage_values[major_type]
    
    # Find minor damage types (all types with >0 damage, excluding major)
    minor_types = []
    for damage_type, value in damage_values.items():
        if value > 0 and damage_type != major_type:
            minor_types.append(damage_type)
    
    result = {
        'major': major_type,
        'minor': minor_types
    }
    
    print(f"Major damage type: {major_type} ({major_value})")
    print(f"Minor damage types: {minor_types}")
    
    return result

def check_dlc_exclusive(gallery_data, weapon_link):
    """
    Check if a weapon is DLC-exclusive by looking for "Elden Ring: Shadow of the Erdtree" title.
    """
    # Find the weapon's list item in the gallery data
    for gallery in gallery_data:
        for item in gallery['list_items']:
            for link in item['links']:
                if link['href'] == weapon_link['href']:
                    # Found the matching weapon, now check its structure
                    soup = BeautifulSoup(item['raw_html'], 'html.parser')
                    
                    # Look for the second child of the li element
                    li_element = soup.find('li')
                    if li_element:
                        children = list(li_element.children)
                        if len(children) >= 2:
                            second_child = children[1]
                            
                            # Check if the second child has a child with the DLC title
                            if hasattr(second_child, 'find'):
                                dlc_element = second_child.find(title="Elden Ring: Shadow of the Erdtree")
                                if dlc_element:
                                    print(f"Found DLC indicator: {dlc_element.get('title', '')}")
                                    return True
                    
                    # Alternative: search for the DLC title anywhere in the item
                    if "Elden Ring: Shadow of the Erdtree" in item['raw_html']:
                        print("Found DLC indicator in raw HTML")
                        return True
    
    return False

def get_weapon_type_from_gallery(gallery_index):
    """Get weapon type based on gallery index."""
    if 0 <= gallery_index < len(WEAPON_TYPES):
        return WEAPON_TYPES[gallery_index]
    else:
        return "Unknown"

def get_attack_types(weapon_name, weapon_type):
    """
    Determine primary and secondary attack types based on weapon type and name.
    Returns a dictionary with 'primary' and 'secondary' attack types.
    """
    # Slash damage weapons (all weapons from these classes) - PRIMARY attack type
    slash_weapon_types = {
        "Backhand Blades",
        "Beast Claws", 
        "Claws",
        "Curved Greatswords",
        "Curved Swords",
        "Daggers",
        "Great Katanas",
        "Katanas",
        "Reapers"
    }
    
    # Specific weapons that deal slash damage (exceptions in their classes) - PRIMARY attack type
    slash_specific_weapons = {
        "Glaive",
        "Loretta's War Sickle", 
        "Nightrider Glaive",
        "Pest's Glaive",
        "Poleblade of the Bud",
        "Spirit Glaive",
        "Urumi"
    }
    
    # Pierce damage weapon classes (all weapons from these classes) - PRIMARY attack type
    pierce_weapon_types = {
        "Ballista",
        "Bows",
        "Crossbows", 
        "Great Spears",
        "Greatbows",
        "Heavy Thrusting Swords",
        "Light Bows",
        "Spears",
        "Throwing Blades",
        "Thrusting Swords"
    }
    
    # Pierce damage weapon classes (Pierce is SECONDARY attack type)
    pierce_secondary_weapon_types = {
        "Colossal Swords",
        "Daggers",
        "Great Katanas",
        "Greatswords", 
        "Halberds",
        "Katanas",
        "Light Greatswords",
        "Straight Swords",
        "Thrusting Shields",
        "Twinblades"
    }
    
    # Specific weapons that deal Pierce damage (exceptions in their classes) - PRIMARY attack type
    pierce_specific_weapons = {
        # Backhand Blades
        # Colossal Weapons
        "Fallingstar Beast Jaw",
        # Hammers
        "Flowerstone Gavel",
        # Axes
        "Forked Hatchet",
        # Fists
        "Katar",
        "Pata",
        "Thiollier's Hidden Needle",
        "Veteran's Prosthesis",
        # Halberds
        "Lucerne",
        # Great Hammers
        "Pickaxe",
        # Greataxes
        "Rusted Anchor",
        # Hammers
        "Warpick"
    }
    
    # Strike damage weapon classes (with exceptions) - PRIMARY attack type
    strike_weapon_types = {
        "Hammers",
        "Fists", 
        "Flails",
        "Great Hammers",
        "Hand-to-Hand",
        "Greatshields",
        "Shields",
        "Torches",
        "Whips"
    }
    
    # Specific weapons that deal strike damage (exceptions in their classes) - PRIMARY attack type
    strike_specific_weapons = {
        # Colossal Weapons
        "Anvil Hammer",
        "Bloodfiend's Arm",
        "Devonia's Hammer", 
        "Envoy's Greathorn",
        "Gazing Finger",
        "Giant-Crusher",
        "Great Club",
        "Prelate's Inferno Crozier",
        "Rotten Staff",
        "Shadow Sunflower Blossom",
        "Staff of the Avatar",
        "Troll's Hammer",
        "Watchdog's Staff",
        # Other classes
        "Jawbone Axe",
        "Spiked Spear",
        "Stone-Sheathed Sword"
    }
    
    # Standard damage weapon classes (all weapons from these classes) - PRIMARY attack type
    standard_weapon_types = {
        "Axes",
        "Colossal Swords",
        "Greataxes", 
        "Greatbows",
        "Great Spears",
        "Greatswords",
        "Halberds",
        "Spears",
        "Straight Swords",
        "Twinblades"
    }
    
    # Spell damage weapon classes (Staves and Sacred Seals) - PRIMARY attack type
    spell_weapon_types = {
        "Staves",
        "Sacred Seals"
    }
    
    # Standard damage weapon classes (Standard is SECONDARY attack type)
    standard_secondary_weapon_types = {
        "Heavy Thrusting Swords",
        "Thrusting Swords"
    }
    
    # Specific weapons that deal Standard damage (exceptions in their classes) - PRIMARY attack type
    standard_specific_weapons = {
        # Colossal Weapons
        "Axe of Godfrey",
        "Dragon Greatclaw", 
        "Duelist Greataxe",
        "Ghiza's Wheel",
        "Golem's Halberd",
        "Rotten Greataxe"
    }
    
    # Weapons that DON'T deal Standard damage (exceptions to their classes)
    non_standard_weapons = {
        # Axes exceptions
        "Jawbone Axe",
        "Forked Hatchet",
        # Greataxes exceptions
        "Rusted Anchor",
        # Spears exceptions
        "Partisan",
        "Spiked Spear", 
        "Cross-Naginata",
        # Straight Swords exceptions
        "Coded Sword",
        "Stone-Sheathed Sword"
    }
    
    # Determine primary attack type
    if weapon_type in spell_weapon_types:
        primary = "Spell"
    elif (weapon_type in slash_weapon_types or weapon_name in slash_specific_weapons):
        primary = "Slash"
    elif (weapon_type in pierce_weapon_types or weapon_name in pierce_specific_weapons):
        primary = "Pierce"
    elif (weapon_type in strike_weapon_types or weapon_name in strike_specific_weapons):
        primary = "Strike"
    elif ((weapon_type in standard_weapon_types and weapon_name not in non_standard_weapons) or
          weapon_name in standard_specific_weapons):
        primary = "Standard"
    else:
        primary = "Standard"  # Default fallback
    
    # Determine secondary attack type
    if weapon_type in pierce_secondary_weapon_types:
        # These weapon types have Pierce as secondary
        secondary = "Pierce"
    elif weapon_type in standard_secondary_weapon_types:
        # These weapon types have Standard as secondary
        secondary = "Standard"
    else:
        # For now, set secondary to same as primary
        # This can be expanded later when you research secondary attack patterns
        secondary = primary
    
    return {
        "primary": primary,
        "secondary": secondary
    }

def get_blood_loss_weapons():
    """
    Get the list of weapons that have blood loss status buildup.
    Based on Fextralife data - only recording presence, not numbers.
    """
    return {
        # Great Spears
        "Barbed Staff-Spear",
        "Bloodfiend's Sacred Spear",
        "Mohgwyn's Sacred Spear",
        
        # Beast Claws
        "Beast Claw",
        "Red Bear's Claw",
        
        # Colossal Weapons
        "Bloodfiend's Arm",
        "Ghiza's Wheel",
        
        # Spears
        "Bloodfiend's Fork",
        "Cross-Naginata",
        "Inquisitor's Girandole",
        "Spiked Spear",
        
        # Claws
        "Bloodhound Claws",
        "Claws of Night",
        "Hookclaws",
        "Raptor Talons",
        
        # Curved Greatswords
        "Bloodhound's Fang",
        "Morgott's Cursed Sword",
        
        # Daggers
        "Bloodstained Dagger",
        "Great Knife",
        "Reduvia",
        "Wakizashi",
        
        # Heavy Thrusting Swords
        "Bloody Helice",
        
        # Greatshields
        "Briar Greatshield",
        "Spiked Palisade Shield",
        
        # Flails
        "Chainlink Flail",
        "Flail",
        "Nightrider Flail",
        
        # Backhand Blades
        "Curseblade's Cirque",
        
        # Great Katanas
        "Dragon-Hunter's Great Katana",
        "Great Katana",
        "Rakshasa's Great Katana",
        
        # Twinblades
        "Eleonora's Poleblade",
        
        # Curved Swords
        "Falx",
        "Scavenger's Curved Sword",
        
        # Axes
        "Forked Hatchet",
        "Forked-Tongue Hatchet",
        
        # Greatswords
        "Flamberge",
        "Forked Greatsword",
        "Sword of Milos",
        
        # Greataxes
        "Great Omenkiller Cleaver",
        
        # Great Hammers
        "Great Stars",
        
        # Reapers
        "Grave Scythe",
        "Halo Scythe",
        "Obsidian Lamina",
        "Scythe",
        "Winged Scythe",
        
        # Katanas
        "Hand of Malenia",
        "Meteoric Ore Blade",
        "Moonveil",
        "Nagakiba",
        "Rivers of Blood",
        "Star-Lined Sword",
        "Sword of Night",
        "Uchigatana",
        
        # Whips
        "Hoslow's Petal Whip",
        "Thorned Whip",
        
        # Medium Shields
        "Marred Leather Shield",
        "Marred Wooden Shield",
        
        # Hammers
        "Morning Star",
        "Spiked Club",
        "Varré's Bouquet",
        
        # Small Shields
        "Shield of the Guilty",
        "Spiralhorn Shield",
        
        # Fists
        "Spiked Caestus",
        "Star Fist",
        
        # Staves
        "Staff of the Guilty",
        
        # Halberds
        "Vulgar Militia Saw"
    }

def get_poison_weapons():
    """
    Get the list of weapons that have poison status buildup.
    Based on Fextralife data - only recording presence, not numbers.
    """
    return {
        # Shields
        "Ant's Skull Plate",
        "Coil Shield",
        
        # Perfume Bottles
        "Deadly Poison Perfume Bottle",
        
        # Fists
        "Poisoned Hand",
        
        # Katanas
        "Serpentbone Blade",
        
        # Bows
        "Serpent Bow",
        
        # Whips
        "Tooth Whip",
        
        # Claws
        "Venomous Fang"
    }

def get_scarlet_rot_weapons():
    """
    Get the list of weapons that have scarlet rot status buildup.
    Based on Fextralife data - only recording presence, not numbers.
    """
    return {
        # Thrusting Swords
        "Antspur Rapier",
        
        # Halberds
        "Poleblade of the Bud",
        
        # Warhammers
        "Rotten Battle Hammer",
        
        # Spears
        "Rotten Crystal Spear",
        
        # Staves
        "Rotten Crystal Staff",
        
        # Straight Swords
        "Rotten Crystal Sword",
        
        # Colossal Weapons
        "Rotten Greataxe",
        "Rotten Staff",
        
        # Daggers
        "Scorpion's Stinger"
    }

def get_frostbite_weapons():
    """
    Get the list of weapons that have frostbite status buildup.
    Based on Fextralife data - only recording presence, not numbers.
    """
    return {
        # Perfume Bottles
        "Chilling Perfume Bottle",
        
        # Greatswords
        "Dark Moon Greatsword",
        "Death's Poker",
        
        # Thrusting Swords
        "Frozen Needle",
        
        # Torches
        "Ghostflame Torch",
        
        # Axes
        "Icerind Hatchet",
        
        # Greataxes
        "Putrescence Cleaver",
        
        # Curved Greatswords
        "Zamor Curved Sword"
    }

def get_sleep_weapons():
    """
    Get the list of weapons that have sleep status buildup.
    Based on Fextralife data - only recording presence, not numbers.
    """
    return {
        # Torches
        "St. Trina's Torch",
        
        # Straight Swords
        "Sword of St Trina",
        "Velvet Sword of St Trina",
        
        # Fists
        "Thiollier's Hidden Needle"
    }

def get_madness_weapons():
    """
    Get the list of weapons that have madness status buildup.
    Based on Fextralife data - only recording presence, not numbers.
    """
    return {
        # Great Spears
        "Vyke's War Spear",
        
        # Greatshields
        "Fingerprint Stone Shield",
        
        # Seals
        "Frenzied Flame Seal",
        
        # Perfume Bottles
        "Frenzyflame Perfume Bottle",
        
        # Fists
        "Madding Hand",
        
        # Torches
        "Nanaya's Torch"
    }

def check_status_buildup(weapon_name):
    """
    Check if a weapon has any status buildup.
    Returns the status type as a string, or "none" if no status.
    """
    blood_loss_weapons = get_blood_loss_weapons()
    poison_weapons = get_poison_weapons()
    scarlet_rot_weapons = get_scarlet_rot_weapons()
    frostbite_weapons = get_frostbite_weapons()
    sleep_weapons = get_sleep_weapons()
    madness_weapons = get_madness_weapons()
    
    if weapon_name in blood_loss_weapons:
        return "blood_loss"
    elif weapon_name in poison_weapons:
        return "poison"
    elif weapon_name in scarlet_rot_weapons:
        return "scarlet_rot"
    elif weapon_name in frostbite_weapons:
        return "frostbite"
    elif weapon_name in sleep_weapons:
        return "sleep"
    elif weapon_name in madness_weapons:
        return "madness"
    else:
        return "none"

def fetch_all_weapons(gallery_data, base_url="https://eldenring.wiki.gg"):
    """Fetch all weapons from all galleries with progress tracking and resume capability."""
    all_weapons = []
    total_weapons = sum(len(gallery['list_items']) for gallery in gallery_data)
    processed_count = 0
    
    print(f"\n=== Starting Bulk Weapon Fetch ===")
    print(f"Total weapons to process: {total_weapons}")
    print(f"Estimated time: {total_weapons * MIN_REQUEST_INTERVAL / 60:.1f} minutes")
    
    # Create progress folder if it doesn't exist
    progress_dir = "progress"
    if not os.path.exists(progress_dir):
        os.makedirs(progress_dir)
        print(f"Created progress directory: {progress_dir}")
    
    progress_file = os.path.join(progress_dir, "weapon_fetch_progress.json")
    processed_weapons = set()
    
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)
                processed_weapons = set(progress_data.get('processed_weapons', []))
                print(f"Resuming from previous run. Already processed: {len(processed_weapons)} weapons")
        except:
            print("Could not load progress file, starting fresh")
    
    # Dictionary to store weapons by gallery/type
    weapons_by_gallery = {}
    
    for gallery_index, gallery in enumerate(gallery_data):
        weapon_type = get_weapon_type_from_gallery(gallery_index)
        gallery_filename = f"weapons_{weapon_type.lower().replace(' ', '_').replace('-', '_')}.json"
        gallery_filepath = os.path.join(progress_dir, gallery_filename)
        
        # Load existing gallery data if it exists
        existing_gallery_weapons = []
        if os.path.exists(gallery_filepath):
            try:
                with open(gallery_filepath, 'r', encoding='utf-8') as f:
                    existing_gallery_weapons = json.load(f)
                print(f"Loaded {len(existing_gallery_weapons)} existing weapons from {gallery_filename}")
            except Exception as e:
                print(f"Error loading existing gallery data: {e}")
                existing_gallery_weapons = []
        
        # Create a set of existing weapon names for quick lookup
        existing_weapon_names = {weapon['weapon_name'] for weapon in existing_gallery_weapons}
        
        gallery_weapons = existing_gallery_weapons.copy()  # Start with existing weapons
        newly_processed_count = 0
        
        print(f"\n--- Processing Gallery {gallery_index + 1}/{len(gallery_data)}: {weapon_type} ---")
        
        for item_index, item in enumerate(gallery['list_items']):
            processed_count += 1
            
            weapon_link = None
            for link in item['links']:
                if link['href'] and link['href'].startswith('/wiki/'):
                    weapon_link = link
                    break
            
            if not weapon_link:
                print(f"Skipping item {item_index + 1} - no valid link")
                continue
            
            weapon_id = weapon_link['href']
            if weapon_id in processed_weapons:
                print(f"Skipping {weapon_link['text']} - already processed")
                continue
            
            print(f"\n[{processed_count}/{total_weapons}] Processing: {weapon_link['text']}")
            weapon_url = urljoin(base_url, weapon_link['href'])
            weapon_html = fetch_wiki_page(weapon_url)
            
            if weapon_html:
                weapon_name = extract_weapon_name(weapon_html)
                attributes = extract_weapon_attributes(weapon_html)
                damage_types = extract_damage_types(weapon_html)
                image = extract_weapon_images(weapon_html, weapon_name)
                dlc_exclusive = check_dlc_exclusive(gallery_data, weapon_link)
                
                final_weapon_name = weapon_name or weapon_link['text']
                
                weapon_data = {
                    'weapon_name': final_weapon_name,
                    'weapon_type': weapon_type,
                    'wikiGGLink': weapon_url,
                    'wikiFextralifeLink': f"https://eldenring.wiki.fextralife.com/{final_weapon_name.replace(' ', '+')}",
                    'attributes': attributes,
                    'damage_types': damage_types,
                    'attack_types': get_attack_types(final_weapon_name, weapon_type),
                    'status_buildup': check_status_buildup(final_weapon_name),
                    'image': image,
                    'dlc_exclusive': dlc_exclusive
                }
                
                # Only add to gallery if it's not already there
                if final_weapon_name not in existing_weapon_names:
                    gallery_weapons.append(weapon_data)
                    newly_processed_count += 1
                    
                    # Save gallery file immediately after adding new weapon
                    with open(gallery_filepath, 'w', encoding='utf-8') as f:
                        json.dump(gallery_weapons, f, indent=2, ensure_ascii=False)
                    print(f"✓ Updated gallery file: {gallery_filepath} ({len(gallery_weapons)} weapons total)")
                
                all_weapons.append(weapon_data)
                processed_weapons.add(weapon_id)
                
                # Save progress
                with open(progress_file, 'w') as f:
                    json.dump({
                        'processed_weapons': list(processed_weapons),
                        'total_processed': len(processed_weapons)
                    }, f, indent=2)
                
                print(f"✓ Processed: {final_weapon_name}")
            else:
                print(f"✗ Failed to fetch: {weapon_link['text']}")
        
        # Gallery file is now saved incrementally, just store the data for summary
        if gallery_weapons:
            weapons_by_gallery[weapon_type] = gallery_weapons
            print(f"✓ Gallery {weapon_type} complete: {len(gallery_weapons)} weapons total ({newly_processed_count} newly processed)")
    
    print(f"\n=== Bulk Fetch Complete ===")
    print(f"Successfully processed: {len(all_weapons)} weapons")
    print(f"Total time: {len(all_weapons) * MIN_REQUEST_INTERVAL / 60:.1f} minutes")
    
    # Save combined file as well
    combined_filename = "all_weapons_data.json"
    with open(combined_filename, 'w', encoding='utf-8') as f:
        json.dump(all_weapons, f, indent=2, ensure_ascii=False)
    print(f"✓ Combined data saved to: {combined_filename}")
    
    # Save gallery summary
    gallery_summary = {
        'total_weapons': len(all_weapons),
        'galleries': {}
    }
    
    for weapon_type, weapons in weapons_by_gallery.items():
        gallery_summary['galleries'][weapon_type] = {
            'count': len(weapons),
            'filename': f"weapons_{weapon_type.lower().replace(' ', '_').replace('-', '_')}.json"
        }
    
    gallery_summary_filepath = os.path.join(progress_dir, "gallery_summary.json")
    with open(gallery_summary_filepath, 'w', encoding='utf-8') as f:
        json.dump(gallery_summary, f, indent=2, ensure_ascii=False)
    print(f"✓ Gallery summary saved to: {gallery_summary_filepath}")
    
    return all_weapons

def display_weapon_summary(weapon_data):
    """
    Display a formatted summary of weapon data.
    """
    print(f"\n=== Successfully fetched weapon from 1st gallery ===")
    print(f"Weapon: {weapon_data['weapon_name']}")
    print(f"Type: {weapon_data['weapon_type']}")
    print(f"Wiki.gg URL: {weapon_data['wikiGGLink']}")
    print(f"Fextralife URL: {weapon_data['wikiFextralifeLink']}")
    
    if weapon_data['attributes']:
        print(f"\n=== Weapon Attributes ===")
        for attr, value in weapon_data['attributes'].items():
            if attr == 'strength' and isinstance(value, dict):
                print(f"{attr.capitalize()}: {value['one_hand']} (1H) / {value['two_hand']} (2H)")
            else:
                print(f"{attr.capitalize()}: {value}")
    else:
        print("No attributes found")
    
    if weapon_data['damage_types']:
        print(f"\n=== Damage Types ===")
        damage = weapon_data['damage_types']
        print(f"Major: {damage['major']}")
        if damage['minor']:
            print(f"Minor: {', '.join(damage['minor'])}")
        else:
            print("Minor: None")
    else:
        print("No damage types found")
    
    if weapon_data['attack_types']:
        print(f"\n=== Attack Types ===")
        attack = weapon_data['attack_types']
        print(f"Primary: {attack['primary']}")
        print(f"Secondary: {attack['secondary']}")
    else:
        print("No attack types found")
    
    if weapon_data['status_buildup']:
        print(f"\n=== Status Buildup ===")
        status = weapon_data['status_buildup']
        if status == "none":
            print("Status: None")
        else:
            print(f"Status: {status.replace('_', ' ').title()}")
    else:
        print("No status buildup found")
    
    print(f"\n=== Weapon Status ===")
    print(f"DLC Exclusive: {weapon_data['dlc_exclusive']}")
    
    if weapon_data['image']:
        print(f"\n=== Weapon Image ===")
        img = weapon_data['image']
        print(f"Image URL: {img['src']}")
        if img['alt']:
            print(f"Alt: {img['alt']}")
        if img['title']:
            print(f"Title: {img['title']}")
    else:
        print("No weapon image found")

def main():
    """
    Main function to fetch the Weapons page HTML and extract gallery items.
    """
    # Try to read from local file first
    html_content = read_local_html('weapons_page.html')
    if not html_content:
        print("Local weapons_page.html not found. Please run the script with option 2 first to download it.")
        return
    
    print("Using local weapons_page.html file")
    print(f"Successfully read HTML content ({len(html_content)} characters)")
    
    # Extract gallery items
    gallery_data = extract_gallery_items(html_content)
    
    if gallery_data:
        # Save gallery data
        save_gallery_data(gallery_data, 'weapons_gallery_data.json')
        
        # Print summary
        print(f"\n=== Gallery Summary ===")
        print(f"Found {len(gallery_data)} gallery lists")
        
        total_items = sum(len(gallery['list_items']) for gallery in gallery_data)
        print(f"Total items across all galleries: {total_items}")
        
        for i, gallery in enumerate(gallery_data):
            print(f"Gallery {i}: {len(gallery['list_items'])} items")
            
            # Show first few items as examples
            for j, item in enumerate(gallery['list_items'][:3]):
                print(f"  - Item {j}: {item['text'][:50]}...")
            if len(gallery['list_items']) > 3:
                print(f"  ... and {len(gallery['list_items']) - 3} more items")
        
        # Ask user what they want to do
        print(f"\n=== Options ===")
        print("1. Fetch single weapon (first from first gallery)")
        print("2. Fetch all weapons (bulk mode)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Fetch the first weapon page
            weapon_data = fetch_first_weapon_page(gallery_data)
            
            if weapon_data:
                display_weapon_summary(weapon_data)
        
        elif choice == "2":
            # Fetch all weapons
            all_weapons = fetch_all_weapons(gallery_data)
            print(f"\n=== Bulk Fetch Summary ===")
            print(f"Total weapons processed: {len(all_weapons)}")
            
            # Save combined data
            combined_filename = "all_weapons_data.json"
            with open(combined_filename, 'w', encoding='utf-8') as f:
                json.dump(all_weapons, f, indent=2, ensure_ascii=False)
            print(f"Combined data saved to: {combined_filename}")
        
        elif choice == "3":
            print("Exiting...")
        
        else:
            print("Invalid choice. Exiting...")
    else:
        print("No gallery data found")

if __name__ == "__main__":
    main()
