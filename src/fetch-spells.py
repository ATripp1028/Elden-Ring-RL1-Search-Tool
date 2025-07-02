#!/usr/bin/env python3
"""
Script to fetch HTML content from Elden Ring wiki pages for spells.
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
        "Burn O Flame!",
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
        "O Flame!",
        "Placidusax's Ruin",
        "Rain of Fire",
        "Scouring Black Flame",
        "Surge O Flame!",
        "The Flame of Frenzy",
        "Theodorix's Magma",
        "Unendurable Frenzy",
        "Whirl O Flame!"
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
        "Wrath of Gold"
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
        
        # Incantations - Frenzied Flame Incantations
        "Howl of Shabriri",
        
        # Incantations - Servants of Rot Incantations
        "Pest Threads",
        "Scarlet Aeonia",
        
        # Incantations - Finger Sorceries
        "Cherishing Fingers"
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
        "Full Moon",
        "Gravity",
        "Glintstone",
        "Night"
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
    elif spell_type == "Sorceries" and bonus in magic_damage_sorcery_bonuses and spell_name not in magic_damage_sorcery_exceptions:
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
    
def extract_spells_from_table(html_content):
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
    
    for i, row in enumerate(rows):
        # Get all cells in the row
        cells = row.find_all(['td', 'th'])
            
        if len(cells) >= 12:  # Need at least 12 cells for all data including DLC status
            # Get the first cell (spell name)
            first_cell = cells[0]
            spell_name = first_cell.get_text(strip=True)
            
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
            
            # Get bonus from cell 11 (index 10)
            bonus_cell = cells[10]        # 11th cell (index 10)
            spell_bonus = bonus_cell.get_text(strip=True)
            
            # Get DLC status from cell 12 (index 11)
            dlc_cell = cells[11]          # 12th cell (index 11)
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
            
            intelligence = parse_requirement(intelligence_cell.get_text(strip=True))
            faith = parse_requirement(faith_cell.get_text(strip=True))
            arcane = parse_requirement(arcane_cell.get_text(strip=True))
            
            # Look for links within the first cell
            links = first_cell.find_all('a')
            spell_links = []
            wiki_fextralife_link = None
            
            for link in links:
                link_info = {
                    'text': link.get_text(strip=True),
                    'href': link.get('href', ''),
                    'title': link.get('title', '')
                }
                spell_links.append(link_info)
                
                # Check if this is a Fextralife link
                if 'fextralife.com' in link.get('href', ''):
                    wiki_fextralife_link = link.get('href')
            
            # Construct wiki.gg link using established convention
            wiki_gg_link = f"https://eldenring.wiki.gg/wiki/{spell_name.replace(' ', '_')}"
            
            spell_data = {
                'index': i,
                'spell_name': spell_name,
                'spell_type': spell_type,
                'requirements': {
                    'intelligence': intelligence,
                    'faith': faith,
                    'arcane': arcane
                },
                'bonus': spell_bonus,
                'dlc_exclusive': is_dlc,
                'damage_types': get_damage_types(spell_name, spell_type, spell_bonus),
                'status_buildup': check_status_buildup(spell_name),
                'wikiGGLink': wiki_gg_link,
                'wikiFextralifeLink': wiki_fextralife_link,
                'links': spell_links
            }
            
            spells_data.append(spell_data)
            dlc_status = "DLC" if is_dlc else "Base Game"
            print(f"Found spell {i + 1}: {spell_name} ({spell_type}) - INT:{intelligence} FTH:{faith} ARC:{arcane} Bonus:{spell_bonus} {dlc_status}")
        elif len(cells) >= 11:  # Need at least 11 cells for bonus but missing DLC status
            # Get the first cell (spell name)
            first_cell = cells[0]
            spell_name = first_cell.get_text(strip=True)
            
            # Get the second cell (spell type)
            second_cell = cells[1]
            spell_type = second_cell.get_text(strip=True)
            
            # Get requirements from cells 6, 7, 8 (intelligence, faith, arcane)
            intelligence_cell = cells[5]  # 6th cell (index 5)
            faith_cell = cells[6]         # 7th cell (index 6)
            arcane_cell = cells[7]        # 8th cell (index 7)
            
            # Get bonus from cell 11 (index 10)
            bonus_cell = cells[10]        # 11th cell (index 10)
            spell_bonus = bonus_cell.get_text(strip=True)
            
            # Extract numeric values, handling empty cells or non-numeric content
            def parse_requirement(cell_text):
                try:
                    # Remove any non-numeric characters and convert to int
                    cleaned = ''.join(filter(str.isdigit, cell_text))
                    return int(cleaned) if cleaned else 0
                except (ValueError, AttributeError):
                    return 0
            
            intelligence = parse_requirement(intelligence_cell.get_text(strip=True))
            faith = parse_requirement(faith_cell.get_text(strip=True))
            arcane = parse_requirement(arcane_cell.get_text(strip=True))
            
            # Look for links within the first cell
            links = first_cell.find_all('a')
            spell_links = []
            wiki_fextralife_link = None
            
            for link in links:
                link_info = {
                    'text': link.get_text(strip=True),
                    'href': link.get('href', ''),
                    'title': link.get('title', '')
                }
                spell_links.append(link_info)
                
                # Check if this is a Fextralife link
                if 'fextralife.com' in link.get('href', ''):
                    wiki_fextralife_link = link.get('href')
            
            # Construct wiki.gg link using established convention
            wiki_gg_link = f"https://eldenring.wiki.gg/wiki/{spell_name.replace(' ', '_')}"
            
            spell_data = {
                'index': i,
                'spell_name': spell_name,
                'spell_type': spell_type,
                'requirements': {
                    'intelligence': intelligence,
                    'faith': faith,
                    'arcane': arcane
                },
                'bonus': spell_bonus,
                'dlc_exclusive': None,
                'damage_types': get_damage_types(spell_name, spell_type, spell_bonus),
                'status_buildup': check_status_buildup(spell_name),
                'wikiGGLink': wiki_gg_link,
                'wikiFextralifeLink': wiki_fextralife_link,
                'links': spell_links
            }
            
            spells_data.append(spell_data)
            print(f"Found spell {i + 1}: {spell_name} ({spell_type}) - INT:{intelligence} FTH:{faith} ARC:{arcane} Bonus:{spell_bonus} DLC:Not available")
    
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
    
    # Extract spells from the table
    spells_data = extract_spells_from_table(html_content)
    
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
            if spell['links']:
                for link in spell['links']:
                    print(f"    Link: {link['text']} -> {link['href']}")
        
        if len(spells_data) > 5:
            print(f"  ... and {len(spells_data) - 5} more spells")
        else:
            print("No spells data found")

if __name__ == "__main__":
    main()
