#!/usr/bin/env python3
"""
Script to fetch HTML content from Elden Ring wiki pages.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin

def fetch_wiki_page(url):
    """
    Fetch HTML content from a wiki page with proper headers to avoid being blocked.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"Fetching content from: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Check if we got HTML content
        if 'text/html' in response.headers.get('content-type', ''):
            return response.text
        else:
            print(f"Warning: Response is not HTML. Content-Type: {response.headers.get('content-type')}")
            return response.text
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_html_content(html_content, filename):
    """
    Save HTML content to a file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML content saved to: {filename}")
        return True
    except Exception as e:
        print(f"Error saving file {filename}: {e}")
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
    """
    Fetch the webpage for the 1st item in the 1st gallery list.
    """
    if not gallery_data or len(gallery_data) == 0:
        print("No gallery data available")
        return None
    
    first_gallery = gallery_data[0]
    if not first_gallery['list_items'] or len(first_gallery['list_items']) == 0:
        print("No items in the first gallery")
        return None
    
    first_item = first_gallery['list_items'][0]
    
    print(f"\n=== First Weapon from First Gallery Details ===")
    print(f"Text: {first_item['text']}")
    print(f"Number of links: {len(first_item['links'])}")
    
    # Find the first valid link
    weapon_link = None
    for link in first_item['links']:
        if link['href'] and link['href'].startswith('/wiki/'):
            weapon_link = link
            break
    
    if not weapon_link:
        print("No valid weapon link found in the first item")
        return None
    
    print(f"Selected link: {weapon_link['text']} -> {weapon_link['href']}")
    
    # Construct full URL
    weapon_url = urljoin(base_url, weapon_link['href'])
    print(f"Full URL: {weapon_url}")
    
    # Fetch the weapon page
    weapon_html = fetch_wiki_page(weapon_url)
    
    if weapon_html:
        # Extract weapon data first
        print(f"\n=== Extracting Weapon Data ===")
        weapon_name = extract_weapon_name(weapon_html)
        weapon_type = extract_weapon_type(weapon_html)
        attributes = extract_weapon_attributes(weapon_html)
        damage_types = extract_damage_types(weapon_html)
        image = extract_weapon_images(weapon_html, weapon_name)
        
        # Check if weapon is DLC-exclusive
        print(f"\n=== Checking DLC Status ===")
        dlc_exclusive = check_dlc_exclusive(gallery_data, weapon_link)
        
        # Use extracted weapon name or fallback to link text
        final_weapon_name = weapon_name or weapon_link['text']
        
        # Create filenames using the weapon name
        weapon_filename = f"weapon_{final_weapon_name.replace(' ', '_').replace('/', '_').lower()}.html"
        weapon_data_filename = f"weapon_{final_weapon_name.replace(' ', '_').replace('/', '_').lower()}_data.json"
        
        # Save the weapon page HTML
        save_html_content(weapon_html, weapon_filename)
        
        weapon_data = {
            'weapon_name': final_weapon_name,
            'weapon_type': weapon_type,
            'weapon_url': weapon_url,
            'filename': weapon_filename,
            'attributes': attributes,
            'damage_types': damage_types,
            'image': image,
            'dlc_exclusive': dlc_exclusive
        }
        
        # Save weapon data with attributes
        with open(weapon_data_filename, 'w', encoding='utf-8') as f:
            json.dump(weapon_data, f, indent=2, ensure_ascii=False)
        print(f"Weapon data saved to: {weapon_data_filename}")
        
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

def extract_weapon_type(html_content):
    """
    Extract weapon type from the div with data-source="type".
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find div with data-source="type"
    type_div = soup.find('div', attrs={'data-source': 'type'})
    
    if type_div:
        # Get the 2nd child of the div
        children = list(type_div.children)
        if len(children) >= 3:
            third_child = children[3] # 2nd child is the weapon type. Index 3 because newlines are counted as children.
            weapon_type = third_child.get_text(strip=True)
            print(f"Found weapon type: {weapon_type}")
            return weapon_type
        else:
            print(f"Not enough children in type div. Found: {len(children)}")
    else:
        print("No div with data-source='type' found")
    
    return None

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
        'major': {
            'type': major_type,
            'value': major_value
        },
        'minor': minor_types
    }
    
    print(f"Major damage type: {major_type} ({major_value})")
    print(f"Minor damage types: {minor_types}")
    
    return result

def main():
    """
    Main function to fetch the Weapons page HTML and extract gallery items.
    """
    url = "https://eldenring.wiki.gg/wiki/Weapons"
    
    # Fetch the HTML content
    html_content = fetch_wiki_page(url)
    
    if html_content:
        # Save raw HTML
        save_html_content(html_content, 'weapons_page.html')
        print(f"Successfully fetched and saved HTML content ({len(html_content)} characters)")
        
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
            
            # Fetch the first weapon page
            weapon_data = fetch_first_weapon_page(gallery_data)
            
            if weapon_data:
                print(f"\n=== Successfully fetched weapon from 1st gallery ===")
                print(f"Weapon: {weapon_data['weapon_name']}")
                print(f"Type: {weapon_data['weapon_type']}")
                print(f"URL: {weapon_data['weapon_url']}")
                print(f"HTML saved to: {weapon_data['filename']}")
                
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
                    print(f"Major: {damage['major']['type']} ({damage['major']['value']})")
                    if damage['minor']:
                        print(f"Minor: {', '.join(damage['minor'])}")
                    else:
                        print("Minor: None")
                else:
                    print("No damage types found")
                
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
        else:
            print("No gallery data found")
    else:
        print("Failed to fetch HTML content")

if __name__ == "__main__":
    main()
