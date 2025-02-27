from character import Character
import buff
from pats_management import pats_management
from inscription_manager import inscription_manager
import inspect
class Battle:
    def __init__(self,total_time:float,tick_scale:float,character:Character):
        '''
        假如人物类已经完成实例化 装备的永久效果已生效
        '''
        self.present_tick=0
        self.total_time=total_time
        self.tick_scale=tick_scale
        self.left_time=total_time
        self.character=character
        self.able_dict=character.able_dict #假如able字典的格式为 操作码:{技能名: 类型：位置 是否可用：} 类型暂定为4类 普通技能 觉醒技能 共鸣技能 宠物技能
        self.buff=character.buff #假如buff字典的格式为 buff名：{buff内容}
        self.skill_list=character.skill_item#假如技能列表的格式为 技能名：{技能对象}
        self.A_cnt=1 #平A计数器
        #字典为实例字典，实例初始化时，应该将永久效果中的倍率影响考虑入内（本模块不去思考如何实现）
        #技能位置有11种，1-5 主+副 Q
        self.skill_oppo={'主1':'副1','主2':'副2','主3':'副3','主4':'副4','主5':'副5','主E':'副E'}
        self.mapping={
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
    def battle(self):
        '''
        开始战斗\n
        需要实现动态技能和静态技能基类\n
        动态技能基类中需要实现随tick变化的buff期望和打断方法 interrupt(self,buff_dict,op_codes) 根据操作码来实现打断策略(伤害终止、buff增加)\n
        所有技能都要实现共鸣的期望时间计算 共鸣时间/技能持续时间\n
        技能实例化时 需要传入放置的位置 (1-5 主/副)\n
        '''
        total_damage=0.0
        present_time=0.0
        #创建装备buff 宠物buff 铭刻buff管理器
        buff_manager=buff.Management(self.character.equipped_item,self.character.buff_instance,self.character.buff)
        buff_manager.manage(self.character,skill=None)
        pats_manager=pats_management(self.character)
        ins_manager=inscription_manager(self.character)
        #初始化boost技能情况
        self.boost_points_process(0,0)
        #存储技能序列：
        skill_sequence=[]
        #直到时间结束后才停止战斗
        while present_time<self.total_time:
            self.display(total_damage,present_time)
            ops_code=self.input_code()
            cost_time=0
            hit =0
            #存储间隔状态
            skill_sequence.append(ops_code)
            #判断技能是否可用
            if ops_code in self.able_dict.keys() and self.able_dict[ops_code]['available']:
                #判断技能种类
                if self.able_dict[ops_code]['type']== 'normal_skill':
                    present_damage,cost_time,boost_points,hit=self.normal_skill_process(ops_code,buff_manager,pats_manager,ins_manager)
                    total_damage+=present_damage
                    present_time+=cost_time
                    if 'boost' in self.character.condition:
                        self.boost_points_process(0,cost_time)#处理共鸣点数相关
                    else:
                        self.boost_points_process(boost_points,cost_time)#处理共鸣点数相关

                if self.able_dict[ops_code]['type'] == 'supper_skill':
                    present_damage,cost_time,boost_points,hit=self.supper_skill_process(ops_code,buff_manager,pats_manager,ins_manager)
                    total_damage+=present_damage
                    present_time+=cost_time
                    if 'boost' in self.character.condition:
                        self.boost_points_process(0,cost_time)#处理共鸣点数相关
                    else:
                        self.boost_points_process(boost_points,cost_time)#处理共鸣点数相关

                if self.able_dict[ops_code]['type']=='normal_atk':
                    present_damage,cost_time,boost_points,hit=self.normal_atk_process(ops_code,buff_manager,pats_manager,ins_manager)
                    total_damage+=present_damage
                    present_time+=cost_time
                    if 'boost' in self.character.condition:
                        self.boost_points_process(0,cost_time)#处理共鸣点数相关
                    else:
                        self.boost_points_process(boost_points,cost_time)#处理共鸣点数相关

                if self.able_dict[ops_code]['type'] == 'boost_skill':
                    self.boost_skill_process(buff_manager) #处理共鸣技能相关
                if self.able_dict[ops_code]['type'] == 'pats_skill':
                    self.pats_skill_process()
            else:
                print('无效操作')
                skill_sequence.remove(ops_code)

            self.skill_cooltime_process(cost_time) #处理技能冷却
            self.pats_cooltime_process() #宠物的显示处理 技能冷却给宠物类自己管理
            self.process_interval(hit,cost_time)#更新间隔变化
            self.speacil_points_process() #魔偶能量处理
            self.buff_time_manage(cost_time) #buff冷却处理
        # 将列表写入到一个文本文件中
        with open('skill_sequence.txt', 'w') as file:
            for item in skill_sequence:
                file.write(item + '\n')


    def normal_skill_process(self,ops_code:int,buff_manager,pats_manager,ins_manager):
        '''
        返回造成伤害 花费时间 获得的共鸣能量
        '''
        self.A_cnt=1
        #更新状态列表
        self.character.condition.append('use skill')
        self.character.condition.append('atk')
        #提取技能实例
        skill_name=self.able_dict[ops_code]['skill_name']#假如我的self.able_dict[ops_code]['name'] 对于人物技能 格式为 xx xx代表人物技能名
        skill=self.skill_list[skill_name]
        #计算花费时间
        cool_rate=self.character.attribute['cool_speed']/(955+self.character.attribute['cool_speed']*0.5)
        skill.present_cooltime=skill.max_cooltime/(1+skill.extra_cool_rate/100)/(1+cool_rate)
        #应用装备buff
        buff_manager.manage(self.character,skill)
        pats_manager.effect(self.character)
        ins_manager.management(self.character,skill)
        #更新条件增伤：
        self.character.attribute['condition_damage']+=self.character.attribute['skill_damage']
        '''对应操作码类型1-5 主技能1-5 6-10 副技能1-5 Q共鸣 jump跳 sidestep闪避'''
        #更新able列表
        self.able_dict[ops_code]['available']=False
        if self.able_dict[ops_code]['position'] in self.skill_oppo.keys(): #放的是主技能 检查副技能冷却 冷却完毕则替换
            for key,value in self.able_dict.items():
                if self.skill_oppo[self.able_dict[ops_code]['position']]==value['position']: # 找到了副技能
                    skill_name=value['skill_name']
                    if self.skill_list[skill_name].present_cooltime ==0:
                        oppo_opscode=key
                        self.able_dict[oppo_opscode]['available']=True
                        break
        dam,cost,points,hit_cnt=skill.use()
        #关闭相关状态
        self.character.attribute['condition_damage']-=self.character.attribute['skill_damage']
        buff_manager.close(self.character)
        ins_manager.close(self.character,skill)
        pats_manager.close(self.character)
        self.character.condition.remove('use skill')
        self.character.condition.remove('atk')

        return dam,cost,points,hit_cnt

    def supper_skill_process(self,ops_code,buff_manager,pats_manager,ins_manager):
        self.A_cnt=1
        #状态更新
        self.character.condition.append('use supper skill')
        self.character.condition.append('use skill')
        self.character.condition.append('atk')
        #获取技能名与对应的对象
        skill_name=self.able_dict[ops_code]['skill_name']
        skill=self.skill_list[skill_name]
        #技能进入冷却 更新装备状态
        cool_rate=self.character.attribute['cool_speed']/(955+self.character.attribute['cool_speed']*0.5)
        skill.present_cooltime=skill.max_cooltime/(1+skill.extra_cool_rate/100)/(1+cool_rate)
        buff_manager.manage(self.character,skill)
        pats_manager.effect(self.character)
        ins_manager.management(self.character,skill)
        self.character.attribute['condition_damage']+=self.character.attribute['skill_damage']
        

        #更新able列表
        self.able_dict[ops_code]['available']=False
        if self.able_dict[ops_code]['position'] in self.skill_oppo.keys(): #放的是主技能 检查副技能冷却 冷却完毕则替换
            for key,value in self.able_dict.items():
                if self.skill_oppo[self.able_dict[ops_code]['position']]==value['position']: # 找到了副技能
                    skill_name=value['skill_name']
                    if self.skill_list[skill_name].present_cooltime ==0:
                        oppo_opscode=key
                        self.able_dict[oppo_opscode]['available']=True
                        break
        dam,cost,points,hit_cnt=skill.use()
        self.character.attribute['condition_damage']-=self.character.attribute['skill_damage']
        buff_manager.close(self.character)
        pats_manager.close(self.character)
        ins_manager.close(self.character,skill)
        self.character.condition.remove('use supper skill')
        self.character.condition.remove('use skill')
        self.character.condition.remove('atk')
        return dam,cost,points,hit_cnt
    def boost_points_process(self,amp_points:int,cost_time:float):
        '''
        处理共鸣点数\n
        amp_points 获得的共鸣点数\n
        cost_time  技能花费时间\n
        存在问题:当技能放一半共鸣消失后 此时应该有共鸣能量 实际没有
        '''
        if self.character.attribute['boost_points']+amp_points < self.character.attribute['boost_points_max']:
            self.character.attribute['boost_points']+=amp_points#非共鸣状态下会加上共鸣能量，共鸣状态返回值为0
        #检查是否可以开启共鸣
        if self.character.attribute['boost_points']>=20000 and 'boost' not in self.character.condition:
            self.able_dict['Q']['available']=True
        #flag=False #指示共鸣为0的状态是否已经处理过
    
        if 'boost' in self.character.condition:
            if self.character.attribute['boost_points']-self.character.attribute['boost_depletion_rate']*cost_time> 0:
                self.character.attribute['boost_points']-=self.character.attribute['boost_depletion_rate']*cost_time

            else:
                self.character.attribute['boost_points']=0
                self.character.condition.remove('boost')
                self.character.attribute['condition_damage']-=self.character.attribute['boosting_damage']


    def boost_skill_process(self,manager):
        '''
        处理共鸣技能相关\n
        没有时间花费 默认在技能期间开启 追求极限手法
        '''
        self.able_dict['Q']['available']=False
        self.character.condition.append('boost')
        manager.manage(self.character,skill=None)
        self.character.attribute['condition_damage']+=(self.character.attribute['boosting_damage']+20)

    def pats_skill_process(self):
        '''
        处理宠物的触发
        '''
        self.character.condition.append('use pats skill')
        #TODO 将manager添加到函数中来
        name=None
        if self.able_dict['5']['available']:
            name=self.able_dict['5']['skill_name']
            self.able_dict['5']['available']=False
        elif self.able_dict['10']['available']:
            name=self.able_dict['10']['skill_name']
            self.able_dict['10']['available']=False
        else:
            print('技能正在冷却')
        
        
        for key,item in self.character.pats_skill_item.items():
            if item.name==name:
                skill=item
        
        argspec = inspect.getfullargspec(skill.use)
        if  'interval' in argspec.args:
            skill.use(self.character.intervals)
        else:
            skill.use()

    def skill_cooltime_process(self,cost_time):
        '''
        处理技能冷却\n
        cost_time  已经过去的时间
        '''

        #技能名：{技能位置 技能类型：持续/非持续 技能倍率：
        #技能总冷却时间： 当前冷却时间： 持续时间： 动画时间： 获得的共鸣点数：}

        self.boost_points_process(0,0) #防止其他情况造成共鸣增长 及时更新
        name_ops={}
        #建立逆向映射表
        for key,value in self.able_dict.items():
            name_ops[value['skill_name']]=key
        for key,skill in self.skill_list.items():
            if key in ['A1', 'A2', 'A3', 'A4','break']:
                continue
            if skill.present_cooltime>cost_time:
                skill.present_cooltime-=cost_time
            else:
                skill.present_cooltime=0
        
        for key,values in self.skill_list.items():
            if key in ['A1', 'A2', 'A3', 'A4','break']:
                continue
            if values.present_cooltime==0:
                ops=name_ops[values.name]
                self.able_dict[ops]['available']=True

        for key,values in self.able_dict.items():
            if key in ['A','B']:
                continue
            # 寻找位置在主1-主5，E的技能名
            #在list中，用技能名为索引，寻找技能对象
            #如果存在，则检查冷却是否为0
            #如果为0，则在able_dict中，寻找技能名相同的字典，将其available改为True
            #在skill_oppo中，寻找对位的技能，在able_dict中，寻找技能名相同的字典，将其available改为False
            if values['position'] in ['主1','主2','主3','主4','主E']:#,'主5']:
                skill_name=values['skill_name']
                skill=self.skill_list[skill_name]
                if skill.present_cooltime==0:
                    position=self.skill_oppo[values['position']]
                    ops_code=self.mapping[position]
                    self.able_dict[ops_code]['available']=False
    
    def process_interval(self,hit,cost_time):
        #更新间隔变化
        self.character.intervals['hit_cnt']['total']=self.character.intervals['hit_cnt']['present']+hit
        self.character.intervals['hit_cnt']['last']=self.character.intervals['hit_cnt']['present']
        self.character.intervals['time_interval']['last']=0
        self.character.intervals['boost_point_interval']['last']=self.character.intervals['boost_point_interval']['present']

        self.character.intervals['hit_cnt']['present']=hit
        self.character.intervals['time_interval']['present']=cost_time
        self.character.intervals['boost_point_interval']['present']=self.character.attribute['boost_points']
            
    def speacil_points_process(self):
        if 'strength' not in self.character.condition:
            #计算获得的特殊能量
            revive=0.0
            if self.character.attribute['present_special_points']<self.character.attribute['special_points_max']:
                revive=self.character.attribute['special_points_charge_rate']*self.character.intervals['time_interval']['present']
            if self.character.attribute['present_special_points']+revive<self.character.attribute['special_points_max']:
                self.character.attribute['present_special_points']+=revive
            else:
                self.character.attribute['present_special_points']=self.character.attribute['special_points_max']


    def normal_atk_process(self,opscode,buff_manager,pats_manager,ins_manager):
        if opscode =='A':
                #更新状态列表
            self.character.condition.append('normal atk')
            self.character.condition.append('atk')
            #应用装备buff
            buff_manager.manage(self.character,skill=None)
            pats_manager.effect(self.character)
            ins_manager.management(self.character,skill=None)
            self.character.attribute['condition_damage']+=self.character.attribute['normal_damage']
            key=f'A{self.A_cnt}'
            skill=self.character.skill_item[key]
            self.A_cnt%=4
            self.A_cnt+=1
            dam,cost,points,hit_cnt=skill.use()
            self.character.attribute['condition_damage']-=self.character.attribute['normal_damage']
            buff_manager.close(self.character)
            ins_manager.close(self.character,skill=None)
            pats_manager.close(self.character)
            self.character.condition.remove('atk')
            self.character.condition.remove('normal atk')
            return dam,cost,points,hit_cnt
        else:
            self.A_cnt=1
            skill=self.character.skill_item['break']
            if 'strength' in self.character.condition:
                self.character.condition.remove('strength')
            return skill.use()
        
    def buff_time_manage(self,cost_time):
        #buff持续时间
        for value in self.buff.values():
            if 'left_time' in value.keys():
                if value['left_time']-cost_time>0:
                    value['left_time']-=cost_time
                else:
                    value['left_time']=0

            if 'cool_time' in value.keys():
                if isinstance(value['cool_time'], list):
                    for index, item in enumerate(value['cool_time']):
                        if item - cost_time > 0:
                            value['cool_time'][index] -= cost_time  # 有多个冷却时间 修改列表中的每一个值
                        else:
                            value['cool_time'][index] = 0

                else:
                    if value['cool_time']-cost_time>0:
                        value['cool_time']-=cost_time
                    else:
                        value['cool_time']=0
    
    def pats_cooltime_process(self):
        '''
        更新宠物的操作列表显示
        '''
        skill1 = self.character.pats_skill_item['pat1']
        skill2=self.character.pats_skill_item['pat2']
        if skill1.present_cooltime==0:
            self.able_dict['5']['available'] = True
            self.able_dict['10']['available'] = False
        if skill2.present_cooltime==0 and skill1.present_cooltime>0:
            self.able_dict['10']['available'] = True

    def display(self,total_damage,present_time):
        mapping={
            '1':'6',
            '2':'7',
            '3':'8',
            '4':'9',
            '5':'10',
            'E':'E2'
        }
        pats_name={}
        for key,item in self.character.pats_skill_item.items():
            pats_name[item.name]=key
        
        for key, value in self.able_dict.items():
            if key in ['1','2','3','4','5','E','Q','A','B']:
                if self.able_dict[key]['available']:
                    print(f'当前可用：技能{key} 技能{value['skill_name']}')
                elif key!='Q' and self.able_dict[mapping[key]]['available']:
                    print(f'当前可用：技能{key} 技能{self.able_dict[mapping[key]]['skill_name']}')
                else:
                    if value['skill_name'] in self.skill_list.keys():
                        print(f'当前冷却：技能{key} 冷却时间：{self.skill_list[value['skill_name']].present_cooltime}')
                    if value['skill_name'] in pats_name.keys():
                         print(f'当前冷却：宠物{key} 冷却时间：{self.character.pats_skill_item[pats_name[value['skill_name']]].present_cooltime}')
        print(f'当前共鸣能量{self.character.attribute['boost_points']}')
        print(f'当前魔偶能量{self.character.attribute['present_special_points']/self.character.attribute['special_points_max']*100:.4f}%')
        print(f'当前已过{present_time}秒')
        print(f'当前造成伤害{total_damage/100000000:.4f}亿')
    def input_code(self):
        '''
        读取操作码并返回
        '''
        mapping={
            '1':'6',
            '2':'7',
            '3':'8',
            '4':'9',
            '5':'10',
            'E':'E2'
        }
        code=str(input("选择操作："))
        if code in ['1','2','3','4','5','E','Q','A','B']:
            if self.able_dict[code]['available']:
                return code
            elif self.able_dict[mapping[code]]['available']:
                return mapping[code]
        else:
            print('无效操作')