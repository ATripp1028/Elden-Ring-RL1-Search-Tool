import weaponsThrustingShields from '../resources/weapons_thrusting_shields.json'
import weaponsGreatshields from '../resources/weapons_greatshields.json'
import weaponsMediumShields from '../resources/weapons_medium_shields.json'
import weaponsSmallShields from '../resources/weapons_small_shields.json'
import weaponsTorches from '../resources/weapons_torches.json'
import weaponsSacredSeals from '../resources/weapons_sacred_seals.json'
import weaponsStaves from '../resources/weapons_staves.json'
import weaponsBallista from '../resources/weapons_ballista.json'
import weaponsCrossbows from '../resources/weapons_crossbows.json'
import weaponsGreatbows from '../resources/weapons_greatbows.json'
import weaponsBows from '../resources/weapons_bows.json'
import weaponsLightBows from '../resources/weapons_light_bows.json'
import weaponsPerfumeBottles from '../resources/weapons_perfume_bottles.json'
import weaponsBeastClaws from '../resources/weapons_beast_claws.json'
import weaponsClaws from '../resources/weapons_claws.json'
import weaponsHandToHand from '../resources/weapons_hand_to_hand.json'
import weaponsFists from '../resources/weapons_fists.json'
import weaponsWhips from '../resources/weapons_whips.json'
import weaponsReapers from '../resources/weapons_reapers.json'
import weaponsHalberds from '../resources/weapons_halberds.json'
import weaponsGreatSpears from '../resources/weapons_great_spears.json'
import weaponsSpears from '../resources/weapons_spears.json'
import weaponsColossalWeapons from '../resources/weapons_colossal_weapons.json'
import weaponsGreatHammers from '../resources/weapons_great_hammers.json'
import weaponsFlails from '../resources/weapons_flails.json'
import weaponsHammers from '../resources/weapons_hammers.json'
import weaponsGreataxes from '../resources/weapons_greataxes.json'
import weaponsAxes from '../resources/weapons_axes.json'
import weaponsTwinblades from '../resources/weapons_twinblades.json'
import weaponsGreatKatanas from '../resources/weapons_great_katanas.json'
import weaponsKatanas from '../resources/weapons_katanas.json'
import weaponsBackhandBlades from '../resources/weapons_backhand_blades.json'
import weaponsCurvedGreatswords from '../resources/weapons_curved_greatswords.json'
import weaponsCurvedSwords from '../resources/weapons_curved_swords.json'
import weaponsHeavyThrustingSwords from '../resources/weapons_heavy_thrusting_swords.json'
import weaponsThrustingSwords from '../resources/weapons_thrusting_swords.json'
import weaponsColossalSwords from '../resources/weapons_colossal_swords.json'
import weaponsGreatswords from '../resources/weapons_greatswords.json'
import weaponsLightGreatswords from '../resources/weapons_light_greatswords.json'
import weaponsStraightSwords from '../resources/weapons_straight_swords.json'
import weaponsDaggers from '../resources/weapons_daggers.json'
import weaponsThrowingBlades from '../resources/weapons_throwing_blades.json'
import type { Weapon } from '../model/types'

/**
 * Loads and returns all weapon data from JSON files
 */
export const loadWeaponsData = (): Weapon[][] => {
  return [
    weaponsThrustingShields,
    weaponsGreatshields,
    weaponsMediumShields,
    weaponsSmallShields,
    weaponsTorches,
    weaponsSacredSeals,
    weaponsStaves,
    weaponsBallista,
    weaponsCrossbows,
    weaponsGreatbows,
    weaponsBows,
    weaponsLightBows,
    weaponsPerfumeBottles,
    weaponsBeastClaws,
    weaponsClaws,
    weaponsHandToHand,
    weaponsFists,
    weaponsWhips,
    weaponsReapers,
    weaponsHalberds,
    weaponsGreatSpears,
    weaponsSpears,
    weaponsColossalWeapons,
    weaponsGreatHammers,
    weaponsFlails,
    weaponsHammers,
    weaponsGreataxes,
    weaponsAxes,
    weaponsTwinblades,
    weaponsGreatKatanas,
    weaponsKatanas,
    weaponsBackhandBlades,
    weaponsCurvedGreatswords,
    weaponsCurvedSwords,
    weaponsHeavyThrustingSwords,
    weaponsThrustingSwords,
    weaponsColossalSwords,
    weaponsGreatswords,
    weaponsLightGreatswords,
    weaponsStraightSwords,
    weaponsDaggers,
    weaponsThrowingBlades,
  ] as Weapon[][]
}
