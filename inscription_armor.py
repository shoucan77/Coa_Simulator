class inscription_armor_outstanding:
    def __init__(self,character):
        self.name="不凡6"
        skill1=character.skill_item.get("55",None)
        if skill1 is not None:
            skill1.extra_cool_rate+=33
            skill1.inde_rate+=35
        
        skill2=character.skill_item.get("s1",None)
        if skill2 is not None:
            skill2.extra_rate+=10
            skill2.extra_cool_rate+=5
            
        skill3=character.skill_item.get("s2",None)
        if skill3 is not None:
            skill3.extra_rate+=10
            skill3.extra_cool_rate+=5
            
        character.attribute['special_points_max']*=1.5
        character.attribute['present_special_points']=character.attribute['special_points_max']
        character.attribute['special_points_charge_rate']*=1.6
        character.buff['passive_stab']['independent_damage_per_layer']+=1.4
        
        for key,value in character.skill_item.items():
            if hasattr(value,'ex_base_rate'):
                if value.hit_cnt_ex!=0:
                    value.ex_base_rate*=1.66
            if hasattr(value,'rate_per_level_ex'):
                if value.hit_cnt_ex!=0:
                    value.rate_per_level_ex*=1.66

class inscription_armor_high_order_skill:
    def __init__(self,character):
        self.name="高阶6"
        add_rate_list=[str(x*5) for x in range(7,15)]
        add_level_list=add_rate_list+['s1', 's2']
        for key,value in character.skill_item.items():
            if key in add_level_list:
                value.add_level=value.add_level+2
        
        for key,value in character.skill_item.items():
            if key in add_rate_list:
                value.extra_rate+=20
                
class inscription_armor_quench:
    def __init__(self, character):
        self.name="淬火2"
        character.attribute['additional_damage']+=3