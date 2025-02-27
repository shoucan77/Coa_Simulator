from character import Character
from skill import Skill
from buff2 import Nicklace_SiMang,Wristband_SiMang,Ring_SiMang,Ring_YanMie,Amulet_SiMang,Amulet_YanMie,Seal_SiMang,Seal_YanMie,Suit5_SiMang,Suit5_YanMie
from buff2 import Nicklace_SiMangPlus,Wristband_SiMangPlus,Ring_SiMangPlus,Ring_YanMiePlus,Amulet_SiMangPlus,Amulet_YanMiePlus,Seal_SiMangPlus,Seal_YanMiePlus,Suit5_SiMangPlus,Suit5_YanMiePlus
import json
import inspect
'''
截至空海版本的装备
'''

class Buff:
    def __init__(self, name: str, buff:dict={}):
        self.name=name
        self.buff=buff

class final_weapon(Buff):
    def effect(self, character:Character):
        if 'final_weapon' not in self.buff.keys():
            self.buff['final_weapon'] = {'work':False}
        if not self.buff['final_weapon']['work']:
            self.buff['final_weapon']['work'] = True
            skill=character.skill_item['s2']
            skill.extra_rate+=15.0
            skill.extra_cool_rate+=15.0
            for item in character.skill_item.values():
                if hasattr(item,'add_level'):
                    item.add_level=item.add_level+1

class Helmet_DieWu(Buff):
    def effect(self,character:Character):
        if 'Helmet_DieWu' not in self.buff.keys():
            self.buff['Helmet_DieWu'] = {'cool_time':0,'left_time':0,'hit':0,'attribute_name':'skill_damage','attribute_value':10,'work':False}
        self.buff['Helmet_DieWu']['hit']+=character.intervals['hit_cnt']['present']
        if self.buff['Helmet_DieWu']['left_time'] ==0 and self.buff['Helmet_DieWu']['work']:
            self.work(character,work_indicator=False)

        if self.buff['Helmet_DieWu']['hit']>=10:
            if not self.buff['Helmet_DieWu']['work']:
                self.work(character,work_indicator=True)
            elif self.buff['Helmet_DieWu']['cool_time'] ==0:
                self.work(character,work_indicator=True)
            self.buff['Helmet_DieWu']['hit']=0
            return


    def work(self,character:Character,work_indicator:bool):
            '''
            character：受影响的角色
            work_indicator：工作方式 t加buff f移除buff
            '''
            attribute=self.buff['Helmet_DieWu']['attribute_name']
            values=self.buff['Helmet_DieWu']['attribute_value']
            if work_indicator:
                if self.buff['Helmet_DieWu']['work']: #重置
                    self.buff['Helmet_DieWu']['cool_time']=10
                    self.buff['Helmet_DieWu']['left_time']=20
                else:
                    character.attribute[attribute]+=values #加上buff
                    self.buff['Helmet_DieWu']['cool_time']=10
                    self.buff['Helmet_DieWu']['left_time']=20
                    self.buff['Helmet_DieWu']['work']=True
            else:
                if self.buff['Helmet_DieWu']['work']: #防止多次检测重复扣除
                    character.attribute[attribute]-=values
                    self.buff['Helmet_DieWu']['work']=False
            return

class Clothes_DieWu(Buff):
    def effect(self,character:Character):
        if 'Clothes_DieWu' not in self.buff.keys():
            self.buff['Clothes_DieWu'] = {'cool_time':0,'attribute_name':'all_skill_ct_value','attribute_value':3.5,'work':False}
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            if self.buff['Clothes_DieWu']['cool_time'] == 0:
                self.work(character)

        if self.buff['Clothes_DieWu']['work'] == False:
            character.attribute['condition_damage']+=6
            self.buff['Clothes_DieWu']['work']=True
            #character.condition.remove('use skill') 交给外面处理

    def work(self,character):
        for key,skill in character.skill_item.items():
            if key in ['A1', 'A2', 'A3', 'A4', 'break']:
                continue
            if skill.present_cooltime<=3.5:
                skill.present_cooltime=0
            else:
                skill.present_cooltime-=3.5
        self.buff['Clothes_DieWu']['cool_time']=20

class Gloves_DieWu(Buff):
    def effect(self,character:Character):
        if 'Gloves_DieWu' not in self.buff.keys():
            self.buff['Gloves_DieWu'] = {'cool_time':0,'left_time':0,'attribute_name':'atk_rate','attribute_value':17,'work':False}
        if 'atk' in character.condition:
            if not self.buff['Gloves_DieWu']['work']: #未持续一定冷却=0
                self.work(character,work_indicator=True)
            elif self.buff['Gloves_DieWu']['cool_time'] ==0: #持续则重置buff
                self.work(character,work_indicator=True)
            return
        if self.buff['Gloves_DieWu']['left_time'] ==0 and self.buff['Gloves_DieWu']['work']: 
            self.work(character,work_indicator=False)

    def work(self,character:Character,work_indicator:bool):
        '''
        character：受影响的角色
        work_indicator：工作方式 t加buff f移除buff
        '''
        attribute=self.buff['Gloves_DieWu']['attribute_name']
        values=self.buff['Gloves_DieWu']['attribute_value']
        if work_indicator:
            if self.buff['Gloves_DieWu']['work']: #重置
                self.buff['Gloves_DieWu']['cool_time']=10
                self.buff['Gloves_DieWu']['left_time']=20
            else:
                character.attribute[attribute]+=values #加上buff
                self.buff['Gloves_DieWu']['cool_time']=10
                self.buff['Gloves_DieWu']['left_time']=20
                self.buff['Gloves_DieWu']['work']=True
        else:
            if self.buff['Gloves_DieWu']['work']: #防止多次检测重复扣除
                character.attribute[attribute]-=values
                self.buff['Gloves_DieWu']['work']=False
        return

