from character import Character
from skill import Skill
import random
'''
截至虚无版本的装备
余烬铭刻数据在json的项链，狱主被动在json的印章（未强化数据）、五件套（新增数据）
'''

class Buff:
    def __init__(self, name: str, buff:dict={}):
        self.name=name
        self.buff=buff

class Nicklace_SiMang(Buff):
    def effect(self, character:Character):
        if 'Nicklace_SiMang' not in self.buff.keys():
            self.buff['Nicklace_SiMang'] = {
                'work':False,
                'attribute_name':'crit_damage',
                'attribute_value':1.8,
                'get_flag':True,#是否能够获取层数
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Nicklace_SiMang']['get_flag']:
            self.buff['Nicklace_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Nicklace_SiMang']['layer']+layer<=self.buff['Nicklace_SiMang']['max_layer']:
                self.buff['Nicklace_SiMang']['layer']+=layer
                attribute=self.buff['Nicklace_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Nicklace_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Nicklace_SiMang']['layer']==self.buff['Nicklace_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Nicklace_SiMang']['max_layer']-self.buff['Nicklace_SiMang']['layer']
                    self.buff['Nicklace_SiMang']['layer']=self.buff['Nicklace_SiMang']['max_layer']
                    attribute=self.buff['Nicklace_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Nicklace_SiMang']['attribute_name']]+=attribute

class Wristband_SiMang(Buff):
    def effect(self, character:Character):
        if 'Wristband_SiMang' not in self.buff.keys():
            self.buff['Wristband_SiMang'] = {
                'work':False,
                'attribute_name':'final_damage',
                'attribute_value':1.2,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Wristband_SiMang']['get_flag']:
            self.buff['Wristband_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Wristband_SiMang']['layer']+layer<=self.buff['Wristband_SiMang']['max_layer']:
                self.buff['Wristband_SiMang']['layer']+=layer
                attribute=self.buff['Wristband_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Wristband_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Wristband_SiMang']['layer']==self.buff['Wristband_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Wristband_SiMang']['max_layer']-self.buff['Wristband_SiMang']['layer']
                    self.buff['Wristband_SiMang']['layer']=self.buff['Wristband_SiMang']['max_layer']
                    attribute=self.buff['Wristband_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Wristband_SiMang']['attribute_name']]+=attribute

class Ring_SiMang(Buff):
    def effect(self, character:Character):
        if 'Ring_SiMang' not in self.buff.keys():
            self.buff['Ring_SiMang'] = {
                'work':False,
                'attribute_name1':'skill_damage',
                'attribute_name2':'normal_damage',
                'attribute_value':1.2,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Ring_SiMang']['get_flag']:
            self.buff['Ring_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Ring_SiMang']['layer']+layer<=self.buff['Ring_SiMang']['max_layer']:
                self.buff['Ring_SiMang']['layer']+=layer
                attribute=self.buff['Ring_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Ring_SiMang']['attribute_name1']]+=attribute
                character.attribute[self.buff['Ring_SiMang']['attribute_name2']]+=attribute
            else:
                if self.buff['Ring_SiMang']['layer']==self.buff['Ring_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Ring_SiMang']['max_layer']-self.buff['Ring_SiMang']['layer']
                    self.buff['Ring_SiMang']['layer']=self.buff['Ring_SiMang']['max_layer']
                    attribute=self.buff['Ring_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Ring_SiMang']['attribute_name1']]+=attribute
                    character.attribute[self.buff['Ring_SiMang']['attribute_name2']]+=attribute

