class inscription_jewelry_element_master:
    def __init__(self, character):
        self.name="属性9"
        character.attribute['element_strength'] +=26
        character.attribute['element_damage'] +=7


class inscription_jewelry_element_endurance:
    def __init__(self, character):
        self.name="耐力9"
        character.attribute['element_resistance'] +=35
        character.attribute['element_damage'] +=10
        character.attribute['element_strength'] +=10

class inscription_jewelry_challenger:
    def __init__(self, character):
        self.name="挑战3"
        character.attribute['boss_damage'] +=3