class Trousers_DieWu(Buff):
    def effect(self, character: Character):
        # 初始化Trousers1_Diewu的buff状态
        if 'Trousers1_Diewu' not in self.buff.keys():
            self.buff['Trousers1_Diewu'] = {
                'cool_time': 0,
                'left_time': 0,
                'attribute_name': 'crit_damage',
                'attribute_value': 24,
                'max_duration':20,
                'work': False
            }
        
        # 初始化Trousers2_Diewu的buff状态
        if 'Trousers2_Diewu' not in self.buff.keys():
            self.buff['Trousers2_Diewu'] = {
                'cool_time': 0,
                'left_time': 0,
                'attribute_name': 'crit_damage',
                'attribute_value': 8,
                'max_duration':60,
                'work': False
            }
        
        # 处理Trousers1_Diewu效果
        
        self.process_effect(character, 'Trousers1_Diewu', 'use skill',self.buff['Trousers1_Diewu']['max_duration'])

        # 处理Trousers2_Diewu效果
        self.process_effect(character, 'Trousers2_Diewu', 'use supper skill', self.buff['Trousers2_Diewu']['max_duration'])
        
    def process_effect(self, character: Character, buff_key: str, trigger_condition: str, duration: float):
        """处理单个buff效果逻辑"""
        if self.buff[buff_key]['left_time'] == 0 and self.buff[buff_key]['work']:  # 检查持续时间
            self.work(character, buff_key, self.buff[buff_key]['max_duration'],work_indicator=False)

        if trigger_condition in character.condition:
            if not self.buff[buff_key]['work']:
                self.work(character, buff_key, self.buff[buff_key]['max_duration'],work_indicator=True)
            elif buff_key == 'Trousers2_Diewu':  # 为特定效果刷新时间
                self.buff[buff_key]['left_time'] = duration  # 刷新持续时间

    def work(self, character: Character, buff_key: str, duration:float,work_indicator: bool):
        """应用或移除buff"""
        attribute = self.buff[buff_key]['attribute_name']
        values = self.buff[buff_key]['attribute_value']
        
        if work_indicator:
            character.attribute[attribute] += values
            self.buff[buff_key]['left_time'] = duration  # 设置持续时间
            self.buff[buff_key]['cool_time'] = 20 if buff_key=='Trousers1_Diewu' else 0
            self.buff[buff_key]['work'] = True
        else:
            if self.buff[buff_key]['work']:
                character.attribute[attribute] -= values
                self.buff[buff_key]['work'] = False

class Shoes_DieWu(Buff):
    def effect(self, character: Character):
        if 'Shoes_DieWu' not in self.buff.keys():
            # 初始化buff的状态
            self.buff['Shoes_DieWu'] = {
                'cool_time': 0,  # 冷却时间
                'left_time': 0,  # 剩余持续时间
                'attribute_name_strength': 'element_strength',  # 属性强化名称
                'attribute_value_strength': 40,  # 增加的属性强化
                'attribute_name_damage': 'element_damage',  # 属性伤害名称
                'attribute_value_damage': 3,  # 增加的属性伤害
                'work': False  # 是否在工作状态
            }


        
        # 检查buff的持续时间
        if self.buff['Shoes_DieWu']['left_time'] == 0:  # 当前没有持续时间
            self.deactivate_buff(character)  # 移除buff
        
        # 检查冷却时间
        if self.buff['Shoes_DieWu']['cool_time'] == 0:
            # 每35秒增加增益
            if not self.buff['Shoes_DieWu']['work']:
                self.activate_buff(character)  # 应用buff




    def activate_buff(self, character: Character):
        """应用buff效果."""
        # 使用临时变量储存字段
        attr_strength = self.buff['Shoes_DieWu']['attribute_name_strength']
        attr_value_strength = self.buff['Shoes_DieWu']['attribute_value_strength']
        attr_damage = self.buff['Shoes_DieWu']['attribute_name_damage']
        attr_value_damage = self.buff['Shoes_DieWu']['attribute_value_damage']

        # 应用属性强化和属性伤害的加成
        character.attribute[attr_strength] += attr_value_strength
        character.attribute[attr_damage] += attr_value_damage
        self.buff['Shoes_DieWu']['left_time'] = 35  # 设置35秒的持续时间
        self.buff['Shoes_DieWu']['work'] = True  # 标记为工作状态
        self.buff['Shoes_DieWu']['cool_time'] = 35# 设置冷却时间

    def deactivate_buff(self, character: Character):
        """移除buff效果."""
        if self.buff['Shoes_DieWu']['work']:  # 防止重复移除
            # 使用临时变量储存字段
            attr_strength = self.buff['Shoes_DieWu']['attribute_name_strength']
            attr_value_strength = self.buff['Shoes_DieWu']['attribute_value_strength']
            attr_damage = self.buff['Shoes_DieWu']['attribute_name_damage']
            attr_value_damage = self.buff['Shoes_DieWu']['attribute_value_damage']
            
            # 移除属性强化和属性伤害的加成
            character.attribute[attr_strength] -= attr_value_strength
            character.attribute[attr_damage] -= attr_value_damage
            self.buff['Shoes_DieWu']['work'] = False  # 标记为不在工作状态
            self.buff['Shoes_DieWu']['cool_time'] = 0  # 重置冷却时间
            self.buff['Shoes_DieWu']['left_time'] = 0  # 重置剩余时间

