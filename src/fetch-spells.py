#!/usr/bin/env python3
"""
Script to fetch HTML content from Elden Ring wiki pages for spells.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import quote
import time
import gzip
import zlib

# Global rate limiting for bulk scraping
last_request_time = 0
MIN_REQUEST_INTERVAL = 15  # Minimum 15 seconds between requests

# Spell types array - will be populated based on the spells page structure
SPELL_TYPES = []

def get_blood_loss_spells():
    """
    Get the list of spells that have blood loss status buildup.
    """
    return {
        # Incantations
        "Bloodboon",
        "Bloodflame Blade", 
        "Bloodflame Talons",
        "Furious Blade of Ansbach",
        "Swarm of Flies",
        
        # Sorceries
        "Briars of Punishment",
        "Briars of Sin", 
        "Impenetrable Thorns"
    }

def get_poison_spells():
    """
    Get the list of spells that have poison status buildup.
    """
    return {
        # Incantations
        "Poison Armament",
        "Poison Mist"
    }

def get_scarlet_rot_spells():
    """
    Get the list of spells that have scarlet rot status buildup.
    """
    return {
        # Incantations
        "Ekzykes's Decay",
        "Rotten Breath",
        "Rotten Butterflies",
        "Scarlet Aeonia"
    }

def get_frostbite_spells():
    """
    Get the list of spells that have frostbite status buildup.
    """
    return {
        # Sorceries
        "Adula's Moonblade",
        "Explosive Ghostflame",
        "Freezing Mist",
        "Frozen Armament",
        "Glintstone Icecrag",
        "Mass of Putrescence",
        "Ranni's Dark Moon",
        "Rings of Spectral Light",
        "Vortex of Putrescence",
        "Zamor Ice Storm",
        
        # Incantations
        "Borealis's Mist",
        "Dragonice",
        "Ghostflame Breath",
        "Frozen Lightning Spear"
    }

def get_madness_spells():
    """
    Get the list of spells that have madness status buildup.
    """
    return {
        # Incantations
        "Frenzied Burst",
        "Howl of Shabriri",
        "Inescapable Frenzy",
        "Midra's Flame of Frenzy",
        "The Flame of Frenzy",
        "Unendurable Frenzy"
    }

def get_fire_damage_spells():
    """
    Get the list of spells that deal fire damage.
    """
    return {
        # Sorceries
        "Gelmir's Fury",
        "Magma Shot",
        "Roiling Magma",
        "Rykard's Rancor",
        
        # Incantations
        "Agheel's Flame",
        "Aspects of the Crucible: Breath",
        "Bayle's Flame Lightning",
        "Bayle's Tyranny",
        "Black Flame",
        "Black Flame Blade",
        "Black Flame Ritual",
        "Bloodboon",
        "Bloodflame Blade",
        "Bloodflame Talons",
        "Burn, O Flame!",
        "Flame, Grant me Strength",
        "Catch Flame",
        "Dragonfire",
        "Fire's Deadly Sin",
        "Fire Serpent",
        "Flame of the Fell God",
        "Flame Sling",
        "Flame, Fall Upon Them",
        "Frenzied Burst",
        "Furious Blade of Ansbach",
        "Giantsflame Take Thee",
        "Howl of Shabriri",
        "Inescapable Frenzy",
        "Magma Breath",
        "Midra's Flame of Frenzy",
        "Messmer's Orb",
        "Noble Presence",
        "O, Flame!",
        "Placidusax's Ruin",
        "Rain of Fire",
        "Scouring Black Flame",
        "Surge, O Flame!",
        "The Flame of Frenzy",
        "Theodorix's Magma",
        "Unendurable Frenzy",
        "Whirl, O Flame!"
    }

def get_lightning_damage_spells():
    """
    Get the list of spells that deal lightning damage.
    """
    return {
        # Incantations
        "Ancient Dragons' Lightning Spear",
        "Ancient Dragons' Lightning Strike",
        "Bayle's Flame Lightning",
        "Bayle's Tyranny",
        "Death Lightning",
        "Electrocharge",
        "Electrify Armament",
        "Frozen Lightning Spear",
        "Fortissax's Lightning Spear",
        "Honed Bolt",
        "Knight's Lightning Spear",
        "Lansseax's Glaive",
        "Lightning Spear",
        "Lightning Strike",
        "Placidusax's Ruin",
        "Vyke's Dragonbolt"
    }

def get_holy_damage_spells():
    """
    Get the list of spells that deal holy damage.
    """
    return {
        # Incantations
        "Aspects of the Crucible: Bloom",
        "Black Blade",
        "Discus of Light",
        "Elden Stars",
        "Giant Golden Arc",
        "Golden Arcs",
        "Land of Shadow",
        "Law of Causality",
        "Light of Miquella",
        "Litany of Proper Death",
        "Multilayered Ring of Light",
        "Radagon's Rings of Light",
        "Spira",
        "Triple Rings of Light",
        "Watchful Spirit",
        "Wrath from Afar",
        "Wrath of Gold",
        "Order's Blade"
    }

def get_physical_damage_spells():
    """
    Get the list of spells that deal physical damage.
    """
    return {
        # Sorceries - Gravity Sorceries
        "Blades of Stone",
        "Meteorite",
        "Meteorite of Astel",
        "Rock Sling",
        
        # Incantations - Bestial Incantations
        "Beast Claw",
        "Bestial Sling",
        "Gurranq's Beast Claw",
        "Stone of Gurranq",
        
        # Incantations - Blood Incantations
        "Swarm of Flies",
        
        # Incantations - Dragon Communion Incantations
        "Dragonclaw",
        "Dragonmaw",
        "Rotten Breath",
        "Ekzykes's Decay",
        "Greyoll's Roar",
        
        # Incantations - Erdtree Incantations
        "Aspects of the Crucible: Horns",
        "Aspects of the Crucible: Tail",
        "Aspects of the Crucible: Thorns",
        
        # Incantations - Frenzied Flame Incantations
        "Howl of Shabriri",
        
        # Incantations - Servants of Rot Incantations
        "Pest Threads",
        "Pest-Thread Spears",
        "Rotten Butterflies",
        "Scarlet Aeonia",
        
        # Incantations - Finger Sorceries
        "Cherishing Fingers",

        # Incantations - Spiral Tower
        "Roar of Rugalea",
        "Divine Beast Tornado",
        "Divine Bird Feathers",
    }

def get_magic_damage_incantations():
    """
    Get the list of incantations that deal magic damage.
    """
    return {
        "Borealis's Mist",
        "Dragonice",
        "Ghostflame Breath",
        "Glintstone Breath",
        "Smarag's Glintstone Breath"
    }

def get_magic_damage_sorcery_exceptions():
    """
    Get the list of sorceries that have magic bonuses but don't deal magic damage.
    """
    return {
        # Carian exceptions
        "Lucidity",
        "Miriam's Vanishing",
        
        # Finger exceptions
        "Cherishing Fingers",
        
        # Gravity exceptions
        "Rock Sling",
        "Blades of Stone",
        
        # Glintstone exceptions
        "Scholar's Shield",
        "Starlight",
        "Thops's Barrier",
        
        # Night exceptions
        "Night's Maiden Mist",
        "Unseen Blade",
        "Unseen Form"
    }

def get_magic_damage_sorcery_bonuses():
    """
    Get the list of bonus types that indicate magic damage for sorceries.
    """
    return {
        "Thorn",
        "Carian",
        "Oracle",
        "Crystalian",
        "Cold",
        "Death",
        "Finger",
        "Moon",
        "Gravity",
        "Glintstone",
        "Sellian"
    }

def get_damage_types(spell_name, spell_type, bonus):
    """
    Determine the damage types for a spell.
    Returns a dictionary with 'major' and 'minor' damage types.
    """
    fire_damage_spells = get_fire_damage_spells()
    lightning_damage_spells = get_lightning_damage_spells()
    holy_damage_spells = get_holy_damage_spells()
    physical_damage_spells = get_physical_damage_spells()
    magic_damage_incantations = get_magic_damage_incantations()
    magic_damage_sorcery_exceptions = get_magic_damage_sorcery_exceptions()
    magic_damage_sorcery_bonuses = get_magic_damage_sorcery_bonuses()
    
    damage_types = []
    
    if spell_name in fire_damage_spells:
        damage_types.append("Fire")
    
    if spell_name in lightning_damage_spells:
        damage_types.append("Lightning")
    
    if spell_name in holy_damage_spells:
        damage_types.append("Holy")
    
    if spell_name in physical_damage_spells:
        damage_types.append("Physical")
    
    # Check for magic damage
    if spell_name in magic_damage_incantations:
        damage_types.append("Magic")
    elif spell_type == "Sorcery" and bonus in magic_damage_sorcery_bonuses and spell_name not in magic_damage_sorcery_exceptions:
        damage_types.append("Magic")
    
    return damage_types

def check_status_buildup(spell_name):
    """
    Check if a spell has any status buildup.
    Returns the status type as a string, or "none" if no status.
    """
    blood_loss_spells = get_blood_loss_spells()
    poison_spells = get_poison_spells()
    scarlet_rot_spells = get_scarlet_rot_spells()
    frostbite_spells = get_frostbite_spells()
    madness_spells = get_madness_spells()
    
    if spell_name in blood_loss_spells:
        return "blood_loss"
    elif spell_name in poison_spells:
        return "poison"
    elif spell_name in scarlet_rot_spells:
        return "scarlet_rot"
    elif spell_name in frostbite_spells:
        return "frostbite"
    elif spell_name in madness_spells:
        return "madness"
    else:
        return "none"

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
    
def transform_spell_name(spell_name):
    """
    Transform the spell name to match the format of the wiki.gg link.
    """
    if (spell_name == "Land of Shadow (Incantation)"):
        return "Land of Shadow"
    if (spell_name == "Aspect of the Crucible: Horns"):
        return "Aspects of the Crucible: Horns"
    if (spell_name == "Aspect of the Crucible: Tail"):
        return "Aspects of the Crucible: Tail"
    if (spell_name == "Aspect of the Crucible: Thorns"):
        return "Aspects of the Crucible: Thorns"
    if (spell_name == "Aspect of the Crucible: Bloom"):
        return "Aspects of the Crucible: Bloom"
    if (spell_name == "Aspect of the Crucible: Breath"):
        return "Aspects of the Crucible: Breath"
    if (spell_name == "Aspects of the Crucible: Horns"):
        return "Aspects of the Crucible: Horns"
    if (spell_name == "Aspects of the Crucible: Tail"):
        return "Aspects of the Crucible: Tail"
    if (spell_name == "Aspects of the Crucible: Thorns"):
        return "Aspects of the Crucible: Thorns"
    if (spell_name == "Aspects of the Crucible: Bloom"):
        return "Aspects of the Crucible: Bloom"
    if (spell_name == "Aspects of the Crucible: Breath"):
        return "Aspects of the Crucible: Breath"
    if (spell_name == "Gurrang's Beast Claw"):
        return "Gurranq's Beast Claw"
    if (spell_name == "Flame, Grant me Strength"):
        return "Flame, Grant Me Strength"
    return spell_name

def transform_spell_name_for_image_url(spell_name):
    """
    Transform the spell name to match the format of the wiki.gg link.
    """
    if (spell_name == "Land of Shadow (Incantation)"):
        return "Land of Shadow"
    if (spell_name == "Aspect of the Crucible: Horns"):
        return "Aspects of the Crucible:Horns"
    if (spell_name == "Aspect of the Crucible: Tail"):
        return "Aspects of the Crucible:Tail"
    if (spell_name == "Aspect of the Crucible: Thorns"):
        return "Aspects of the Crucible:Thorns"
    if (spell_name == "Aspect of the Crucible: Bloom"):
        return "Aspects of the Crucible:Bloom"
    if (spell_name == "Aspect of the Crucible: Breath"):
        return "Aspects of the Crucible:Breath"
    if (spell_name == "Aspects of the Crucible: Horns"):
        return "Aspects of the Crucible:Horns"
    if (spell_name == "Aspects of the Crucible: Tail"):
        return "Aspects of the Crucible:Tail"
    if (spell_name == "Aspects of the Crucible: Thorns"):
        return "Aspects of the Crucible:Thorns"
    if (spell_name == "Aspects of the Crucible: Bloom"):
        return "Aspects of the Crucible:Bloom"
    if (spell_name == "Aspects of the Crucible: Breath"):
        return "Aspects of the Crucible:Breath"
    if (spell_name == "Gurrang's Beast Claw"):
        return "Gurranq's Beast Claw"
    if (spell_name == "Flame, Grant me Strength"):
        return "Flame, Grant Me Strength"
    return spell_name

def extract_image_urls_from_wiki_gg(html_content):
    """
    Extract image URLs from the wiki.gg spells page by matching spell names.
    Returns a dictionary mapping transformed spell names to their image URLs.
    """
    if not html_content:
        return {}
    
    soup = BeautifulSoup(html_content, 'html.parser')
    image_map = {}
    
    # Find all tables in the page
    tables = soup.find_all('table', class_='sortable wikitable')
    
    for table in tables:
        # Find the table body
        tbody = table.find('tbody')
        if not tbody:
            continue
        
        # Get all rows from the table body
        rows = tbody.find_all('tr')
        
        for row in rows:
            # Get all cells in the row
            cells = row.find_all(['td', 'th'])
            
            if len(cells) >= 2:  # Need at least 2 cells: icon and name
                # Get the first cell (icon with image)
                icon_cell = cells[0]
                
                # Get the second cell (spell name)
                name_cell = cells[1]
                
                # Handle line breaks in spell names (like "Aspects of the Crucible:<br />Bloom")
                # Replace <br> tags with spaces to get the full name
                for br in name_cell.find_all('br'):
                    br.replace_with(' ')
                
                spell_name = name_cell.get_text(strip=True)
                
                # Clean up extra spaces around colons (common in wiki.gg formatting)
                spell_name = spell_name.replace(' : ', ': ').replace(': ', ': ').replace(' :', ': ')
                transformed_spell_name = transform_spell_name_for_image_url(spell_name)
                
                # Look for image within the icon cell
                img = icon_cell.find('img')
                if img and spell_name:
                    src = img.get('src', '')
                    if src:
                        # Convert relative URLs to absolute URLs
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = 'https://eldenring.wiki.gg' + src
                        elif not src.startswith('http'):
                            src = 'https://eldenring.wiki.gg/' + src
                        
                        image_map[transformed_spell_name] = src
                        print(f"Found image for {transformed_spell_name}: {src}")
    
    return image_map

def extract_spells_from_table(html_content, image_map=None):
    """
    Extract spell names, types, and requirements from the table within the "tabcontent 1-tab" div.
    Looks for div with classes "tabcontent 1-tab", then "table-responsive", then table.
    Extracts spell names from the first cell, spell types from the second cell,
    and requirements from cells 6-8 (intelligence, faith, arcane).
    """
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the div with classes "tabcontent 1-tab"
    tab_content = soup.find('div', class_='tabcontent 1-tab')
    if not tab_content:
        print("No div with class 'tabcontent 1-tab' found")
        return None

    # Find the table-responsive div within the tab content
    table_responsive = tab_content.find('div', class_='table-responsive')
    if not table_responsive:
        print("No div with class 'table-responsive' found within tabcontent")
        return None
    
    # Find the table within table-responsive
    table = table_responsive.find('table')
    if not table:
        print("No table found within table-responsive div")
        return None
    
    # Find the table body
    tbody = table.find('tbody')
    if not tbody:
        print("No tbody found in the table")
        return None
    
    # Get all rows from the table body
    rows = tbody.find_all('tr')
    if not rows:
        print("No rows found in the table body")
        return None
    
    spells_data = []
    used_images = set()  # Track which images are used
    
    for i, row in enumerate(rows):
        # Get all cells in the row
        cells = row.find_all(['td', 'th'])
            
        if len(cells) == 11:  # Exactly 11 columns as specified
            # Get the first cell (spell name)
            first_cell = cells[0]
            spell_name = first_cell.get_text(strip=True)
            transformed_spell_name = transform_spell_name(spell_name)
            # Get the second cell (spell type)
            second_cell = cells[1]
            second_cell_text = second_cell.get_text(strip=True)
            if (second_cell_text == "Incantations"): # resolve inconsistency in the wiki
                second_cell_text = "Incantation"
            spell_type = second_cell_text
            
            # Get requirements from cells 6, 7, 8 (intelligence, faith, arcane)
            intelligence_cell = cells[5].get_text(strip=True)  # 6th cell (index 5)
            faith_cell = cells[6].get_text(strip=True)         # 7th cell (index 6)
            arcane_cell = cells[7].get_text(strip=True)        # 8th cell (index 7)
            
            # Get bonus from cell 10 (index 9)
            bonus_cell = cells[9]        # 10th cell (index 9)
            spell_bonus = bonus_cell.get_text(strip=True)
            
            # Get DLC status from cell 11 (index 10)
            dlc_cell = cells[10]          # 11th cell (index 10)
            dlc_text = dlc_cell.get_text(strip=True)
            is_dlc = dlc_text == "Shadow of the Erdtree DLC"
            
            # Extract numeric values, handling empty cells or non-numeric content
            def parse_requirement(cell_text):
                try:
                    # Remove any non-numeric characters and convert to int
                    cleaned = ''.join(filter(str.isdigit, cell_text))
                    return int(cleaned) if cleaned else 0
                except (ValueError, AttributeError):
                    return 0
            
            intelligence = parse_requirement(intelligence_cell)
            faith = parse_requirement(faith_cell)
            arcane = parse_requirement(arcane_cell)
            
            # Look for links within the first cell
            link = first_cell.find('a')
            wiki_fextralife_link = "https://eldenring.wiki.fextralife.com/" + link.get('href')
            
            # Construct wiki.gg link using established convention
            wiki_gg_link = f"https://eldenring.wiki.gg/wiki/{spell_name.replace(' ', '_').replace(':', '')}"

            # Get image URL from image map or use fallback
            image_url = None
            transformed_spell_name_for_image_url = transform_spell_name_for_image_url(transformed_spell_name)
            if image_map and transformed_spell_name_for_image_url in image_map:
                image_url = image_map[transformed_spell_name_for_image_url]
                used_images.add(transformed_spell_name_for_image_url)  # Mark as used
                # Remove from image map to avoid duplicates
                del image_map[transformed_spell_name_for_image_url]
            else:
                # Fallback to hardcoded URL if not found in image map
                url_name = transformed_spell_name_for_image_url.replace(' ', '_').replace(':', '')
                image_url = f"https://eldenring.wiki.gg/images/thumb/0/08/ER_Icon_Spell_{url_name}.png/300px-ER_Icon_Spell_{url_name}.png"
                print(f"Warning: No image found for {transformed_spell_name}, using fallback URL")
            
            spell_data = {
                'spell_name': transformed_spell_name,
                'spell_type': spell_type,
                'requirements': {
                    'intelligence': intelligence,
                    'faith': faith,
                    'arcane': arcane
                },
                'bonus': spell_bonus,
                'dlc_exclusive': is_dlc,
                'damage_types': get_damage_types(transformed_spell_name, spell_type, spell_bonus),
                'status_buildup': check_status_buildup(transformed_spell_name),
                'wikiGGLink': wiki_gg_link,
                'wikiFextralifeLink': wiki_fextralife_link,
                'imageUrl': image_url
            }
            
            spells_data.append(spell_data)
            dlc_status = "DLC" if is_dlc else "Base Game"
            print(f"Found spell {i + 1}: {spell_name} ({spell_type}) - INT:{intelligence} FTH:{faith} ARC:{arcane} Bonus:{spell_bonus} {dlc_status}")
        else:
            # Skip rows that don't have exactly 11 columns
            print(f"Skipping row {i + 1}: Expected 11 columns, found {len(cells)}")
    
    # Print unused images for troubleshooting
    if image_map:
        print(f"\n=== UNUSED IMAGE URLS ({len(image_map)} total) ===")
        for spell_name, image_url in sorted(image_map.items()):
            print(f"Unused: {spell_name} -> {image_url}")
        print("=== END UNUSED IMAGE URLS ===\n")
    
    return spells_data

def save_spells_by_type(spells_data):
    """
    Save spells data to separate JSON files based on spell type.
    """
    if not spells_data:
        print("No spells data to save")
        return False

    # Group spells by type
    spells_by_type = {}
    
    for spell in spells_data:
        spell_type = spell['spell_type']
        if spell_type not in spells_by_type:
            spells_by_type[spell_type] = []
        spells_by_type[spell_type].append(spell)
    
    # Save each type to a separate file
    for spell_type, spells in spells_by_type.items():
        # Create a safe filename from the spell type
        safe_type_name = spell_type.lower().replace(' ', '_').replace('-', '_').replace('/', '_')
        filename = f"spells_{safe_type_name}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(spells, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(spells)} spells of type '{spell_type}' to: {filename}")
        except Exception as e:
            print(f"Error saving spells data for type '{spell_type}': {e}")
            return False
    
    # Also save a combined file with all spells
    try:
        with open('all_spells_data.json', 'w', encoding='utf-8') as f:
            json.dump(spells_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved combined data with {len(spells_data)} total spells to: all_spells_data.json")
    except Exception as e:
        print(f"Error saving combined spells data: {e}")
        return False
    
    return True

def main():
    """
    Main function to fetch the Spells page HTML and extract spell data from the table.
    """
    # Try to read from local file first
    html_content = read_local_html('spells_page.html')
    if not html_content:
        print("Local spells_page.html not found. Please download the spells page first.")
        return
    
    print("Using local spells_page.html file")
    print(f"Successfully read HTML content ({len(html_content)} characters)")
    
    # Read wiki.gg spells page for image URLs
    wiki_gg_html_content = read_local_html('wiki_gg_spells_page.html')
    image_map = {}
    if wiki_gg_html_content:
        print("Reading wiki.gg spells page for image URLs...")
        image_map = extract_image_urls_from_wiki_gg(wiki_gg_html_content)
        print(f"Found {len(image_map)} image URLs from wiki.gg page")
    else:
        print("Warning: wiki_gg_spells_page.html not found, will use fallback image URLs")
    
    # Extract spells from the table
    spells_data = extract_spells_from_table(html_content, image_map)
    
    if spells_data:
        # Save spells data by type
        save_spells_by_type(spells_data)
        
        # Print summary
        print(f"\n=== Spells Summary ===")
        print(f"Found {len(spells_data)} total spells in the table")
        
        # Group by type for summary
        spells_by_type = {}
        for spell in spells_data:
            spell_type = spell['spell_type']
            if spell_type not in spells_by_type:
                spells_by_type[spell_type] = []
            spells_by_type[spell_type].append(spell)
        
        print(f"\nSpells by type:")
        for spell_type, spells in spells_by_type.items():
            print(f"  - {spell_type}: {len(spells)} spells")
        
        # Show first few spells as examples
        print(f"\nFirst few spells:")
        for i, spell in enumerate(spells_data[:5]):
            print(f"  - Spell {i + 1}: {spell['spell_name']} ({spell['spell_type']})")
            if spell['wikiFextralifeLink']:
                print(f"    Link: {spell['wikiFextralifeLink']}")
        
        if len(spells_data) > 5:
            print(f"  ... and {len(spells_data) - 5} more spells")
        else:
            print("No spells data found")

if __name__ == "__main__":
    main()