class Seal_SiMang(Buff):
    def effect(self, character:Character):
        if 'Seal_SiMang' not in self.buff.keys():
            self.buff['Seal_SiMang'] = {
                'work':False,
                'attribute_name':'boss_damage',
                'attribute_value':1.0,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Seal_SiMang']['get_flag']:
            self.buff['Seal_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Seal_SiMang']['layer']+layer<=self.buff['Seal_SiMang']['max_layer']:
                self.buff['Seal_SiMang']['layer']+=layer
                attribute=self.buff['Seal_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Seal_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Seal_SiMang']['layer']==self.buff['Seal_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Seal_SiMang']['max_layer']-self.buff['Seal_SiMang']['layer']
                    self.buff['Seal_SiMang']['layer']=self.buff['Seal_SiMang']['max_layer']
                    attribute=self.buff['Seal_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Seal_SiMang']['attribute_name']]+=attribute

class Amulet_SiMang(Buff):
    def effect(self, character:Character):
        if 'Amulet_SiMang' not in self.buff.keys():
            self.buff['Amulet_SiMang'] = {
                'work':False,
                'attribute_name':'element_strength',
                'attribute_value':2.6,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Amulet_SiMang']['get_flag']:
            self.buff['Amulet_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Amulet_SiMang']['layer']+layer<=self.buff['Amulet_SiMang']['max_layer']:
                self.buff['Amulet_SiMang']['layer']+=layer
                attribute=self.buff['Amulet_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Amulet_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Amulet_SiMang']['layer']==self.buff['Amulet_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Amulet_SiMang']['max_layer']-self.buff['Amulet_SiMang']['layer']
                    self.buff['Amulet_SiMang']['layer']=self.buff['Amulet_SiMang']['max_layer']
                    attribute=self.buff['Amulet_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Amulet_SiMang']['attribute_name']]+=attribute

class Suit5_SiMang(Buff):
    def effect(self, character:Character):
        if 'Suit5_SiMang' not in self.buff.keys():
            self.buff['Suit5_SiMang'] = {
                'work':False,
                'cool_time':0,
                'left_time':0,
                'max_cool_time':25,
                'max_left_time':10,
                'rate':0.75,
                'layer':0,
                'buff_add':False
                }
            #todo 新改动
        if 'boost' in character.condition and not self.buff['Suit5_SiMang']['work'] and self.buff['Suit5_SiMang']['cool_time']==0:
            self.buff['Suit5_SiMang']['work'] = True
            self.buff['Suit5_SiMang']['layer']=character.buff['Wristband_SiMang']['layer'] #存储层数
            self.buff['Suit5_SiMang']['cool_time']=self.buff['Suit5_SiMang']['max_cool_time']
            self.buff['Suit5_SiMang']['left_time']=self.buff['Suit5_SiMang']['max_left_time']
            for name,item in character.buff.items():
                if name in ['Nicklace_SiMang', 'Wristband_SiMang','Ring_SiMang','Seal_SiMang','Amulet_SiMang']:
                    item['get_flag']=False

        if not self.buff['Suit5_SiMang']['buff_add'] and self.buff['Suit5_SiMang']['work']:
            self.buff['Suit5_SiMang']['buff_add'] = True
            for name,item in character.buff.items():
                if name in ['Nicklace_SiMang', 'Wristband_SiMang','Ring_SiMang','Seal_SiMang','Amulet_SiMang']:
                    if name != 'Ring_SiMang':
                        buff_name=item.get('attribute_name',None)
                        buff_value=item.get('attribute_value',None)
                        if buff_name and buff_value:
                            character.attribute[buff_name]+=self.buff['Suit5_SiMang']['rate']*buff_value*self.buff['Suit5_SiMang']['layer']
                    else:
                        attribute_name1=item.get('attribute_name1',None)
                        attribute_name2=item.get('attribute_name2',None)
                        attribute_value=item.get('attribute_value',None)
                        if attribute_name1 and attribute_name2 and attribute_value:
                            character.attribute[attribute_name1]+=self.buff['Suit5_SiMang']['rate']*buff_value*self.buff['Suit5_SiMang']['layer']
                            character.attribute[attribute_name2]+=self.buff['Suit5_SiMang']['rate']*buff_value*self.buff['Suit5_SiMang']['layer']
        if self.buff['Suit5_SiMang']['left_time']==0 and self.buff['Suit5_SiMang']['work']:
            self.buff['Suit5_SiMang']['work'] = False
            self.buff['Suit5_SiMang']['buff_add'] = False
            for name,item in character.buff.items():
                if name in ['Nicklace_SiMang', 'Wristband_SiMang','Ring_SiMang','Seal_SiMang','Amulet_SiMang']:
                    if name!= 'Ring_SiMang':
                        buff_name=item.get('attribute_name',None)
                        buff_value=item.get('attribute_value',None)
                        buff_layer=item.get('layer',None)
                        if buff_name and buff_value and buff_layer:
                            character.attribute[buff_name]-=(self.buff['Suit5_SiMang']['rate']+1)*buff_value*self.buff['Suit5_SiMang']['layer']
                            item['layer']=0
                            item['get_flag']=True
                    else:
                        attribute_name1=item.get('attribute_name1',None)
                        attribute_name2=item.get('attribute_name2',None)
                        attribute_value=item.get('attribute_value',None)
                        buff_layer=item.get('layer',None)
                        if attribute_name1 and attribute_name2 and attribute_value and buff_layer:
                            character.attribute[attribute_name1]-=(self.buff['Suit5_SiMang']['rate']+1)*buff_value*self.buff['Suit5_SiMang']['layer']
                            character.attribute[attribute_name2]-=(self.buff['Suit5_SiMang']['rate']+1)*buff_value*self.buff['Suit5_SiMang']['layer']
                            item['layer']=0
                            item['get_flag']=True
            self.buff['Suit5_SiMang']['layer']=0


