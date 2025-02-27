class inscription_weapon_brilliance:
    def __init__(self,character):
        self.name='卓9'
        character.attribute['special_points_consume_rate'] /=1.3 #卓越4
        skill=character.skill_item.get('55',None)
        self.work_indicator9=False #卓越9 14附加指示器
        self.work_indicator7=False #卓越7 10伤害指示器
        self.work_indicator_rate=False #2800倍率指示器
        self.left_time9=0
        self.left_time7=0
        self.cool_time7=0
        self.extra_cnt=0
        for key,item in character.skill_item.items():
            if hasattr(item,'add_level'):
                item.add_level=item.add_level+1
        if skill is not None:
            skill.inde_rate+=45
            skill.cost/=1.3
    
    def effect(self, character,skill=None):
        
        if 'strength' in character.condition and not self.work_indicator9:
            character.attribute['additional_damage']+=14
            self.left_time9=20
            self.work_indicator9=True
        elif 'strength' in character.condition and self.work_indicator9:
            self.left_time9=20
        
        
        if skill is not None:
            if 'strength' in character.condition:
                    self.extra_cnt+=skill.hit_cnt_ex
                    
            if self.extra_cnt >=5 and self.cool_time7>0:
                self.extra_cnt=0
                
            if self.extra_cnt >= 5 and self.cool_time7==0:
                self.work_indicator_rate=True
                self.work_indicator7=True
                self.cool_time7=5
                self.extra_cnt=0
                skill.base_rate+=2800
                if self.left_time7 == 0:
                    character.attribute['final_damage']+=8
                    self.left_time7 = 10
                else:
                    self.left_time7 = 10
            
    
        #################
        # 冷却独立处理
        interval=character.intervals['time_interval']['present']
        if self.left_time7 > interval:
            self.left_time7 -= interval
        else:
            self.left_time7 = 0

        if self.left_time9 > interval:
            self.left_time9 -= interval
        else:
            self.left_time9 = 0

        if self.cool_time7 > interval:
            self.cool_time7-= interval
        else:
            self.cool_time7 = 0
        ################

    def close(self,character,skill=None):
        
        if self.work_indicator_rate and skill is not None:
            skill.base_rate-=2800
            self.work_indicator_rate=False
        
        if self.left_time9==0 and self.work_indicator9:
                character.attribute['additional_damage']-=14
                self.work_indicator9=False
        if self.left_time7==0:
            if self.work_indicator7:
                character.attribute['final_damage']-=8
                self.work_indicator7=False

        


class inscription_weapon_stable:
    def __init__(self,character):
        self.name='不破8'
        character.attribute['condition_damage']+=32
        

class inscription_weapon_bitter_hit:
    def __init__(self,character):
        self.name='痛击4'
        character.attribute['crit_rate']+=4
        character.attribute['crit_damage']+=8

