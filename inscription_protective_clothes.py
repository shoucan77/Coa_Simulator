class inscription_protective_clothes_destroy:
    def __init__(self,character):
        self.name = '破坏9'
        self.max_layer=5
        self.layer=0
        self.rate_per_layer = 5
    
    def effect(self, character):
        if 'destroy' not in  character.buff.keys():
            character.buff['destroy']={
                'left_time':0,
                'work':False,
                'cool_time':0
            }
        if 'use skill' in character.condition or 'use supper skill' in character.condition:
            character.buff['destroy']['work']=True
            if self.layer<5:
                self.layer+=1
                character.attribute['final_damage']+=self.rate_per_layer

            character.buff['destroy']['left_time']=2
            
            if character.buff['destroy']['cool_time']==0:
                skill1=character.skill_item.get('s1',None)
                skill2=character.skill_item.get('s2',None)
                skill3=character.skill_item.get('minis',None)
            
                if skill1 is not None:
                    if skill1.present_cooltime>1:
                        skill1.present_cooltime-=1
                    else:
                        skill1.present_cooltime=0
                
                if skill2 is not None:
                    if skill2.present_cooltime>1:
                        skill2.present_cooltime-=1
                    else:
                        skill2.present_cooltime=0
                
                if skill3 is not None:
                    if skill3.present_cooltime>1:
                        skill3.present_cooltime-=1
                    else:
                        skill3.present_cooltime=0
    def close(self,character):
        if character.buff['destroy']['left_time']==0 and character.buff['destroy']['work']:
            att_value=self.layer*self.rate_per_layer
            self.layer=0
            character.attribute['final_damage']-=att_value
            character.buff['destroy']['work']=False

class inscription_protective_clothes_aloof:
    def __init__(self, character):
        self.name='超然9'
        for key,value in character.skill_item.items():
            if hasattr(value,'extra_rate'):
                value.extra_rate+=10
        skill1=character.skill_item.get('s1',None)
        skill2=character.skill_item.get('s2',None)
        skill3=character.skill_item.get('minis',None)

        for value in character.skill_item.items():
            if hasattr(value,'extra_rate'):
                value.extra_rate+=10
        
        if skill1 is not None:
            skill1.inde_rate+=30
            skill1.special_points_cost*=2
        if skill2 is not None:
            skill2.inde_rate+=30
            skill2.special_points_cost*=2
        if skill3 is not None:
            skill3.inde_rate+=30
            skill3.special_points_cost*=2
            
        character.buff['s2']['max_time']=15.0
            
class inscription_protective_clothes_adapt:
    def __init__(self, character):
        self.name='适应9'
        for key,value in character.able_dict.items():
            if 'position' in value and value['position'] in ['主1', '主2', '主3', '主4', '主E']:
                name=value.get('skill_name',None)
                skill=character.skill_item[name]
                if skill is not None:
                    skill.extra_rate+=18
        character.buff['adapt9']={
            'cool_time':[0,0],#一个给使用主计时，一个使用副计时
            'max_cooltime':8
        }
        self.skillmap={'main':[],'secondly':[]}
        for key,value in character.able_dict.items():
            if 'position' in value and value['position'] in ['主1', '主2', '主3', '主4', '主E']:
                self.skillmap['main'].append(value['skill_name'])
            if 'position' in value and value['position'] in  ['副1', '副2', '副3', '副4', '副E']:
                self.skillmap['secondly'].append(value['skill_name'])
    def effect(self, character,skill):
        if hasattr(skill,'name'):
            name=skill.name#技能名
        else:
            return
        #得到技能对应的位置
        for value in character.able_dict.values():
            if 'skill_name' in value and value['skill_name']==name:
                position=value['position']
        if position in ['主1', '主2', '主3', '主4', '主E']:
            Key='main'
            if character.buff['adapt9']['cool_time'][0]>0:
                return
            else:
                for name in self.skillmap['secondly']:
                    character.skill_item[name].present_cooltime=max(character.skill_item[name].present_cooltime-1.5,0)
                character.buff['adapt9']['cool_time'][0]=character.buff['adapt9']['max_cooltime']
                return
        if position in  ['副1', '副2', '副3', '副4', '副E']:
            key='secondly'
            if character.buff['adapt9']['cool_time'][1]>0:
                return
            else:
                for name in self.skillmap['main']:
                    character.skill_item[name].present_cooltime=max(character.skill_item[name].present_cooltime-1.5,0)
                character.buff['adapt9']['cool_time'][1]=character.buff['adapt9']['max_cooltime']
                return

class inscription_protective_clothes_quick:
    def __init__(self, character):
        self.name='迅捷3'
        character.attribute['cool_speed']+=30