class Nicklace_SiMangPlus(Buff):
    def effect(self, character:Character):
        if 'Nicklace_SiMang' not in self.buff.keys():
            self.buff['Nicklace_SiMang'] = {
                'work':False,
                'attribute_name':'crit_damage',
                'attribute_value':2.2,
                'get_flag':True,#是否能够获取层数
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Nicklace_SiMang']['get_flag']:
            self.buff['Nicklace_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Nicklace_SiMang']['layer']+layer<=self.buff['Nicklace_SiMang']['max_layer']:
                self.buff['Nicklace_SiMang']['layer']+=layer
                attribute=self.buff['Nicklace_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Nicklace_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Nicklace_SiMang']['layer']==self.buff['Nicklace_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Nicklace_SiMang']['max_layer']-self.buff['Nicklace_SiMang']['layer']
                    self.buff['Nicklace_SiMang']['layer']=self.buff['Nicklace_SiMang']['max_layer']
                    attribute=self.buff['Nicklace_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Nicklace_SiMang']['attribute_name']]+=attribute

class Wristband_SiMangPlus(Buff):
    def effect(self, character:Character):
        if 'Wristband_SiMang' not in self.buff.keys():
            self.buff['Wristband_SiMang'] = {
                'work':False,
                'attribute_name':'final_damage',
                'attribute_value':1.4,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Wristband_SiMang']['get_flag']:
            self.buff['Wristband_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Wristband_SiMang']['layer']+layer<=self.buff['Wristband_SiMang']['max_layer']:
                self.buff['Wristband_SiMang']['layer']+=layer
                attribute=self.buff['Wristband_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Wristband_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Wristband_SiMang']['layer']==self.buff['Wristband_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Wristband_SiMang']['max_layer']-self.buff['Wristband_SiMang']['layer']
                    self.buff['Wristband_SiMang']['layer']=self.buff['Wristband_SiMang']['max_layer']
                    attribute=self.buff['Wristband_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Wristband_SiMang']['attribute_name']]+=attribute

