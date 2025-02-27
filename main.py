from character import Character
import json
import battle
from buff import Management
import battle_with_sequence
import bfs

if __name__ == "__main__":

    with open('skill_position.json','r',encoding='utf-8-sig') as file:
        skill_list = json.load(file)

    with open('equipment.json','r',encoding='utf-8-sig') as file:
        equipment_list=json.load(file)

    with open('init_attribute.json','r',encoding='utf-8-sig') as file:
        init_attribute = json.load(file)
    for key,values in init_attribute.items():
        init_attribute[key]=float(values)
    with open('to_equip.json','r',encoding='utf-8-sig') as file:
        toequip = json.load(file)

    with open('passive_skill.json','r',encoding='utf-8-sig') as file:
        passive_skill= json.load(file)

    character=Character(init_attribute,equipment_list,toequip,skill_list)
    #equip_effect(character) #装备好装备的被动效果
    manager=Management(passive_skill,character.buff_instance,character.buff)
    #防止循环引用 时装的装备在main中完成

    #时装嫌麻烦，免去了base_attribute和universal的区分  
    #没有刷新冷却的效果认为是全程触发
    #鸟 1技能没用之前 2技能无法进入cd 2技能使用后 2和1异同开始cd 2有两层 15scd 1 43scd

    #todo铭刻效果在main中装备完成

    #simulator=battle.Battle(90,0.1,character)
    #simulator.battle()
    auto_simulater=battle_with_sequence.battle_with_sequence(90,0.1,character)
    auto_simulater.battle()

    #auto_search=bfs.OptimizedBattle(90,0.1,character)
    #max_damage, best_squence=bfs.bfs(auto_search)
    