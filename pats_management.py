from pats_skill_bird import bird
from pats_skill_cat import cat

pats={
    '鸟': bird,
    '猫':cat
}

class pats_management:
    def __init__(self,character):
        for key,item in character.toequip.items():
            if key in ['pat1', 'pat2']:
                for name,strength in item.items():
                    pats_class=pats[name](name,character.attribute,strength)
                    character.pats_skill_item[key]=pats_class
    
    def effect(self,character):
        for pats_name,pats_skill_item in character.pats_skill_item.items():
            if hasattr(pats_skill_item,'effect'):
                pats_skill_item.effect(character)
    
    def close(self,character):
        for pats_name,pats_skill_item in character.pats_skill_item.items():
            if hasattr(pats_skill_item,'close'):
                pats_skill_item.close()