class Ring_SiMangPlus(Buff):
    def effect(self, character:Character):
        if 'Ring_SiMang' not in self.buff.keys():
            self.buff['Ring_SiMang'] = {
                'work':False,
                'attribute_name1':'skill_damage',
                'attribute_name2':'normal_damage',
                'attribute_value':1.4,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Ring_SiMang']['get_flag']:
            self.buff['Ring_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Ring_SiMang']['layer']+layer<=self.buff['Ring_SiMang']['max_layer']:
                self.buff['Ring_SiMang']['layer']+=layer
                attribute=self.buff['Ring_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Ring_SiMang']['attribute_name1']]+=attribute
                character.attribute[self.buff['Ring_SiMang']['attribute_name2']]+=attribute
            else:
                if self.buff['Ring_SiMang']['layer']==self.buff['Ring_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Ring_SiMang']['max_layer']-self.buff['Ring_SiMang']['layer']
                    self.buff['Ring_SiMang']['layer']=self.buff['Ring_SiMang']['max_layer']
                    attribute=self.buff['Ring_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Ring_SiMang']['attribute_name1']]+=attribute
                    character.attribute[self.buff['Ring_SiMang']['attribute_name2']]+=attribute

class Seal_SiMangPlus(Buff):
    def effect(self, character:Character):
        if 'Seal_SiMang' not in self.buff.keys():
            self.buff['Seal_SiMang'] = {
                'work':False,
                'attribute_name':'boss_damage',
                'attribute_value':1.2,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Seal_SiMang']['get_flag']:
            self.buff['Seal_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Seal_SiMang']['layer']+layer<=self.buff['Seal_SiMang']['max_layer']:
                self.buff['Seal_SiMang']['layer']+=layer
                attribute=self.buff['Seal_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Seal_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Seal_SiMang']['layer']==self.buff['Seal_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Seal_SiMang']['max_layer']-self.buff['Seal_SiMang']['layer']
                    self.buff['Seal_SiMang']['layer']=self.buff['Seal_SiMang']['max_layer']
                    attribute=self.buff['Seal_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Seal_SiMang']['attribute_name']]+=attribute

class Amulet_SiMangPlus(Buff):
    def effect(self, character:Character):
        if 'Amulet_SiMang' not in self.buff.keys():
            self.buff['Amulet_SiMang'] = {
                'work':False,
                'attribute_name':'element_strength',
                'attribute_value':2.9,
                'get_flag':True,
                'layer':7,
                'max_layer':15
                }
        if 'atk' in character.condition and self.buff['Amulet_SiMang']['get_flag']:
            self.buff['Amulet_SiMang']['work'] = True
            cnt=character.intervals['hit_cnt']['present']
            time=character.intervals['time_interval']['present']
            times=time/0.3
            if times-int(times)>0:
                times=int(times)+1  #持续时间内能触发的次数
            layer=min(times,cnt) #如果cnt>times 则认为可以触发全部
            if self.buff['Amulet_SiMang']['layer']+layer<=self.buff['Amulet_SiMang']['max_layer']:
                self.buff['Amulet_SiMang']['layer']+=layer
                attribute=self.buff['Amulet_SiMang']['attribute_value']*layer
                character.attribute[self.buff['Amulet_SiMang']['attribute_name']]+=attribute
            else:
                if self.buff['Amulet_SiMang']['layer']==self.buff['Amulet_SiMang']['max_layer']:
                    return
                else:
                    layer=self.buff['Amulet_SiMang']['max_layer']-self.buff['Amulet_SiMang']['layer']
                    self.buff['Amulet_SiMang']['layer']=self.buff['Amulet_SiMang']['max_layer']
                    attribute=self.buff['Amulet_SiMang']['attribute_value']*layer
                    character.attribute[self.buff['Amulet_SiMang']['attribute_name']]+=attribute

