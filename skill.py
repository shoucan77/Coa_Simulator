'''
battle需求 cost方法：获取冷却时间 calcu_damage方法 根据buff和属性计算伤害 present_cooltime属性和max_cooltime属性
amp_point(condition)方法 获取获得的共鸣能量

'''
class Skill:
    def __init__(self, name: str, base_rate:float,ex_base_rate:float,rate_per_level:float,rate_per_level_ex:float,add_level:int,max_cooltime: float,present_cooltime:float, cost: float, boost_points: int, hit_cnt_base:int,hit_cnt_ex:int,special_points_cost:float,condition:list, attribute: dict):
        '''
        name:技能名
        damage_rate:伤害倍率
        base_rate:基础倍率
        rate_per_level:每级新增倍率
        add_level:额外技能等级
        max_cooltime:技能面板却时间
        present_cooltime:当前冷却时间
        cost:技能动画时间
        boost_point:共鸣点数
        hit_cnt:连击次数
        attribute:人物面板
        '''
        self.name = name
        self.base_rate = base_rate
        self.ex_base_rate= ex_base_rate
        self.rate_per_level=rate_per_level
        self.rate_per_level_ex=rate_per_level_ex
        self._add_level = add_level
        self.max_cooltime = max_cooltime
        self.present_cooltime = present_cooltime
        self.cost = cost
        self.boost_points = boost_points
        self.hit_cnt_base = hit_cnt_base
        self.hit_cnt_ex = hit_cnt_ex
        self.special_points_cost = special_points_cost
        self.attribute = attribute
        self.condition = condition
        self.extra_rate=0 #技能倍率加成
        self.inde_rate=0 #独立倍率加成
        self.extra_cool_rate=0 #技能额外冷却加

    @property
    def add_level(self):
        return self._add_level

    @add_level.setter
    def add_level(self, value):
        self._add_level = value

    @property
    def damage_rate(self):
        '''
        condition 是否处于脱离态
        '''
        if not 'strength' in self.condition:
            return (self.base_rate + self.rate_per_level * self.add_level)*(1+self.extra_rate/100)*(1+self.inde_rate/100)
        else:
            return (self.base_rate + self.rate_per_level * self.add_level + self.ex_base_rate+self.rate_per_level_ex*self.add_level)*(1+self.extra_rate/100)*(1+self.inde_rate/100)
    @property #卓越1 鸟1 高阶2 时装3 闪灵1 8级 差卓越和鸟
    def hit_cnt(self):
        return self.hit_cnt_base+self.hit_cnt_ex if self.condition else self.hit_cnt_base

    
    def use(self):
        if self.name in ['15','55','s1']:
            if 'strength' not in self.condition and self.attribute['present_special_points']>0:
                self.condition.append('strength')
        
        dmrate=self.damage_rate
        if dmrate < 0:
            print("!!!!!!!!!!!!")
        damage=self.damage_rate/100*calcu_damage_rate(self.attribute)
        #公式 rate=cool_speed/(955+cool_speed*0.5)
        #公式 rate=atk_speed/（0.95*atk_speed+915）
        #公式 crit_rate=agility/（0.01*agility+90）
        
        #cool_rate=self.attribute['cool_speed']/(955+self.attribute['cool_speed']*0.5)
        atk_speed_rate=self.attribute['atk_speed']/(915+self.attribute['atk_speed']*0.95)
        cost=self.cost
        charge=self.attribute['boost_charge_rate']/100+1
        if 'strength'  in self.condition:
            self.attribute['present_special_points']=self.attribute['present_special_points']-self.special_points_cost*self.attribute['special_points_consume_rate'] if self.attribute['present_special_points']-self.special_points_cost*self.attribute['special_points_consume_rate'] >0 else 0
        if self.attribute['present_special_points']==0:
            self.condition.remove('strength')
        return damage,cost,self.boost_points*charge,self.hit_cnt


class normal_atk:
    def __init__(self,name:str,damage_rate:int,boost_points:int,cost:float,hit_cnt:int,attribute:dict):
        '''
        name:技能名
        damage_rate:伤害倍率
        boost_points:获得的共鸣点数
        cost:普攻动画时间
        hit_cnt:连击数
        '''
        self.name = name
        self.damage_rate = damage_rate
        self.boost_points = boost_points
        self.cost = cost
        self.hit_cnt =hit_cnt
        self.attribute = attribute

    def use(self):
        damage=self.damage_rate*calcu_damage_rate(self.attribute)/100
        #公式 rate=cool_speed/(955+cool_speed*0.5)
        #公式 rate=atk_speed/（0.95*atk_speed+915）
        #公式 crit_rate=agility/（0.01*agility+90）
        #cool_rate=self.attribute['cool_speed']/(955+self.attribute['cool_speed']*0.5)
        #atk_speed_rate=self.attribute['atk_speed']/(915+self.attribute['atk_speed']*0.95)
        cost=self.cost
        charge=self.attribute['boost_charge_rate']/100+1
        return damage,cost,self.boost_points*charge,self.hit_cnt

class pats_skill:
    def __init__(self,name:str, attribute:dict):
        self.name=name
        self.attribute=attribute
    
    def dict_add(self,a:dict,b:dict):
        for key in b:
            if isinstance(b[key], dict):
                self.dict_add(a, b[key])
            else:
                if key in a.keys():
                    a[key] += b[key]

mapping_for_strength ={
    'power':{'pink':{'boss_damage': 1.5,'final_damage':1},'pink_2025':{'boss_damage':2.4,'final_damage':1.6},'purple':{'def':100},'cat':{'element_damage':5}},
    'skill':{'pink':{'element_strength':4,'boosting_damage':2},'purple':{'atk':30}},
    'speed':{'pink':{'atk_speed':10,'cool_speed':10,'normal_damage':1.5,'skill_damage':1.5},'purple':{'hp':100}}
}



def calcu_damage_rate(attribute):
    '''
    调用前先处理好条件增伤 例如普攻 技伤 共鸣伤等等 全加到condition_damage 调用后再删除
    '''
    attribute['total_atk']=attribute['atk']*(1+attribute['atk_rate']/100)\
        *(1+attribute['strength']*(1+attribute['strength_rate']/100)/1000) #总攻击力
    
    attribute['total_super_atk']=attribute['super_atk']*(1+attribute['super_atk_rate']/100)
    
    crit_rate=attribute['crit_rate']+(attribute['agility']/(attribute['agility']*0.01+90))
    crit_rate/=100
    #防御减伤
    def_rate=(3500)/(3500+attribute['boss_def']*(1-attribute['penetrate']/100))
    
    #攻击 暴击 克制 条件 元素 伤害提升 附加伤害 独立
    #crit_rate 计算敏捷的提升
    total_atk=(attribute['total_atk']*def_rate+attribute['total_super_atk'])
    crit=(1+crit_rate*attribute['crit_damage']/100)
    boss=(1+attribute['boss_damage']/100)
    condition=(1+attribute['condition_damage']/100)
    element_strength=(1+attribute['element_strength']/220)
    element_damage=(1+attribute['element_damage']/100)
    final_damage=(1+attribute['final_damage']/100)
    additional_damage=(1+attribute['additional_damage']/100)
    indenpen=(1+attribute['independent_damage']/100)
    final_rate=total_atk*crit*boss*condition*element_strength*element_damage*final_damage*additional_damage*indenpen
    return final_rate