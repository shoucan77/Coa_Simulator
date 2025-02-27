from inscription_armor import inscription_armor_high_order_skill,inscription_armor_outstanding,inscription_armor_quench
from inscription_weapon import inscription_weapon_bitter_hit,inscription_weapon_brilliance,inscription_weapon_stable
from inscription_jewelry import inscription_jewelry_challenger,inscription_jewelry_element_endurance,inscription_jewelry_element_master
from inscription_protective_clothes import inscription_protective_clothes_adapt,inscription_protective_clothes_aloof,inscription_protective_clothes_destroy,inscription_protective_clothes_quick
import json
import inspect
mapping={
    "卓9":inscription_weapon_brilliance,
    "不破8":inscription_weapon_stable,
    "痛击4":inscription_weapon_bitter_hit,
    "不凡6":inscription_armor_outstanding,
    "高阶6":inscription_armor_high_order_skill,
    "淬火2":inscription_armor_quench,
    "属性9":inscription_jewelry_element_master,
    "耐力9":inscription_jewelry_element_endurance,
    "挑战3":inscription_jewelry_challenger,
    "破坏9":inscription_protective_clothes_destroy,
    "超然9":inscription_protective_clothes_aloof,
    "适应9":inscription_protective_clothes_adapt,
    "迅捷3":inscription_protective_clothes_quick
}

class inscription_manager:
    def __init__(self, character):
        with open('inscription.json','r',encoding='utf-8-sig') as file:
            inscription_list= json.load(file)
        for key,value in inscription_list.items():
            for key2,value2 in value.items():
                if value2 in mapping:
                    classes=mapping[value2](character)
                    character.inscription[value2]=classes
    
    def management(self,character,skill=None):
        for key,value in character.inscription.items():
            if hasattr(value,'effect'):
                argspec = inspect.getfullargspec(value.effect)
                if 'skill' in argspec.args:
                    value.effect(character,skill)
                else:
                    value.effect(character)
    
    def close(self, character,skill=None):
        for key,value in character.inscription.items():
            if hasattr(value,'close'):
                if 'skill' in inspect.getfullargspec(value.close).args:
                    value.close(character,skill)
                else:
                    value.close(character)