class Suit5_SiMangPlus(Buff):
    def effect(self, character:Character):
        if 'Suit5_SiMang' not in self.buff.keys():
            self.buff['Suit5_SiMang'] = {
                'work':False, #五件套是否被共鸣开启的指示
                'cool_time':0,
                'left_time':0,
                'max_cool_time':25,
                'max_left_time':10,
                'rate':0.75,
                'layer':0,
                'buff_add':False #buff是否添加的指示
                }
            #todo 新改动
        if 'boost' in character.condition and not self.buff['Suit5_SiMang']['work'] and self.buff['Suit5_SiMang']['cool_time']==0:
            self.buff['Suit5_SiMang']['work'] = True
            self.buff['Suit5_SiMang']['layer']=character.buff['Wristband_SiMang']['layer'] #存储层数
            character.attribute['element_damage']+=5
            self.buff['Suit5_SiMang']['cool_time']=self.buff['Suit5_SiMang']['max_cool_time']
            self.buff['Suit5_SiMang']['left_time']=self.buff['Suit5_SiMang']['max_left_time']
            for name,item in character.buff.items():
                if name in ['Nicklace_SiMang', 'Wristband_SiMang','Ring_SiMang','Seal_SiMang','Amulet_SiMang']:
                    item['get_flag']=False

        if not self.buff['Suit5_SiMang']['buff_add'] and self.buff['Suit5_SiMang']['work']:
            self.buff['Suit5_SiMang']['buff_add'] = True
            for name,item in character.buff.items():
                if name in ['Nicklace_SiMang', 'Wristband_SiMang','Ring_SiMang','Seal_SiMang','Amulet_SiMang']:
                    if name != 'Ring_SiMang':
                        buff_name=item.get('attribute_name',None)
                        buff_value=item.get('attribute_value',None)
                        if buff_name and buff_value:
                            character.attribute[buff_name]+=self.buff['Suit5_SiMang']['rate']*buff_value*self.buff['Suit5_SiMang']['layer']
                    else:
                        attribute_name1=item.get('attribute_name1',None)
                        attribute_name2=item.get('attribute_name2',None)
                        attribute_value=item.get('attribute_value',None)
                        if attribute_name1 and attribute_name2 and attribute_value:
                            character.attribute[attribute_name1]+=self.buff['Suit5_SiMang']['rate']*buff_value*self.buff['Suit5_SiMang']['layer']
                            character.attribute[attribute_name2]+=self.buff['Suit5_SiMang']['rate']*buff_value*self.buff['Suit5_SiMang']['layer']
        if self.buff['Suit5_SiMang']['left_time']==0 and self.buff['Suit5_SiMang']['work']: #buff没时间了 关闭buff
            self.buff['Suit5_SiMang']['work'] = False
            self.buff['Suit5_SiMang']['buff_add'] = False
            character.attribute['element_damage']-=5
            for name,item in character.buff.items():
                if name in ['Nicklace_SiMang', 'Wristband_SiMang','Ring_SiMang','Seal_SiMang','Amulet_SiMang']:
                    if name!= 'Ring_SiMang':
                        buff_name=item.get('attribute_name',None)
                        buff_value=item.get('attribute_value',None)
                        buff_layer=item.get('layer',None)
                        if buff_name and buff_value and buff_layer:
                            character.attribute[buff_name]-=(self.buff['Suit5_SiMang']['rate']+1)*buff_value*self.buff['Suit5_SiMang']['layer']
                            item['layer']=0
                            item['get_flag']=True
                    else:
                        attribute_name1=item.get('attribute_name1',None)
                        attribute_name2=item.get('attribute_name2',None)
                        attribute_value=item.get('attribute_value',None)
                        buff_layer=item.get('layer',None)
                        if attribute_name1 and attribute_name2 and attribute_value and buff_layer:
                            character.attribute[attribute_name1]-=(self.buff['Suit5_SiMang']['rate']+1)*buff_value*self.buff['Suit5_SiMang']['layer']
                            character.attribute[attribute_name2]-=(self.buff['Suit5_SiMang']['rate']+1)*buff_value*self.buff['Suit5_SiMang']['layer']
                            item['layer']=0
                            item['get_flag']=True
            self.buff['Suit5_SiMang']['layer']=0


