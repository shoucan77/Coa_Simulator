from skill import pats_skill
from skill import mapping_for_strength

class cat(pats_skill):
    def __init__(self, name: str, attribute: dict,strength: dict):
        '''
        例如 strength={
                    'power':'pink',
                    'skill':'purple',
                    'speed':'purple'
                    }
        '''
        super().__init__(name, attribute)
        self.self_attribute = {'strength':333.0,'atk':88.0,'crit_rate':6.0}
        self.max_cnt=5
        self.present_cnt=0
        self.present_cooltime = 0  # 当前冷却时间
        self.max_cooltime=60 #最大冷却时间
        self.max_lefttime=10 #buff 最大剩余时间
        self.present_lefttime=0 #buff当前剩余时间
        self.passive_skill_attribute_perlevel = {'element_strength':2}
        self.passive_skill_attribute = {'element_strength':15}
        self.passive_add_level=0
        self.work_indicator=False
        self.effect_strength(strength=strength)
    
    def effect(self,character):
        if 'cat' not in character.buff:
            character.buff['cat'] = {
                'cool_time': 4
            }
        
        if character.buff['cat']['cool_time']==0:
            max_cool=0
            name=None
            for skillname,skill in character.skill_item.items():
                if hasattr(skill,'present_cooltime') and skillname not in ['s1', 's2', 'minis']:
                    if skill.present_cooltime>=max_cool:
                        max_cool=skill.present_cooltime
                        name=skillname
            
            character.skill_item[name].present_cooltime=0
            character.buff['cat']['cool_time']=40
            
        #################
        # 冷却独立处理
        interval=character.intervals['time_interval']['present']
        if self.present_lefttime > interval:
            self.present_lefttime -= interval
        else:
            self.present_lefttime = 0

        if self.present_cooltime > interval:
            self.present_cooltime  -= interval
        else:
            self.present_cooltime=0

        if self.present_lefttime==0:
            self.work_indicator=False
        ################
        
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            if not self.work_indicator:
                return
            else:
                if self.present_cnt>0:
                    for key,skill in character.skill_item.items():
                        if self.present_cnt>0:
                            if key in ['A1', 'A2', 'A3', 'A4','break']:
                                continue
                            if skill.present_cooltime>4:
                                skill.present_cooltime-=4
                            else:
                                skill.present_cooltime=0
                    self.present_cnt-=1
                if self.present_cnt==0:
                    self.work_indicator=False

    def effect_strength(self,strength:dict):
        #处理魂印的常驻属性 被动技能属性
        for key,value in strength.items():
            dicts=mapping_for_strength[key][value]
            self.dict_add(self.attribute,dicts)


         #处理力魂印
        power=strength.get('power',None)
        if power is not None:
            if power == 'cat':
                for key,value in self.self_attribute.items():
                    self.self_attribute[key] *=1.2
            else:
                for key,value in self.self_attribute.items():
                    self.self_attribute[key] *=1.1
        self.dict_add(self.attribute,self.self_attribute)
        
        #处理技魂印
        skill=strength.get('skill',None)
        if skill is not None:
            self.passive_add_level+=1
        
        for key,value in self.passive_skill_attribute.items():
            value += self.passive_skill_attribute_perlevel[key]*self.passive_add_level
        
        #被动生效
        self.dict_add(self.attribute,self.passive_skill_attribute)
        
        #处理速魂印
        speed=strength.get('speed',None)
        if speed is not None:
            if speed == 'pink':
                self.max_cooltime *= 0.9
            else:
                self.max_cooltime *= 0.9
                
    def use(self):
        self.present_cooltime=self.max_cooltime
        self.present_cnt=self.max_cnt
        self.work_indicator=True
        self.present_lefttime=self.max_lefttime