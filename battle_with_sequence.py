from battle import Battle
from character import Character
import buff
from pats_management import pats_management
from inscription_manager import inscription_manager
import inspect
class battle_with_sequence(Battle):
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
        buff_manager=buff.Management(self.character.equipped_item,self.character.buff_instance,self.character.buff)
        buff_manager.manage(self.character,skill=None)
        pats_manager=pats_management(self.character)
        ins_manager=inscription_manager(self.character)
        self.boost_points_process(0,0)
        with open('skill_sequence.txt', 'r') as file:
            skill_sequence = file.read().splitlines()
        while len(skill_sequence)>0:
            ops_code=skill_sequence[0]
            skill_sequence.remove(skill_sequence[0])
            cost_time=0
            hit =0

            if ops_code in self.able_dict.keys() and self.able_dict[ops_code]['available']:
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
                print('技能不匹配，请重新录入序列')
                return

            self.skill_cooltime_process(cost_time) #处理技能冷却
            self.pats_cooltime_process() #宠物的显示处理 技能冷却给宠物类自己管理
            self.process_interval(hit,cost_time)#更新间隔变化
            self.speacil_points_process() #魔偶能量处理
            self.buff_time_manage(cost_time) #buff冷却处理 
        self.display(total_damage,present_time)