class Ring_YanMie(Buff):
    def effect(self,character:Character,skill:Skill):
        if 'Ring_YanMie' not in self.buff.keys():
                self.buff['Ring_YanMie'] = {
                    'work':False,
                    'extra_rate':20,
                    'add_extra_rate':False,
                    'skill_name':None,
                    'Suit5_flag':False
                    }
        if not self.buff['Ring_YanMie']['Suit5_flag'] and self.buff.get('Suit5_YanMie',None) is not None:
            self.buff['Ring_YanMie']['extra_rate'] *=1.8
            self.buff['Ring_YanMie']['Suit5_flag'] = True

        if 'boost' in character.condition and not self.buff['Ring_YanMie']['work']:
            self.buff['Ring_YanMie']['add_extra_rate'] = True #T表示还没打出去
            self.buff['Ring_YanMie']['work'] = True
        
        if 'boost' not in character.condition and self.buff['Ring_YanMie']['work']:
            self.buff['Ring_YanMie']['work'] = False
        
        if (('use skill' in character.condition) or ('use supper skill' in character.condition)) and self.buff['Ring_YanMie']['add_extra_rate']:
            if hasattr(skill,'extra_rate'):
                skill.extra_rate+=self.buff['Ring_YanMie']['extra_rate']
                self.buff['Ring_YanMie']['skill_name']=skill.name
    
    def close(self,character:Character):
        if self.buff['Ring_YanMie']['add_extra_rate']:
            self.buff['Ring_YanMie']['add_extra_rate'] = False
            skill_name=self.buff['Ring_YanMie']['skill_name']
            if skill_name:
                character.skill_item[skill_name].extra_rate-=self.buff['Ring_YanMie']['extra_rate']
                

class Seal_YanMie(Buff):
    def effect(self, character:Character):
        if 'Seal_YanMie' not in self.buff.keys():
            self.buff['Seal_YanMie'] = {
                'work':False,
                'left_time':0,
                'attribute_name':'final_damage',
                'attribute_value':13,
                'max_left_time':30,
                'Suit5_flag':False
                }
        
        if not self.buff['Seal_YanMie']['Suit5_flag'] and self.buff.get('Suit5_YanMie',None) is not None:
            self.buff['Seal_YanMie']['attribute_value'] *=1.8
            self.buff['Seal_YanMie']['Suit5_flag'] = True
        
        if 'use pats skill' in character.condition :
            self.work(character)
            character.condition.remove('use pats skill')

    
    def work(self,character:Character):
        if self.buff['Seal_YanMie']['work']==False:
            self.buff['Seal_YanMie']['work'] = True
            self.buff['Seal_YanMie']['left_time'] = self.buff['Seal_YanMie']['max_left_time']
            character.attribute[self.buff['Seal_YanMie']['attribute_name']] += self.buff['Seal_YanMie']['attribute_value']
        else:
            self.buff['Seal_YanMie']['left_time'] = self.buff['Seal_YanMie']['max_left_time']
        rand_num=random.random()

        if character.buff_instance.get('Amulet_YanMie',None) is not None:
            if rand_num<0.5:
                character.buff_instance['Amulet_YanMie'].work(character)

    
    def close(self,character:Character):
        if self.buff['Seal_YanMie']['left_time']==0 and self.buff['Seal_YanMie']['work']:
            character.attribute[self.buff['Seal_YanMie']['attribute_name']] -= self.buff['Seal_YanMie']['attribute_value']
            self.buff['Seal_YanMie']['work'] = False

