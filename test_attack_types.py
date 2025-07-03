#!/usr/bin/env python3
"""
Test script to verify the updated get_attack_types function.
"""

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

def test_attack_types():
    """Test the get_attack_types function with various weapon types."""
    
    # Test cases for Staves and Sacred Seals
    spell_weapons = [
        ("Academy Glintstone Staff", "Staves"),
        ("Carian Glintblade Staff", "Staves"),
        ("Carian Regal Scepter", "Staves"),
        ("Crystal Staff", "Staves"),
        ("Demi-Human Queen's Staff", "Staves"),
        ("Digger's Staff", "Staves"),
        ("Gelmir Glintstone Staff", "Staves"),
        ("Glintstone Staff", "Staves"),
        ("Lusat's Glintstone Staff", "Staves"),
        ("Meteorite Staff", "Staves"),
        ("Prince of Death's Staff", "Staves"),
        ("Rotten Crystal Staff", "Staves"),
        ("Staff of Loss", "Staves"),
        ("Staff of the Guilty", "Staves"),
        ("Staff of the Avatar", "Staves"),
        ("Terra Magicus", "Staves"),
        ("Azur's Glintstone Staff", "Staves"),
        ("Albinauric Staff", "Staves"),
        ("Carian Glintstone Staff", "Staves"),
        ("Staff of the Guilty", "Staves"),
        ("Clawmark Seal", "Sacred Seals"),
        ("Dragon Communion Seal", "Sacred Seals"),
        ("Erdtree Seal", "Sacred Seals"),
        ("Finger Seal", "Sacred Seals"),
        ("Frenzied Flame Seal", "Sacred Seals"),
        ("Giant's Seal", "Sacred Seals"),
        ("Godslayer's Seal", "Sacred Seals"),
        ("Golden Order Seal", "Sacred Seals"),
        ("Gravel Stone Seal", "Sacred Seals"),
        ("Two Fingers Heirloom", "Sacred Seals")
    ]
    
    print("Testing Staves and Sacred Seals (should return 'Spell'):")
    print("=" * 60)
    
    for weapon_name, weapon_type in spell_weapons:
        result = get_attack_types(weapon_name, weapon_type)
        print(f"{weapon_name} ({weapon_type}):")
        print(f"  Primary: {result['primary']}")
        print(f"  Secondary: {result['secondary']}")
        print()
    
    # Test a few other weapon types to make sure they still work correctly
    other_weapons = [
        ("Dagger", "Daggers"),
        ("Longsword", "Straight Swords"),
        ("Greatsword", "Greatswords"),
        ("Uchigatana", "Katanas"),
        ("Morning Star", "Hammers")
    ]
    
    print("Testing other weapon types (should return appropriate attack types):")
    print("=" * 60)
    
    for weapon_name, weapon_type in other_weapons:
        result = get_attack_types(weapon_name, weapon_type)
        print(f"{weapon_name} ({weapon_type}):")
        print(f"  Primary: {result['primary']}")
        print(f"  Secondary: {result['secondary']}")
        print()

if __name__ == "__main__":
    test_attack_types() 