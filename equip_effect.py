import buff as Buff
def equip_effect(character):
            '''
            装备好装备的被动效果
            '''
            mapping={
                'Helmet_DieWu':Buff.Helmet_DieWu,
                'Clothes_DieWu':Buff.Clothes_DieWu,
                'Gloves_DieWu':Buff.Gloves_DieWu,
                'Trousers_DieWu':Buff.Trousers_DieWu,
                'Shoes_DieWu':Buff.Shoes_DieWu,
                'Suit3_armor_DieWu':Buff.Suit3_DieWu,
                'Suit5_armor_DieWu':Buff.Suit5_DieWu
            }
            for values in character.equipped_item.values():
                if values in mapping.keys():
                    temp=mapping[values](name=values,buff=character.buff)
                    temp.effect(character)
                    character.buff_instance[values]=temp
                    