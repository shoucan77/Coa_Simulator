import json
import skill
from skill import normal_atk
#from pats_management import pats_management
#from inscription_manager import inscription_manager
class Character:
    def __init__(self, init_attribute:dict,equipment_list:dict,toequip:dict,skill_list:dict):
        '''
        初始化面板数据
        
        init_attribute:初始面板字典
        
        equipment_list: 装备列表(所有装备):
        equipment_item: 装备了的装备
        
        skill_list: 技能列表:技能等级 技能位置
        
        buff、condition初始化为空
        
        intervals初始化全0
        '''
        self.attribute = init_attribute
        self.attribute_true={} #真实面板
        self.condition=[]
        self.equipment_list = equipment_list #所有装备 {装备类型：{装备名：{各个属性加成}}}
        self.toequip=toequip #需要装备的 {装备类型 装备名}
        self.equipped_item = {} #已经装备的 {装备类型：装备名}
        self.skill_list =skill_list#{技能名:技能位置}
        self.skill_item = {} #技能名：技能对象 字典
        self.pats_skill_item={} #宠物技能名 宠物对象
        self.able_dict={} #当前可操作
        self.buff_instance={} #buff列表 由buff模块添加条目
        self.buff={} #buff字典 管理冷却一类的
        self.inscription={} #铭刻管理
        self.intervals={'hit_cnt':{'total':0 ,'last':0,'present':0},\
                        'time_interval': {'last':0, 'present':0},'boost_point_interval': {'last':0,'present':0}}
        self.reinforcement_grade_strength={18:246,19:300,20:360,21:426,22:497,23:573,24:656,25:743}
        self.reinforcement_grade_amulet={18:695,19:873,20:1084,21:1355,22:1682,23:2065,24:2541,25:3111}
        self.reinforcement_grade_weapon={18:3476,19:4368,20:5420,21:6775,22:8410,23:10326,24:12709,25:15559}
        self.reinforcement_grade_clothes={18:7359,19:8340,20:9403,21:10548,22:11774,23:13164,24:14636,25:16190}
        self.equip_equipment() #装备装备方法
        self.equip_skill() #装备技能方法
    def equip_equipment(self):
        '''
        根据需要装备的列表进行装备 同时修改属性 并将字典合并
        '''
        #装备宠物
        #pats_manager=pats_management(self)
        #pats_manager.effect(self)
        #身上的装备 如装备 徽记一类
        for type,name in self.toequip.items():  #type 装备类别 name 装备名  如type=Helmet name=Helmet_DieWu  或者type=Suit5_jewelry name=ShengHui
            for key in self.equipment_list.keys():#key 装备大类 如normal_equipments
                if type in self.equipment_list[key].keys():#大类字典的键为装备类型
                    if name in self.equipment_list[key][type].keys():  #小类的字典的键为装备名
                        equipment=self.equipment_list[key][type][name]
                        self.dict_add(a=self.attribute,b=equipment)
                        if type in ['Suit2_armor', 'Suit3_armor', 'Suit5_armor','Suit3_jewelry', 'Suit5_jewelry']: #套装的type为Suit2_armor 等等
                            self.equipped_item[type]=f'{type}'+f'_{name}'  #名字改为type_name 如Suit5_jewelry_ShengHui
                        else:
                            self.equipped_item[type]=name
                        break # 找到了就跳出循环
        #装备强化等级
        self.equip_reinforcement()
        #装备上装备的属性 buff
        #装备铭刻
        #insc_manager=inscription_manager(self)
        #避免循环引用 操作移到battle中
        #装备徽记
        self.gem_equip()
        #装备回路和药剂
        self.ohter_equip()
        
    def equip_skill(self):
        mapping={
            '主1':'1',
            '主2':'2',
            '主3':'3',
            '主4':'4',
            '主E':'E',
            '主5':'5',
            '副1':'6',
            '副2':'7',
            '副3':'8',
            '副4':'9',
            '副E':'E2',
            '副5':'10',
            'Q':'Q'
        }
        self.able_dict={key:{'skill_name':'','available':'','type':'','position':''}for key in (mapping[key2] for key2 in mapping.keys())}
        able_dict=self.able_dict
        for skill_name,skill_position in self.skill_list.items():
            able_dict[mapping[skill_position]]['skill_name']=skill_name
            able_dict[mapping[skill_position]]['available'] = mapping[skill_position] in {'1', '2', '3', '4', '5','E'}
            able_dict[mapping[skill_position]]['position']=skill_position

            
            if mapping[skill_position]=='E'or mapping[skill_position]=='E2':
                able_dict[mapping[skill_position]]['type']='supper_skill'
            elif mapping[skill_position]=='5' or mapping[skill_position]=='10':
                able_dict[mapping[skill_position]]['type']='pats_skill'
            elif mapping[skill_position]=='Q':
                able_dict[mapping[skill_position]]['type']='boost_skill'
            else:
                able_dict[mapping[skill_position]]['type']='normal_skill'
        #Done skill类的生成至skill_item 中
        self.skill_instance()
    
    def skill_instance(self):
        with open('skill_list.json','r',encoding='utf-8-sig') as file:
            skill_dict = json.load(file)
        with open('normal_atk.json','r',encoding='utf-8-sig') as file:
            normal_atks = json.load(file)

        for key in self.skill_list.keys(): #装备上普通技能（宠物除外）
            if key in skill_dict:
                attribute=self.attribute
                temp_dict=skill_dict[key]
                temp_dict['attribute']=attribute
                temp_dict['name']=key
                temp_dict['condition']=self.condition
                self.skill_item[key]=skill.Skill(**temp_dict)

        for key,value in normal_atks.items():
            attribute=self.attribute
            temp_dict=value
            temp_dict['attribute']=attribute
            temp_dict['name']=key
            self.skill_item[key]=normal_atk(**temp_dict)
        dic={'skill_name':'A','available':True,'type':'normal_atk','cnt':1,'position':'A'}
        dic2={'skill_name':'break','available':True,'type':'normal_atk','position':'B'}
        self.able_dict['A']=dic
        self.able_dict['B']=dic2
    
    
    def equip_reinforcement(self):
        with open('equip_reinforcement.json','r',encoding='utf-8-sig') as file:
            reinforcement = json.load(file)
        for key,value in reinforcement.items():
            if key in ['Helmet','Gloves','Shoes','Nicklace','Wristband','Ring']:
                self.attribute['strength'] += self.reinforcement_grade_strength[value]
            if key in ['Amulet','Seal']:
                self.attribute['super_atk'] += self.reinforcement_grade_amulet[value]
            if key in ['Clothes','Trousers']:
                self.attribute['hp'] += self.reinforcement_grade_clothes[value]
                self.attribute['vitality'] += self.reinforcement_grade_strength[value]
            if key=='weapon':
                self.attribute['super_atk'] += self.reinforcement_grade_weapon[value]

    
    def gem_equip(self):
        '''
        徽记装备方法
        '''
        with open('gem_dict.json','r',encoding='utf-8-sig') as file:
            gem_dict= json.load(file)
        with open('gem_toequip.json','r',encoding='utf-8-sig') as file:
            gem_toequip= json.load(file)
        for key,value in gem_toequip.items():
            if value in gem_dict.keys():
                self.dict_add(self.attribute,gem_dict[value])
            
        
    def ohter_equip(self):
        '''
        回路和药剂装备方法
        '''
        with open('other_attribute.json','r',encoding='utf-8-sig') as file:
            other_att= json.load(file)
        for value in other_att.values():
            self.dict_add(self.attribute,value)

    def dict_add(self,a, b):
        for key in b:
            if isinstance(b[key], dict):
                self.dict_add(a, b[key])
            else:
                a[key] += b[key]