class Amulet_YanMie(Buff):
    def effect(self, character:Character):
        if 'Amulet_YanMie' not in self.buff.keys():
            self.buff['Amulet_YanMie'] = {
                'work':False,
                'left_time':0,
                'attribute_name':'boss_damage',
                'attribute_value_perlayer':1.5,
                'layer':0,
                'max_layer':10,
                'max_left_time':12,
                'Suit5_flag':False
                }
        if not self.buff['Amulet_YanMie']['Suit5_flag'] and self.buff.get('Suit5_YanMie',None) is not None:
            self.buff['Amulet_YanMie']['attribute_value_perlayer'] *=1.8
            self.buff['Amulet_YanMie']['Suit5_flag'] = True
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            self.work(character)

    def work(self,character:Character):
        if self.buff['Amulet_YanMie']['work']==False:
            self.buff['Amulet_YanMie']['work'] = True
        self.buff['Amulet_YanMie']['left_time'] = self.buff['Amulet_YanMie']['max_left_time']
        if self.buff['Amulet_YanMie']['layer'] < self.buff['Amulet_YanMie']['max_layer']:
            self.buff['Amulet_YanMie']['layer'] += 1
            character.attribute[self.buff['Amulet_YanMie']['attribute_name']] += self.buff['Amulet_YanMie']['attribute_value_perlayer']
        rand_num=random.random()
        if character.buff_instance.get('Seal_YanMie',None) is not None:
            if rand_num<0.5:
                character.buff_instance['Seal_YanMie'].work(character)
    
    def close(self, character:Character):
        if self.buff['Amulet_YanMie']['left_time']==0 and self.buff['Amulet_YanMie']['work']:
            character.attribute[self.buff['Amulet_YanMie']['attribute_name']] -= self.buff['Amulet_YanMie']['attribute_value_perlayer']*self.buff['Amulet_YanMie']['layer']
            self.buff['Amulet_YanMie']['work'] = False
            self.buff['Amulet_YanMie']['layer'] = 0

class Suit5_YanMie(Buff):
    def __init__(self, name: str, buff: dict = {}):
        super().__init__(name, buff)
        self.buff['Suit5_YanMie'] = {
            'work': False
        }
    def effect(self,character:Character):
        if self.buff['Suit5_YanMie']['work']==False:
            self.buff['Suit5_YanMie']['work'] = True
            for value in character.skill_item.values():
                if hasattr(value,'add_level'):
                    value.add_level = value.add_level+1
    

class Ring_YanMiePlus(Buff):
    def effect(self,character:Character,skill:Skill):
        if 'Ring_YanMie' not in self.buff.keys():
                self.buff['Ring_YanMie'] = {
                    'work':False,
                    'extra_rate':25,
                    'add_extra_rate':False,
                    'skill_name':None,
                    'Suit5_flag':False
                    }
        if not self.buff['Ring_YanMie']['Suit5_flag'] and self.buff.get('Suit5_YanMie',None) is not None:
            self.buff['Ring_YanMie']['extra_rate'] *=1.8
            self.buff['Ring_YanMie']['Suit5_flag'] = True

        if 'boost' in character.condition and not self.buff['Ring_YanMie']['work']:
            self.buff['Ring_YanMie']['add_extra_rate'] = True #T表示还没打出去
            self.buff['Ring_YanMie']['work'] = True
        
        if 'boost' not in character.condition and self.buff['Ring_YanMie']['work']:
            self.buff['Ring_YanMie']['work'] = False
        
        if (('use skill' in character.condition) or ('use supper skill' in character.condition)) and self.buff['Ring_YanMie']['add_extra_rate']:
            if hasattr(skill,'extra_rate'):
                skill.extra_rate+=self.buff['Ring_YanMie']['extra_rate']
                self.buff['Ring_YanMie']['skill_name']=skill.name
    
    def close(self,character:Character):
        if self.buff['Ring_YanMie']['add_extra_rate']:
            self.buff['Ring_YanMie']['add_extra_rate'] = False
            skill_name=self.buff['Ring_YanMie']['skill_name']
            if skill_name:
                character.skill_item[skill_name].extra_rate-=self.buff['Ring_YanMie']['extra_rate']