#2 3 5件套效果类
class Suit3_DieWu(Buff):
    MAX_STACKS = 4  # 最大叠加层数

    def effect(self, character: Character):
        if 'Suit3_DieWu' not in self.buff.keys():
            # 初始化buff的状态
            self.buff['Suit3_DieWu'] = {
                'stacks': 0,  # 当前层数
                'left_time': 0,  # 剩余持续时间
                'attribute_name_strength': 'element_strength',  # 属性强化名称
                'attribute_value_strength_per_stack': 7,  # 每层增加的属性强化
                'attribute_name_crit_damage': 'crit_damage',  # 暴击伤害名称
                'attribute_value_crit_damage_per_stack': 5.5,  # 每层增加的暴击伤害
                'attribute_name_boss_damage': 'boss_damage',  # boss伤害名称
                'attribute_value_boss_damage_per_stack': 2,  # 每层增加的boss伤害
                'work':False
            }

        #检查持续时间
        if self.buff['Suit3_DieWu']['left_time'] <= 0 and self.buff['Suit3_DieWu']['work'] :
            self.clear_buff(character)

        # 检查角色是否释放技能
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            self.add_stack(character)
            self.buff['Suit3_DieWu']['work']=True


    def add_stack(self, character: Character):
        """增加叠加层数的buff"""
        if self.buff['Suit3_DieWu']['stacks'] < self.MAX_STACKS:
            self.buff['Suit3_DieWu']['stacks'] += 1
            self.buff['Suit3_DieWu']['left_time'] = 20  # 每次增加层数后更新持续时间
            self.update_attributes(character)
        else:
            self.buff['Suit3_DieWu']['left_time'] = 20

            # 增加属性
        

    def update_attributes(self, character: Character):

        # 应用叠层效果
        character.attribute[self.buff['Suit3_DieWu']['attribute_name_strength']] +=  self.buff['Suit3_DieWu']['attribute_value_strength_per_stack']
        character.attribute[self.buff['Suit3_DieWu']['attribute_name_crit_damage']] += self.buff['Suit3_DieWu']['attribute_value_crit_damage_per_stack']
        character.attribute[self.buff['Suit3_DieWu']['attribute_name_boss_damage']] += self.buff['Suit3_DieWu']['attribute_value_boss_damage_per_stack']

    def clear_buff(self, character: Character):
        """清理buff效果"""
        self.clear_attributes(character)
        self.buff['Suit3_DieWu']['stacks'] = 0
        self.buff['Suit3_DieWu']['left_time'] = 0
        self.buff['Suit3_DieWu']['work']=False

    def clear_attributes(self, character: Character):
        """清理角色属性的增益效果"""
        # 移除所有层数带来的属性增加
        character.attribute[self.buff['Suit3_DieWu']['attribute_name_strength']] -= self.buff['Suit3_DieWu']['stacks'] * self.buff['Suit3_DieWu']['attribute_value_strength_per_stack']
        character.attribute[self.buff['Suit3_DieWu']['attribute_name_crit_damage']] -= self.buff['Suit3_DieWu']['stacks'] * self.buff['Suit3_DieWu']['attribute_value_crit_damage_per_stack']
        character.attribute[self.buff['Suit3_DieWu']['attribute_name_boss_damage']] -= self.buff['Suit3_DieWu']['stacks'] * self.buff['Suit3_DieWu']['attribute_value_boss_damage_per_stack']

