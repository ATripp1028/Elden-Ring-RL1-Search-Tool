export interface Weapon {
    name: string;
    type: WeaponType;
    imgPath: string;
    stats: {
        strength: number;
        dexterity: number;
        intelligence: number;
        faith: number;
        arcane: number;
    }
    wikiGGLink?: string;
    wikiFextralifeLink: string;
    dlcExclusive: boolean;
}

export enum WeaponType {
    Dagger = "Dagger",
    ThrowingBlade = "Throwing Blade",
    StraightSword = "Straight Sword",
    LightGreatsword = "Light Greatsword",
    Greatsword = "Greatsword",
    ColossalSword = "Colossal Sword",
    ThrustingSword = "Thrusting Sword",
    HeavyThrustingSword = "Heavy Thrusting Sword",
    CurvedSword = "Curved Sword",
    CurvedGreatsword = "Curved Greatsword",
    BackhandBlade = "Backhand Blade",
    Katana = "Katana",
    GreatKatana = "Great Katana",
    Twinblade = "Twinblade",
    Axe = "Axe",
    GreatAxe = "Great Axe",
    Hammer = "Hammer",
    Flail = "Flail",
    GreatHammer = "Great Hammer",
    ColossalWeapon = "Colossal Weapon",
    Spear = "Spear",
    GreatSpear = "Great Spear",
    Halberd = "Halberd",
    Reaper = "Reaper",
    Whip = "Whip",
    Fist = "Fist",
    HandToHand = "Hand-to-Hand",
    Claws = "Claws",
    BeastClaws = "Beast Claws",
    PerfumeBottle = "Perfume Bottle",
    LightBow = "Light Bow",
    Bow = "Bow",
    GreatBow = "Great Bow",
    Crossbow = "Crossbow",
    Ballista = "Ballista",
    Stave = "Stave",
    SacredSeal = "Sacred Seal",
    Torch = "Torch",
    SmallShield = "Small Shield",
    MediumShield = "Medium Shield",
    GreatShield = "Great Shield",
    ThrustingShield = "Thrusting Shield",
}