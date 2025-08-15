import type { Spell } from '../model/types'
import spellsSorcery from '../resources/spells_sorcery.json'
import spellsIncantation from '../resources/spells_incantation.json'

export function loadSpellsData(): Spell[] {
  return [
    ...(spellsSorcery as Spell[]),
    ...(spellsIncantation as Spell[])
  ]
}