class Suit5_DieWu(Buff):
    def __init__(self,name,buff):
        super().__init__(name=name,buff=buff)
        self.is_applied = False  # 标志位，表示增益是否已应用
    def effect(self, character: Character):
        if 'Suit5_DieWu' not in self.buff.keys():
            # 初始化buff的状态
            self.buff['Suit5_DieWu'] = {
                'attribute_name_strength': 'element_strength',
                'boss_damage_per_60_strength': 2,
                'max_boss_damage': 14,
                'attribute_name_resistance': 'element_resistance',
                'final_damage_per_25_resistance': 2,
                'max_final_damage': 6,
                'extra_final_damage': 11,
                'extra_skill_damage': 9,
                'extra_normal_damage': 9,
                'boost_duration': 20,
                'left_time': 0,  # 额外增益效果的剩余持续时间
                'work':False
            }
        
        if self.buff['Suit5_DieWu']['left_time'] <= 0 and self.buff['Suit5_DieWu']['work']:
            self.clear_extra_boost(character)
            self.buff['Suit5_DieWu']['work']=False
        
        self.check_and_apply_extra_boost(character)

        if not self.is_applied:
            self.update_attributes_based_on_strength(character)
            self.update_attributes_based_on_resistance(character)
            self.skill_level_up(character)
            self.is_applied=True


    def update_attributes_based_on_strength(self, character: Character):
        """根据属性强化增加 boss 伤害"""
        strength = character.attribute[self.buff['Suit5_DieWu']['attribute_name_strength']]
        additional_boss_damage = min((strength // 60) * self.buff['Suit5_DieWu']['boss_damage_per_60_strength'],
                                     self.buff['Suit5_DieWu']['max_boss_damage'])

        # 应用 boss 伤害增益
        character.attribute['boss_damage'] += additional_boss_damage

    def update_attributes_based_on_resistance(self, character: Character):
        """根据属性抗性增加最终伤害"""
        resistance = character.attribute[self.buff['Suit5_DieWu']['attribute_name_resistance']]
        additional_final_damage = min((resistance // 25) * self.buff['Suit5_DieWu']['final_damage_per_25_resistance'],
                                      self.buff['Suit5_DieWu']['max_final_damage'])

        # 应用最终伤害增益
        character.attribute['final_damage'] += additional_final_damage

    def check_and_apply_extra_boost(self, character: Character):
        """检查 Suit3_DieWu 的四层叠加状态并应用额外增益"""
        suit3_buff = character.buff.get('Suit3_DieWu', {})
        if suit3_buff.get('stacks', 0) == 4:
            # 如果 Suit3_DieWu 的层数为4，应用额外增益
            if self.buff['Suit5_DieWu']['left_time'] <= 0 and not self.buff['Suit5_DieWu']['work']:
                character.attribute['final_damage'] += self.buff['Suit5_DieWu']['extra_final_damage']
                character.attribute['skill_damage'] += self.buff['Suit5_DieWu']['extra_skill_damage']
                character.attribute['normal_damage'] += self.buff['Suit5_DieWu']['extra_normal_damage']
                self.buff['Suit5_DieWu']['left_time'] = self.buff['Suit5_DieWu']['boost_duration']
                self.buff['Suit5_DieWu']['work']=True
            else:
                self.buff['Suit5_DieWu']['left_time'] = self.buff['Suit5_DieWu']['boost_duration']

    def skill_level_up(self, character: Character):
        skill_list=character.skill_item
        for item in character.skill_item.values():
                if hasattr(item,'add_level'):
                    item.add_level=item.add_level+1
        skill1=skill_list.get('s1',None)
        if skill1 is not None:
            skill1.extra_rate+=30
        skill2=skill_list.get('s2',None)
        if skill2 is not None:
            skill2.extra_rate+=30
        skill3=skill_list.get('minis',None)
        if skill3 is not None:
            skill3.extra_rate+=30
    def clear_extra_boost(self, character: Character):
        """清理因 Suit3_DieWu 的四层触发的额外增益"""
        if self.buff['Suit5_DieWu']['work']:
            character.attribute['final_damage'] -= self.buff['Suit5_DieWu']['extra_final_damage']
            character.attribute['skill_damage'] -= self.buff['Suit5_DieWu']['extra_skill_damage']
            character.attribute['normal_damage'] -= self.buff['Suit5_DieWu']['extra_normal_damage']

class Nicklace_ShengHui(Buff):
    
    def effect(self, character: Character):
        # 初始化buff状态
        if 'Nicklace_ShengHui' not in self.buff.keys():
            self.buff['Nicklace_ShengHui'] = {
                'layer_count': 5,
                'max_layers': 5,
                'attribute_name': 'crit_damage',
                'attribute_value': 8,  # 每层的暴击伤害增加值
                'work': False
            }

        # 当不在共鸣状态时：没有层数
        if 'boost' not in character.condition and not self.buff['Nicklace_ShengHui']['work']:
            layer=(character.attribute['crit_rate']/100+character.attribute['agility']/(character.attribute['agility']*0.01+90))*(character.intervals['hit_cnt']['present']-character.intervals['hit_cnt']['last']) #期望暴击次数
            if self.buff['Nicklace_ShengHui']['layer_count']+int(layer) < self.buff['Nicklace_ShengHui']['max_layers']:
                self.buff['Nicklace_ShengHui']['layer_count']+=int(layer)
            else:
                self.buff['Nicklace_ShengHui']['layer_count']=self.buff['Nicklace_ShengHui']['max_layers']
            return

        #没共鸣 有层数的情况 不单独写层数为1 容易出bug
        if 'boost' not in character.condition and self.buff['Nicklace_ShengHui']['work']:
            if 'use skill' in character.condition or 'use supper skill' in character.condition:
                if not self.buff['Nicklace_ShengHui']['work'] and self.buff['Nicklace_ShengHui']['layer_count'] > 0:
                    self.work(character, work_indicator=True)
                elif self.buff['Nicklace_ShengHui']['work'] and self.buff['Nicklace_ShengHui']['layer_count'] == 0:
                    # 如果没有剩余层数，则停止工作
                    self.buff['Nicklace_ShengHui']['work']=False

        if 'boost'  in character.condition:
            self.buff['Nicklace_ShengHui']['work']=True

        # 当处于共鸣状态时，释放技能消耗层数
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            if self.buff['Nicklace_ShengHui']['work'] and self.buff['Nicklace_ShengHui']['layer_count'] > 0:
                self.work(character, work_indicator=True)
            elif self.buff['Nicklace_ShengHui']['work'] and self.buff['Nicklace_ShengHui']['layer_count'] == 0:
                # 如果没有剩余层数，则停止工作
                self.buff['Nicklace_ShengHui']['work']=False

    def work(self, character: Character, work_indicator: bool):
        '''
        character：受影响的角色
        work_indicator：工作方式 t加buff f移除buff
        '''
        attribute = self.buff['Nicklace_ShengHui']['attribute_name']
        layer_count = self.buff['Nicklace_ShengHui']['layer_count']
        total_effect = layer_count * self.buff['Nicklace_ShengHui']['attribute_value']

        if work_indicator:
            # 应用buff，并消耗一层
            character.attribute[attribute] += total_effect

    def close(self, character: Character):
        if self.buff['Nicklace_ShengHui']['work'] and ('use skill' in character.condition or 'use supper skill' in character.condition) and self.buff['Nicklace_ShengHui']['layer_count']>0:
            attribute = self.buff['Nicklace_ShengHui']['attribute_name']
            layer_count = self.buff['Nicklace_ShengHui']['layer_count']
            total_effect = layer_count * self.buff['Nicklace_ShengHui']['attribute_value']

            character.attribute[attribute] -= total_effect
            self.buff['Nicklace_ShengHui']['layer_count'] -= 1
            if self.buff['Nicklace_ShengHui']['layer_count']==0:
                self.buff['Nicklace_ShengHui']['work'] = False

class Wristband_ShengHui(Buff):
    def effect(self, character: Character):
        # 初始化 buff 状态
        if 'Wristband_ShengHui' not in self.buff.keys():
            self.buff['Wristband_ShengHui'] = {
                'layer_count': 5,
                'max_layers': 5,
                'attribute_name': 'skill_damage',
                'attribute_value': 5,  # 每层的技能伤害增加值
                'work': False
            }

        # 当不在共鸣状态时，释放技能增加一层效果
        if 'boost' not in character.condition and not self.buff['Wristband_ShengHui']['work']:
            if ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Wristband_ShengHui']['layer_count'] < self.buff['Wristband_ShengHui']['max_layers']:
                self.buff['Wristband_ShengHui']['layer_count'] += 1
            return

        if 'boost' not in character.condition and self.buff['Wristband_ShengHui']['work']:
            if ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Wristband_ShengHui']['layer_count'] > 0:
                self.work(character, work_indicator=True)
            elif self.buff['Wristband_ShengHui']['layer_count'] == 0:
                self.buff['Wristband_ShengHui']['work'] = False

        # 当处于共鸣状态时，释放技能消耗一层效果
        if 'boost' in character.condition:
            self.buff['Wristband_ShengHui']['work'] = True
            if ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Wristband_ShengHui']['layer_count'] > 0:
                self.work(character, work_indicator=True)
            elif self.buff['Wristband_ShengHui']['layer_count'] == 0:
                self.buff['Wristband_ShengHui']['work'] = False

    def work(self, character: Character, work_indicator: bool):
        '''
        character：受影响的角色
        work_indicator：工作方式 t加buff f移除buff
        '''
        attribute = self.buff['Wristband_ShengHui']['attribute_name']
        layer_count = self.buff['Wristband_ShengHui']['layer_count']
        total_effect = layer_count * self.buff['Wristband_ShengHui']['attribute_value']

        if work_indicator and self.buff['Wristband_ShengHui']['work']:
            # 应用效果，并消耗一层
            character.attribute[attribute] += total_effect

    def close(self, character: Character):
        # 在work状态下，如果使用过技能，执行关闭逻辑
        if self.buff['Wristband_ShengHui']['work'] and ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Wristband_ShengHui']['layer_count'] > 0:
            attribute = self.buff['Wristband_ShengHui']['attribute_name']
            layer_count = self.buff['Wristband_ShengHui']['layer_count']
            total_effect = layer_count * self.buff['Wristband_ShengHui']['attribute_value']

            character.attribute[attribute] -= total_effect
            self.buff['Wristband_ShengHui']['layer_count'] -= 1
            if self.buff['Wristband_ShengHui']['layer_count']==0:
                self.buff['Wristband_ShengHui']['work'] = False

class Ring_ShengHui(Buff):
    def effect(self, character: Character):
        # 初始化 buff 状态
        if 'Ring_ShengHui' not in self.buff.keys():
            self.buff['Ring_ShengHui'] = {
                'layer_count': 5,
                'max_layers': 5,
                'attribute_name': 'element_strength',
                'attribute_value': 6,  # 每层的属性强化增加值
                'work': False
            }

        # 计算时间间隔
        interval = (character.intervals['time_interval']['present'] - character.intervals['time_interval']['last']) / 3

        # 当不在共鸣状态时，时间间隔增加层数
        if 'boost' not in character.condition and not self.buff['Ring_ShengHui']['work']:
            new_layers = self.buff['Ring_ShengHui']['layer_count'] + interval
            if new_layers < self.buff['Ring_ShengHui']['max_layers']:
                self.buff['Ring_ShengHui']['layer_count'] = new_layers
            else:
                self.buff['Ring_ShengHui']['layer_count'] = self.buff['Ring_ShengHui']['max_layers']
            return
        
        #共鸣完了，层数没完
        if 'boost' not in character.condition and self.buff['Ring_ShengHui']['work']:
            self.buff['Ring_ShengHui']['layer_count'] = int(self.buff['Ring_ShengHui']['layer_count'])  # 截断小数部分
            if ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Ring_ShengHui']['layer_count'] > 0:
                self.work(character, work_indicator=True)
            elif self.buff['Ring_ShengHui']['layer_count'] == 0:
                self.buff['Ring_ShengHui']['work'] = False

        # 当处于共鸣状态时，消耗整层的效果
        if 'boost' in character.condition:
            self.buff['Ring_ShengHui']['work'] = True
            self.buff['Ring_ShengHui']['layer_count'] = int(self.buff['Ring_ShengHui']['layer_count'])  # 截断小数部分
            if ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Ring_ShengHui']['layer_count'] > 0:
                self.work(character, work_indicator=True)
            elif self.buff['Ring_ShengHui']['layer_count'] == 0:
                self.buff['Ring_ShengHui']['work'] = False

    def work(self, character: Character, work_indicator: bool):
        '''
        character：受影响的角色
        work_indicator：工作方式 t加buff f移除buff
        '''
        attribute = self.buff['Ring_ShengHui']['attribute_name']
        layer_count = self.buff['Ring_ShengHui']['layer_count']
        total_effect = layer_count * self.buff['Ring_ShengHui']['attribute_value']

        if work_indicator and self.buff['Ring_ShengHui']['work']:
            # 应用效果
            character.attribute[attribute] += total_effect

    def close(self, character: Character):
        # 在work状态下，如果使用过技能，执行关闭逻辑
        if self.buff['Ring_ShengHui']['work'] and  ('use skill' in character.condition or 'use supper skill' in character.condition) and \
                    self.buff['Ring_ShengHui']['layer_count'] > 0:
            attribute = self.buff['Ring_ShengHui']['attribute_name']
            layer_count = self.buff['Ring_ShengHui']['layer_count']
            total_effect = layer_count * self.buff['Ring_ShengHui']['attribute_value']

            character.attribute[attribute] -= total_effect
            self.buff['Ring_ShengHui']['layer_count'] -= 1
            if self.buff['Ring_ShengHui']['layer_count']==0:
                self.buff['Ring_ShengHui']['work'] = False

class Amulet_ShengHui(Buff):
    def effect(self, character: Character):
        # 初始化 buff 状态
        if 'Amulet_ShengHui' not in self.buff.keys():
            self.buff['Amulet_ShengHui'] = {
                'boost_points': 0,  # 共鸣能量变化量
                'strength_rate': 0,  # 力量百分比提升
                'boost_rate_per_10000': 5,  # 每10000点共鸣能量增加的力量百分比
                'work': False
            }

        if 'boost' not in character.condition:
            self.buff['Amulet_ShengHui']['boost_points'] =character.attribute['boost_points']
            self.buff['Amulet_ShengHui']['strength_rate']=self.buff['Amulet_ShengHui']['boost_points']/10000*5


        # 始终应用力量增益
        if 'boost' in character.condition:
            self.buff['Amulet_ShengHui']['work'] = True
            self.buff['Amulet_ShengHui']['strength_rate']=20
        
        if 'atk' in character.condition:
            self.apply_strength_rate(character)

    def apply_strength_rate(self, character: Character):
        ''' 应用力量百分比到角色的属性上 '''
        character.attribute['strength_rate'] += self.buff['Amulet_ShengHui']['strength_rate']

    def close(self, character: Character):
        # 停止状态时，可以清除力量提升
        if  'atk' in character.condition:
            character.attribute['strength_rate'] -= self.buff['Amulet_ShengHui']['strength_rate']


class Seal_ShengHui(Buff):
    def __init__(self,name,buff):
        super().__init__(name,buff)
        self.is_applied = False  # 标志位，表示增益是否已应用

    def effect(self, character: Character):
        # 初始化 buff 状态
        if 'Seal_ShengHui' not in self.buff.keys():
            self.buff['Seal_ShengHui'] = {
                'boost_charge_rate': 0,  # 共鸣充能效率
                'final_damage': 0,  # 最终伤害提升
            }

        # 计算付给的共鸣充能效率
        boost_charge_rate = character.attribute.get('boost_charge_rate', 0)

        # 每4点共鸣充能效率提升1点最终伤害
        if boost_charge_rate >= 4 and not self.is_applied:
            additional_damage = max(boost_charge_rate / 4,10)
            self.buff['Seal_ShengHui']['final_damage'] += additional_damage
            character.attribute['final_damage'] += self.buff['Seal_ShengHui']['final_damage']
            self.is_applied = True  # 标记为已应用

        # 更新角色的最终伤害属性
        
    '''
    不需要写close
    def close(self, character: Character):
        # 清除最终伤害提升
        character.attribute['final_damage'] -= self.buff['Seal_ShengHui']['final_damage']
        self.is_applied = False  # 重置为未应用状态，以便下次可重新应用
    '''

class treasure_final(Buff):
    def __init__(self, name: str, buff: dict = {}):
        super().__init__(name, buff)
        self.is_applied = False  # 标志位，表示增益是否已应用
    def effect(self, character: Character):
        if self.is_applied:
            return
        
        self.is_applied = True
        with open('equip_reinforcement.json','r',encoding='utf-8-sig') as file:
            reinforcement = json.load(file)
        total=0
        for value in reinforcement.values():
            total+=value
        if total>=50:
            character.attribute['super_atk_rate']+=1.6
        if total>=100:
            character.attribute['super_atk_rate']+=2
        if total>=120:
            character.attribute['boost_charge_rate']+=4.2
        if total >= 130:
            character.attribute['super_atk']+=50
        if total >= 140:
            character.attribute['super_atk']+=70
        if total >= 150:
            character.attribute['super_atk_rate']+=2.4
            character.attribute['hp']+=(total-150)*50
        if total >= 160:
            character.attribute['atk_rate']+=1.2
        if total >= 170:
            character.attribute['element_strength']+=6
        if total >= 180:
            character.attribute['atk_rate']+=1.8
            character.attribute['atk']+=(total-180)*2
        if total >= 190:
            character.attribute['boosting_damage']+=3.5
        if total >= 200:
            character.attribute['super_atk_rate']+=2.8
            character.attribute['super_atk']+=(total-200)*10
        if total >= 210:
            character.attribute['hp']+=1000
        if total >= 220:
            character.attribute['boosting_damage']+=2
            character.attribute['boost_charge_rate']+=6.5
        if total >= 230:
            character.attribute['super_atk_rate']+=3.2
        if total >= 240:
            for key,value in character.skill_item.items():
                if key in [str(x*5) for x in range(1,7)]+['1']:
                    value.add_level=value.add_level+1
        if total >= 245:
            character.attribute['atk_rate']+=2.4

        if total >= 250:
            for key,value in character.skill_item.items():
                if key in [str(x*5) for x in range(7,11)]+['s1']:
                    value.add_level=value.add_level+1
        if total >= 255:
            character.attribute['crit_damage']+=5
        if total >= 260:
            character.attribute['strength_rate']+=3
        if total >= 265:
            character.attribute['final_damage']+=3
        if total >= 270:
            for key,value in character.skill_item.items():
                if key in [str(x*5) for x in range(11,15)]+['s2']:
                    value.add_level=value.add_level+1
        if total >= 275:
            character.attribute['boss_damage']+=3

class Suit3_ShengHui(Buff):
    '''懒得写15秒持续了'''
    def __init__(self,buff,name):
        super().__init__(buff,name)
        self.is_applied = False  # 标志位，表示增益是否已应用
    def effect(self, character: Character,skill: Skill):
        # 初始化 buff 状态
        if 'Suit3_ShengHui' not in self.buff.keys():
            self.buff['Suit3_ShengHui'] = {
                'boosting_damage': 40,
                'boost_points_rate': 0.5,
                'next_skill_strength':30,
                'flag_first_boost':False, #指示开启共鸣
                'skill_name':None,
                'work': False #指示30倍率已打出
            }
        #初次开启共鸣
        if 'boost' in character.condition and not self.buff['Suit3_ShengHui']['flag_first_boost']:
            self.buff['Suit3_ShengHui']['flag_first_boost'] = True
            self.buff['Suit3_ShengHui']['work'] = True
            character.attribute['boost_points']*=self.buff['Suit3_ShengHui']['boost_points_rate']
            character.attribute['boosting_damage']+=self.buff['Suit3_ShengHui']['boosting_damage']

        if 'boost' not in character.condition and self.buff['Suit3_ShengHui']['flag_first_boost']:
            self.buff['Suit3_ShengHui']['flag_first_boost'] = False
            character.attribute['boosting_damage']-=self.buff['Suit3_ShengHui']['boosting_damage']

        if ('use skill' in character.condition or 'use supper skill' in character.condition) and self.buff['Suit3_ShengHui']['work']:
            if hasattr(skill,'extra_rate'):
                skill.extra_rate+=self.buff['Suit3_ShengHui']['next_skill_strength']
                self.buff['Suit3_ShengHui']['skill_name']=skill.name
    
    def close(self,character):
        if self.buff['Suit3_ShengHui']['work'] and 'use skill' in character.condition or 'use supper skill' in character.condition:
            self.buff['Suit3_ShengHui']['work'] = False
            character.skill_item[self.buff['Suit3_ShengHui']['skill_name']].extra_rate-=self.buff['Suit3_ShengHui']['next_skill_strength']

class Suit5_ShengHui(Buff):
    def effect(self, character: Character):
        # 初始化 buff 状态
        if 'Suit5_ShengHui' not in self.buff.keys():
            self.buff['Suit5_ShengHui'] = {
                'work': False
            }
            self.buffname=['Nicklace_ShengHui','Wristband_ShengHui','Ring_ShengHui']
        
        if  not self.buff['Suit5_ShengHui']['work']:
            self.buff['Suit5_ShengHui']['work']=True
            character.attribute['boost_points_max']+=10000
            for buffname in self.buffname:
                character.buff[buffname]['attribute_value']*=1.5

class s2(Buff):
    def effect(self, character: Character,skill: Skill):
        # 初始化 buff 状态
        if 's2' not in self.buff.keys():
            self.buff['s2'] = {
                'left_time':0.0,
                'max_time':4.0,
                'max_special_points_consume_rate':0.0,
                'work': False
            }
            self.buff['s2']['max_special_points_consume_rate']=character.attribute['special_points_consume_rate']
        
        if skill is None:
            return  # 若技能为空，不执行

        if not self.buff['s2']['work'] and skill.name=='s2':
            self.buff['s2']['work'] = True
            character.attribute['special_points_consume_rate']=0
            self.buff['s2']['left_time'] = self.buff['s2']['max_time']  # 4秒内不消耗能量
        if self.buff['s2']['left_time'] == 0:
            self.buff['s2']['work'] = False
            character.attribute['special_points_consume_rate']=self.buff['s2']['max_special_points_consume_rate']
            
class passive_stab(Buff):
    #可能会导致没锁住，少了一层
    def effect(self, character: Character):
        # 初始化 buff 状态
        if 'passive_stab' not in self.buff.keys():
            self.buff['passive_stab'] = {
                'work': False,
                'independent_damage_per_layer': 7.0,
                'max_layer':3,
                'max_left_time':20.0,
                'left_time':0,
                'present_layer':0,
                'work':False
            }
        if not self.buff['passive_stab']['work']:
            if ('use skill' in character.condition or 'use supper skill' in character.condition):
                self.buff['passive_stab']['work'] = True

        if ('use skill' in character.condition or 'use supper skill' in character.condition) and self.buff['passive_stab']['work']:
            if self.buff['passive_stab']['present_layer']==3:
                self.buff['passive_stab']['left_time'] = self.buff['passive_stab']['max_left_time']
                return
            else:
                self.buff['passive_stab']['present_layer']+=1
                self.buff['passive_stab']['left_time'] = self.buff['passive_stab']['max_left_time']
                character.attribute['independent_damage']+=self.buff['passive_stab']['independent_damage_per_layer']

        if self.buff['passive_stab']['left_time'] == 0:
            character.attribute['independent_damage']-=self.buff['passive_stab']['independent_damage_per_layer']*self.buff['passive_stab']['present_layer']
            self.buff['passive_stab']['present_layer']=0
            self.buff['passive_stab']['work'] = False

class Suit5_ornament(Buff):
    def effect(self, character: Character):
        if 'Suit5_ornament' not in self.buff:
            self.buff['Suit5_ornament'] = {
                'work': False,
            }

        if self.buff['Suit5_ornament']['work'] == False:
            for item in character.skill_item.values():
                if item.name in ([ str(x*5) for x in range(1,12)]+['s1']+['1']):
                    item.add_level=item.add_level+1
            self.buff["Suit5_ornament"]["work"]=True

class ornament_weapon_2024(Buff):
    def effect(self, character: Character):
        if 'ornament_weapon_2024' not in self.buff:
            self.buff['ornament_weapon_2024'] = {
                'work': False,
            }
        if self.buff['ornament_weapon_2024']['work'] == False:
            for item in character.skill_item.values():
                if item.name in ([ str(x*5) for x in range(1,13)]+['1','s1','s2']):
                    item.add_level=item.add_level+1
            self.buff["ornament_weapon_2024"]["work"]=True

class ornament_weapon_2025(Buff):
    def effect(self, character: Character):
        if 'ornament_weapon_2025' not in self.buff:
            self.buff['ornament_weapon_2025'] = {
                'attribute_name':[
                    'final_damage',
                    'element_strength'
                ],
                'attribute_value':[
                    5,
                    12
                ],
                'left_time':0,
                'cool_time':0,
                'max_cooltime':30,
                'max_left_time':10,
                'level_work': False,
                'attribute_work':False,
            }
        if self.buff['ornament_weapon_2025']['level_work'] == False:
            for item in character.skill_item.values():
                if item.name in ([ str(x*5) for x in range(1,15)]+['1','s1','s2']):
                    item.add_level=item.add_level+1
            self.buff["ornament_weapon_2025"]["level_work"]=True
        
        if 'boost' in character.condition and not self.buff['ornament_weapon_2025']['attribute_work'] and self.buff['ornament_weapon_2025']['cool_time']==0:
            self.buff['ornament_weapon_2025']['attribute_work']=True
            for attribute_name,attribute_value in zip(self.buff['ornament_weapon_2025']['attribute_name'],self.buff['ornament_weapon_2025']['attribute_value']):
                character.attribute[attribute_name]+=attribute_value
            self.buff['ornament_weapon_2025']['left_time'] = self.buff['ornament_weapon_2025']['max_left_time']
            self.buff['ornament_weapon_2025']['cool_time'] = self.buff['ornament_weapon_2025']['max_cooltime']

    def close(self,character:Character):
        if self.buff['ornament_weapon_2025']['left_time']==0 and self.buff['ornament_weapon_2025']['attribute_work']:
            for attribute_name,attribute_value in zip(self.buff['ornament_weapon_2025']['attribute_name'],self.buff['ornament_weapon_2025']['attribute_value']):
                character.attribute[attribute_name]-=attribute_value
            self.buff['ornament_weapon_2025']['attribute_work']=False
class ornament_aureole_2024(Buff):
    ''''
    2024国庆光环
    '''
    def effect(self, character: Character):
        if 'ornament_aureole_2024' not in self.buff:
            self.buff['ornament_aureole_2024'] = {
                'work': False,
            }
        if self.buff['ornament_aureole_2024']['work'] == False:
            for item in character.skill_item.values():
                if item.name in ([ str(x*5) for x in range(9,15)]+['s1','s2']):
                    item.add_level=item.add_level+1
            self.buff["ornament_aureole_2024"]["work"]=True
class ornament_footprint_2024(Buff):
    '''
    2024 51足迹
    '''
    def effect(self, character: Character):
        if 'ornament_footprint_2024' not in self.buff:
            self.buff['ornament_footprint_2024'] = {
                'work': False,
            }
        if self.buff['ornament_footprint_2024']['work'] == False:
            for item in character.skill_item.values():
                if item.name in ([ str(x*5) for x in range(9,13)]+['s1','s2']):
                    item.add_level=item.add_level+1
            self.buff["ornament_footprint_2024"]["work"]=True



class designation_gem(Buff):
    '''
    称号徽记
    鸟1
    
    '''
    def __init__(self, name: str, buff: dict = {}):
        super().__init__(name, buff)
        self.flags=False
    def effect(self, character: Character):
        if not self.flags:
            self.flags = True
            for item in character.skill_item.values():
                if hasattr(item, 'add_level'):
                    item.add_level=item.add_level+1
            skill1=character.skill_item.get('65',None)
            skill2=character.skill_item.get('70',None)
            if skill1 is not None:
                skill1.extra_rate+=10
            if skill2 is not None:
                skill2.extra_rate+=10

class Management:
    def __init__(self, equip_list: dict,buff_instance:dict,buff:dict):
        '''
        equip_list 格式: {装备类： 装备名：}\n
        buff_instance: buff接口字典\n
        buff: 各装备共同维护的buff列表
        '''
        # 根据装备列表实例化对应类
        for equip_item in equip_list.values():
            equip_name=equip_item
            buff_instance[equip_name] = self.create_buff_instance(equip_name,buff)
    def create_buff_instance(self, equip_name: str,buff: dict):

        """
        创建并返回对应的 buff 实例
        需要条件生效的buff就添加到下面的map中 永久属性会在character中被装备
        命名规则为 toequip中的键值:对应的类
        """
        
        # 定义一个映射从装备名称到类的映射，可以根据实际情況添加
        class_map = {
            "s2":s2, #二觉固有被动
            "passive_stab":passive_stab, #自生固有被动
            'weapon_final': final_weapon,
            'weapon_final_plus':final_weapon,
            'weapon_god':final_weapon,
            'Helmet_DieWu':Helmet_DieWu,
            'Clothes_DieWu':Clothes_DieWu,
            'Gloves_DieWu':Gloves_DieWu,
            'Trousers_DieWu':Trousers_DieWu,
            'Shoes_DieWu': Shoes_DieWu,
            'Suit3_armor_DieWu': Suit3_DieWu,
            'Suit5_armor_DieWu': Suit5_DieWu,
            'Nicklace_ShengHui':Nicklace_ShengHui,
            'Wristband_ShengHui':Wristband_ShengHui,
            'Ring_ShengHui':Ring_ShengHui,
            'Amulet_ShengHui':Amulet_ShengHui,
            'Seal_ShengHui':Seal_ShengHui,
            'final':treasure_final,
            'Suit3_jewelry_ShengHui':Suit3_ShengHui,
            'Suit5_jewelry_ShengHui':Suit5_ShengHui,
            'ornament_designation_3w':designation_gem, #称号徽记（称号本身为常驻属性，未写effect方法）
            'ornament_designation_2025':designation_gem,
            'ornament_weapon_2024':ornament_weapon_2024, #2024武器
            'ornament_weapon_2025':ornament_weapon_2025, #2025武器
            'ornament_aureole_2024':ornament_aureole_2024, #光环
            'ornament_footprint_2024':ornament_footprint_2024, #足迹 
            'Suit5_ornament_new':Suit5_ornament,
            'Nicklace_SiMang':Nicklace_SiMang,
            'Wristband_SiMang':Wristband_SiMang,
            'Ring_SiMang':Ring_SiMang,
            'Ring_YanMie':Ring_YanMie,
            'Amulet_SiMang':Amulet_SiMang,
            'Amulet_YanMie':Amulet_YanMie,
            'Seal_SiMang':Seal_SiMang,
            'Seal_YanMie':Seal_YanMie,
            'Suit5_jewelry_SiMang':Suit5_SiMang,
            'Suit5_jewelry_YanMie':Suit5_YanMie,
            'Nicklace_SiMangPlus':Nicklace_SiMangPlus,
            'Wristband_SiMangPlus':Wristband_SiMangPlus,
            'Ring_SiMangPlus':Ring_SiMangPlus,
            'Ring_YanMiePlus':Ring_YanMiePlus,
            'Amulet_SiMangPlus':Amulet_SiMangPlus,
            'Amulet_YanMiePlus':Amulet_YanMiePlus,
            'Seal_SiMangPlus':Seal_SiMangPlus,
            'Seal_YanMiePlus':Seal_YanMiePlus,
            'Suit5_jewelry_SiMangPlus':Suit5_SiMangPlus,
            'Suit5_jewelry_YanMiePlus':Suit5_YanMiePlus
        }

        # 根据装备名获取对应的类，并实例化
        buff_class = class_map.get(equip_name)
        if buff_class:
            return buff_class(equip_name,buff)

    def manage(self, character: Character,skill:Skill):
        """循环执行每个 buff 实例的 effect 方法"""
        for buff_name, buff_instance in character.buff_instance.items():
            if buff_instance!=None:
                if hasattr(buff_instance,'effect'):
                    argspec = inspect.getfullargspec(buff_instance.effect)
                    if 'skill' in argspec.args:
                        buff_instance.effect(character,skill)
                    else:
                        buff_instance.effect(character)
    def close(self, character: Character):
        """循环执行每个 buff 实例的 close 方法"""
        for buff_name, buff_instance in character.buff_instance.items():
            if buff_instance!= None and hasattr(buff_instance,'close'):
                buff_instance.close(character)


#统一用英文算了
class BuffName_Change:
    '''
    持续类buff名的映射
    buff字典键名、技能字典键名、属性字典键名用中文 其他用英文
    '''
    def __init__(self):
        self.mapping={
            'atk':'攻击力',
            'supper_atk':'破防攻击',
            'atk_rate':'攻击力%',
            'def':'防御力',
            'hp':'基础生命',
            'strength':'力量',
            'strength_rate':'力量百分比',
            'crit_rate':'暴击率',
            'crit_damage':'暴击伤害',
            'element_strength':'属性强化',
            'final_damage':'伤害提升',
            'skill_damage':'技能伤害',
            'normal_damage':'普攻伤害',
            'condition_damage':'条件增伤',
            'boss_damage':'克制伤害',
            'element_damage':'属性伤害',
            'additional_damage':'附加伤害',
            'independent_damage':'独立增伤',
            'boosting_damage':'共鸣期间伤害',
            'boost_points':'共鸣点数',
            'boost_points_max':'最大共鸣点数',
            'boosting_time':'共鸣时间',
            'boost_depletion_rate':'共鸣消耗速度',
            'boost_points_rate':'共鸣能量倍率',
            'boost_charge_rate':'共鸣充能效率',
            'Helmet_DieWu':'炫翼蝶舞头带',
            'Clothes_DieWu':'炫翼蝶舞礼服',
            'Glove_DieWu':'炫翼蝶舞手套',
            'Trousers_DieWu':'炫翼蝶舞下装',
            'Shoes_DieWu':'炫翼蝶舞礼鞋',
            'Diewu2':'炫翼蝶舞二件套',
            'Diewu3':'炫翼蝶舞三件套',
            'Diewu5':'炫翼蝶舞五件套',
        }