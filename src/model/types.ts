export interface Weapon {
    weapon_name: string,
    weapon_type: string,
    wikiGGLink: string,
    wikiFextralifeLink: string,
    attributes: Attributes,
    damage_types: DamageTypes,
    attack_types: AttackTypes,
    status_buildup: string,
    image: Image,
    dlc_exclusive: boolean
}

export interface Attributes {
  strength: Strength,
  dexterity: number,
  intelligence: number,
  faith: number,
  arcane: number
}

export interface DamageTypes {
  major: DamageType,
  minor: DamageType[]
}

export interface Strength {
  one_hand: number,
  two_hand: number
}

export interface AttackTypes {
  primary: AttackType,
  secondary: AttackType
}

export interface Image {
  src: string,
  alt: string,
  title: string
}

export enum AttackType {
  Standard = "Standard",
  Slash = "Slash",
  Strike = "Strike",
  Piercing = "Pierce",
}

export enum DamageType {
  Physical = "Physical",
  Fire = "Fire",
  Lightning = "Lightning",
  Holy = "Holy",
  Magic = "Magic",
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
