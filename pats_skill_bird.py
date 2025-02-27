from skill import pats_skill
from skill import mapping_for_strength
class bird(pats_skill):
    def __init__(self, name: str, attribute: dict,strength: dict):
        '''
        例如 strength={
                    'power':'pink,
                    'skill':'purple',
                    'speed':'purple'
                    }
        '''
        super().__init__(name, attribute)
        self.self_attribute = {'strength':345.0,'boos_damage':10.0,'hp_rate':6.8}
        self.current_shape = 1  # 当前技能形态 (1或2)
        self.max_cnt=6
        self.present_cnt=0
        self.present_cooltime = 0  # 当前冷却时间
        self.cooltime=[0,15]  #记录两个的冷却时间
        self.max_cooltime=[45.0,15.0] #对应技能1和技能2的最大冷却时间 注意外部接口调用减冷却时 冷却为列表的情况
        self.max_lefttime=8 #buff 最大剩余时间
        self.present_lefttime=0 #buff当前剩余时间
        self.active_skill_attribute_perlevel = {'additional_damage':0.6}
        self.base_active_skill_attribute={'additional_damage':3.2}
        self.passive_skill_attribute_perlevel = {'possibilities':4,'element_strength':3,'boss_damage':0.96}
        self.passive_skill_attribute = {'possibilities':64,'element_strength':40,'boss_damage':12}
        self.active_add_level=0
        self.passive_add_level=0
        self.shape2_usage = 0  # 形态2的使用次数
        self.present_hit=0 #记录当前的连击数 为后面叠层做准备
        self.work_indicator=False
        self.level_flag=False
        self.effect_strength(strength=strength)


    def effect(self,character):
        #处理等级
        if not self.level_flag:
            for key,item in character.skill_item.items():
                if hasattr(item,'add_level'):
                    item.add_level=item.add_level+1
            self.level_flag=True
        #处理冷却
        if not self.work_indicator:
            if 'use skill' in character.condition or 'use supper skill' in character.condition:
                self.present_hit+=1
        
        interval=character.intervals['time_interval']['present']
        if self.present_lefttime > interval:
            self.present_lefttime -= interval
        else:
            self.present_lefttime = 0

        if self.current_shape == 1:
            if self.cooltime[0] > interval:
                self.cooltime[0] -= interval
            else:
                self.cooltime[0] = 0
            self.present_cooltime=self.cooltime[0]

        if self.current_shape == 2:
            if self.cooltime[0] > interval:
                self.cooltime[0] -= interval
            else:
                self.cooltime[0] = 0

            if self.cooltime[1] > interval:
                self.cooltime[1] -= interval
            else:
                self.cooltime[1] = 0
            self.present_cooltime=self.cooltime[1]


    def effect_strength(self,strength:dict):
        #处理魂印的常驻属性
        for key,value in strength.items():
            dicts=mapping_for_strength[key][value]
            self.dict_add(self.attribute,dicts)

        #处理力魂印
        power=strength.get('power',None)
        if power is not None:
            if power == 'pink':
                for key,value in self.self_attribute.items():
                    self.self_attribute[key] *=1.2
            if power == 'pink_2025':
                for key,value in self.self_attribute.items():
                    self.self_attribute[key] *=1.25
            else:
                for key,value in self.self_attribute.items():
                    self.self_attribute[key] *=1.1
        self.dict_add(self.attribute,self.self_attribute)
        
        #处理技魂印
        skill=strength.get('skill',None)
        if skill is not None:
            if skill == 'pink':
                self.active_add_level+=1
                self.passive_add_level+=1
            else:
                self.passive_add_level+=1
        
        #处理属性
        for key,value in self.passive_skill_attribute.items():
            value += self.passive_skill_attribute_perlevel[key]*self.passive_add_level
        
        self.dict_add(self.attribute,self.passive_skill_attribute)

        #处理速魂印
        speed=strength.get('speed',None)
        if speed is not None:
            if speed == 'pink':
                for max_cooltime in self.max_cooltime:
                    max_cooltime *= 0.9
            else:
                for max_cooltime in self.max_cooltime:
                    max_cooltime *= 0.95

    def use(self,interval:dict):
        # 处理技能的冷却逻辑
        if self.current_shape == 1:
            # 形态1的技能触发
            if self.present_cooltime == 0:
                #print(f"{self.name} 形态1技能触发！")
                # 触发形态1后设置冷却，同时切换到形态2
                if not self.work_indicator:
                    self.present_cnt=6
                    self.work_indicator=True
                    attribute=(self.base_active_skill_attribute['additional_damage']+self.active_add_level*self.active_skill_attribute_perlevel['additional_damage'])*self.present_cnt
                    self.attribute['additional_damage']+=attribute
                self.present_cooltime = self.max_cooltime[1]
                self.cooltime[0] = self.max_cooltime[0]
                self.cooltime[1]=self.max_cooltime[1]
                self.present_lefttime=self.max_lefttime
                self.current_shape = 2  # 切换到形态2
    
        elif self.current_shape == 2:
            # 形态2的技能触发
            if self.present_cooltime == 0:
                #print(f"{self.name} 形态2技能触发！")
                self.work_indicator=True
                self.present_cnt=int(self.present_hit*(self.passive_skill_attribute['possibilities']/100+self.passive_skill_attribute_perlevel['possibilities']/100*self.passive_add_level))
                if self.present_cnt>6:
                    self.present_cnt=6
                self.present_hit=0
                attribute=(self.base_active_skill_attribute['additional_damage']+self.active_add_level*self.active_skill_attribute_perlevel['additional_damage'])*self.present_cnt
                self.attribute['additional_damage']+=attribute
                self.shape2_usage += 1
                # 每使用一次形态2进入冷却
                self.present_cooltime = self.max_cooltime[1]
                self.cooltime[1]=self.present_cooltime
                self.present_lefttime=self.max_lefttime

                # 如果使用了两次形态2，切换回形态1
                if self.shape2_usage >= 2:
                    print(f"{self.name} 切换回形态1！")
                    self.shape2_usage = 0
                    self.current_shape = 1  # 切换回形态1
                    self.present_cooltime = self.cooltime[0]
        
    def close(self):
        if self.work_indicator:
            if self.present_lefttime ==0:
                self.work_indicator=False
                self.attribute['additional_damage']-=(self.base_active_skill_attribute['additional_damage']+self.active_add_level*self.active_skill_attribute_perlevel['additional_damage'])*self.present_cnt
                self.present_cnt=0