class Seal_YanMiePlus(Buff):
    def effect(self, character:Character):
        if 'Seal_YanMie' not in self.buff.keys():
            self.buff['Seal_YanMie'] = {
                'work':False,
                'left_time':0,
                'attribute_name':'final_damage',
                'attribute_value':16,
                'max_left_time':30,
                'Suit5_flag':False
                }
        
        if not self.buff['Seal_YanMie']['Suit5_flag'] and self.buff.get('Suit5_YanMie',None) is not None:
            self.buff['Seal_YanMie']['attribute_value'] *=1.8
            self.buff['Seal_YanMie']['Suit5_flag'] = True
        
        if 'use pats skill' in character.condition :
            self.work(character)
            character.condition.remove('use pats skill')

    
    def work(self,character:Character):
        if self.buff['Seal_YanMie']['work']==False:
            self.buff['Seal_YanMie']['work'] = True
            self.buff['Seal_YanMie']['left_time'] = self.buff['Seal_YanMie']['max_left_time']
            character.attribute[self.buff['Seal_YanMie']['attribute_name']] += self.buff['Seal_YanMie']['attribute_value']
        else:
            self.buff['Seal_YanMie']['left_time'] = self.buff['Seal_YanMie']['max_left_time']
        rand_num=random.random()

        if character.buff_instance.get('Amulet_YanMie',None) is not None:
            if rand_num<0.5:
                character.buff_instance['Amulet_YanMie'].work(character)

    
    def close(self,character:Character):
        if self.buff['Seal_YanMie']['left_time']==0 and self.buff['Seal_YanMie']['work']:
            character.attribute[self.buff['Seal_YanMie']['attribute_name']] -= self.buff['Seal_YanMie']['attribute_value']
            self.buff['Seal_YanMie']['work'] = False

class Amulet_YanMiePlus(Buff):
    def effect(self, character:Character):
        if 'Amulet_YanMie' not in self.buff.keys():
            self.buff['Amulet_YanMie'] = {
                'work':False,
                'left_time':0,
                'attribute_name':'boss_damage',
                'attribute_value_perlayer':1.8,
                'layer':0,
                'max_layer':10,
                'max_left_time':12,
                'Suit5_flag':False
                }
        if not self.buff['Amulet_YanMie']['Suit5_flag'] and self.buff.get('Suit5_YanMie',None) is not None:
            self.buff['Amulet_YanMie']['attribute_value_perlayer'] *=1.8
            self.buff['Amulet_YanMie']['Suit5_flag'] = True
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            self.work(character)

    def work(self,character:Character):
        if self.buff['Amulet_YanMie']['work']==False:
            self.buff['Amulet_YanMie']['work'] = True
        self.buff['Amulet_YanMie']['left_time'] = self.buff['Amulet_YanMie']['max_left_time']
        if self.buff['Amulet_YanMie']['layer'] < self.buff['Amulet_YanMie']['max_layer']:
            self.buff['Amulet_YanMie']['layer'] += 1
            character.attribute[self.buff['Amulet_YanMie']['attribute_name']] += self.buff['Amulet_YanMie']['attribute_value_perlayer']
        rand_num=random.random()
        if character.buff_instance.get('Seal_YanMie',None) is not None:
            if rand_num<0.5:
                character.buff_instance['Seal_YanMie'].work(character)
    
    def close(self, character:Character):
        if self.buff['Amulet_YanMie']['left_time']==0 and self.buff['Amulet_YanMie']['work']:
            character.attribute[self.buff['Amulet_YanMie']['attribute_name']] -= self.buff['Amulet_YanMie']['attribute_value_perlayer']*self.buff['Amulet_YanMie']['layer']
            self.buff['Amulet_YanMie']['work'] = False
            self.buff['Amulet_YanMie']['layer'] = 0

class Suit5_YanMiePlus(Buff):
    def __init__(self, name: str, buff: dict = {}):
        super().__init__(name, buff)
        self.buff['Suit5_YanMie'] = {
            'work': False
        }
    def effect(self,character:Character):
        if self.buff['Suit5_YanMie']['work']==False:
            self.buff['Suit5_YanMie']['work'] = True
            for value in character.skill_item.values():
                if hasattr(value,'add_level'):
                    value.add_level = value.add_level+1
    
#湮灭的倍率被动没加