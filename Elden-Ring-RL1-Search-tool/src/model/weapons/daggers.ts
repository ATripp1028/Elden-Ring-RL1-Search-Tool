import { type Weapon, WeaponType } from "../types";

export const daggers: Weapon[] = [
    {
        name: "Dagger",
        type: WeaponType.Dagger,
        imgPath: "weapons/daggers/dagger.webp",
        stats: {
            strength: 5,
            dexterity: 9,
            intelligence: 0,
            faith: 0,
            arcane: 0,
        },
        wikiGGLink: "https://eldenring.wiki.gg/wiki/Dagger",
        wikiFextralifeLink: "https://eldenring.wiki.fextralife.com/Dagger",
        dlcExclusive: false,
    },
    {
        name: "Parrying Dagger",
        type: WeaponType.Dagger,
        imgPath: "weapons/daggers/parrying_dagger.webp",
        stats: {
            strength: 5,
            dexterity: 14,
            intelligence: 0,
            faith: 0,
            arcane: 0,
        },
        wikiGGLink: "https://eldenring.wiki.gg/wiki/Parrying_Dagger",
        wikiFextralifeLink: "https://eldenring.wiki.fextralife.com/Parrying+Dagger",
        dlcExclusive: false,
    }
];