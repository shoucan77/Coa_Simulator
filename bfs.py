from queue import PriorityQueue,Queue
from battle import Battle
from character import Character
import buff
from pats_management import pats_management
from inscription_manager import inscription_manager
import copy


class OptimizedBattle(Battle):
    def __init__(self,total_time,tick_scale,character):
        super().__init__(total_time,tick_scale,character)
        self.buff_manager=buff.Management(self.character.equipped_item,self.character.buff_instance,self.character.buff)
        self.buff_manager.manage(self.character,skill=None)
        self.pats_manager=pats_management(self.character)
        self.ins_manager=inscription_manager(self.character)
    
    def __lt__(self, other):
        # 这里只需确保返回一个布尔值，应该使得比较逻辑适用于需求
        return id(self) < id(other)  # 简单方案，比较对象ID

    def battle(self,ops_code):
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
        buff_manager=self.buff_manager
        buff_manager.manage(self.character,skill=None)
        pats_manager=self.pats_manager
        ins_manager=self.ins_manager
        #初始化boost技能情况
        self.boost_points_process(0,0)
        ops_code=self.trans_code(ops_code)
        cost_time=0
        present_damage=0
        hit =0
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

        self.skill_cooltime_process(cost_time) #处理技能冷却
        self.pats_cooltime_process() #宠物的显示处理 技能冷却给宠物类自己管理
        self.process_interval(hit,cost_time)#更新间隔变化
        self.speacil_points_process() #魔偶能量处理
        self.buff_time_manage(cost_time) #buff冷却处理

        return present_damage,cost_time
    

    def able_dict_process(self):
        '''
        建立操作码与实际技能序列的对应关系
        要在able_dict变更后才能执行
        '''
        # 定义 副技能操作码与实际技能序列的对应关系
        mapping={
            '6':'1',
            '7':'2',
            '8':'3',
            '9':'4',
            '10':'5',
            'E2':'E'
        }
        #建立实际的可用操作列表
        ops=[]
        able_dict=self.able_dict
        for opscode,item in able_dict.items():
            if 'position' in item and item['position'] in ['主1', '主2', '主3', '主4', '主5','主E','A','B','Q'] and item['available']:
                ops.append(opscode)
            elif 'position' in item and item['position'] in ['副1', '副2', '副3', '副4', '副E','副5'] and item['available']:
                ops.append(mapping.get(opscode,opscode))

        return ops
    

    def trans_code(self,code):
        '''
        读取操作码并返回
        '''
        mapping={
            '1':'6',
            '2':'7',
            '3':'8',
            '4':'9',
            '5':'10',
            'E':'E2',
            'Q':'Q'
        }
        if code in ['1','2','3','4','5','E','Q','A','B']:
            if self.able_dict[code]['available']:
                return code
            elif self.able_dict[mapping[code]]['available']:
                return mapping[code]
        else:
            print('无效操作')

def bfs(init_battle: OptimizedBattle):
    '''
    广度优先搜索（BFS）算法，用于在给定的战斗状态中优化技能序列以最大化伤害。

    参数：
    init_battle: OptimizedBattle 实例，初始战斗状态。

    返回：
    最大损伤和最佳操作序列。
    '''
    # 处理可用操作并初始化
    init_battle.boost_points_process(0, 0)  # 开局打出共鸣的情况
    init_code = init_battle.able_dict_process()
    init_ops_sequence = []
    init_damage_estimate = -272352720000
    
    queue = PriorityQueue()
    max_damage = 0
    best_sequence = []

    # 放入初始状态：(dps，累计伤害, 已过时间, 战斗实例, 可用操作, 操作序列)
    queue.put((0,0, 0, init_battle, init_code, init_ops_sequence))
    total_cnt=0

    while not queue.empty():
        dps,total_damage, total_time, battle_class, able_ops, ops_sequence = queue.get()
        #battle_class = copy.deepcopy(battle_class)
        #able_ops = copy.deepcopy(able_ops)
        #ops_sequence = copy.deepcopy(ops_sequence)
        total_cnt+=1
        if total_cnt%100==0:
            print(f'已处理{total_cnt}个状态...',end='\r')
        
        # 对那些达到最大伤害无望的节点进行剪枝操作
        if cut_tree(dps,total_damage, total_time, battle_class, able_ops, ops_sequence,init_damage_estimate):
            continue

        # 遍历能执行的操作
        for opcode in able_ops:
            # 调用战斗处理，计算伤害和时间成本
            battle_class_new=copy.deepcopy(battle_class)
            ops_sequence = copy.deepcopy(ops_sequence)
            present_damage, cost_time = battle_class_new.battle(opcode)
            
            # 计算新的总伤害和总时间
            new_total_damage = total_damage - present_damage  # 假设伤害为正值
            new_total_time = total_time + cost_time

            # 如果超出总时间限制，继续下一个操作
            if new_total_time >= battle_class_new.total_time:
                continue

            # 更新可用操作状态
            new_able_ops = battle_class_new.able_dict_process()

            # 新操作序列
            new_ops_sequence = ops_sequence + [opcode]

            # 更新最大损伤
            if new_total_damage < max_damage:
                max_damage = new_total_damage
                best_sequence = new_ops_sequence[:]
                
            #更新dps：
            new_dps=new_total_damage/new_total_time if new_total_time != 0 else 0

            # 将新状态压入队列
            queue.put((new_dps,new_total_damage,new_total_time,  battle_class_new, new_able_ops, new_ops_sequence))

    # 返回最大损伤和最佳操作序列
    return -max_damage, best_sequence

def index_ops(op_sequence,aim):
    '''
    ��找 aim 出现的首次在 op_sequence 中的位置
    '''
    first_index = next((i for i, op in enumerate(op_sequence) if op == aim), None)
    
    return True if first_index is not None else False, first_index

def cut_tree(dps,total_damage, total_time, battle_class, able_ops, ops_sequence,init_damage_estimate):
    # 对那些达到最大伤害无望的节点进行剪枝操作
        ##时间过去2/3但是一半伤害都没有的
        
        if(battle_class.total_time-total_time)<=30 and total_damage > init_damage_estimate/2:
            return True
        
        ##第一波爆发过了伤害还没到1/10的
        if total_time<20 and total_time > 15 and total_damage > init_damage_estimate*0.1:
            return True
        
        ##开局半天都在当蜘蛛侠的
        if total_time>5 and total_damage ==0:
            return True
        
        ##不开共鸣就开觉醒的
        bool1,indexE=index_ops(ops_sequence,'E')
        bool2,indexQ=index_ops(ops_sequence,'Q')
        ###共鸣再觉醒之后的
        if bool1 and bool2 and indexQ>indexE:
            return True
        ###单挂一个觉醒的
        if bool1 and not bool2:
            return True
        
        
        ##不开宠物就开觉醒的
        bool3,index5=index_ops(ops_sequence,'5')
        if bool3 and bool1 and index5>indexE:
            return True
        if  bool1 and not bool3:
            return True
        
        return False