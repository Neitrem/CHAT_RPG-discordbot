import sqlite3
import json
import pickle
from classes import *


def CreateTable():
    """Creating database for saving players data
    only if there no database with same name"""

    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users_data(
        id TEXT,
        data_b VARBINARY(2048)
        )""")

    db.commit()  # creating table for players


def AddNewPLayerToDB(player_id):
    """Add new player and save it in the db"""
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute(f"SELECT id FROM users_data WHERE id = '{player_id}'")
    if sql.fetchone() is None:
        print('Creating new account...')

        new_inventory = [GetItemFromDB(0, 5, 0), GetItemFromDB(2000, 1, 0), GetItemFromDB(1002, 1, 0)]
        new_player = PLAYER(10, 10, 0, 'player', 0,
                            {'dexterity': 1, 'physique': 1, 'intelligence': 1}, 'Player', 10, new_inventory, 0, None,
                            {'head': None, 'body': None, 'legs': None}, "Start Village", "Start_Village")
        new_player_bytes = pickle.dumps(new_player)

        sql.execute(f"INSERT INTO users_data VALUES (?, ?)", (player_id, new_player_bytes))
        db.commit()

        return 0  # success
    else:
        print('Account have already created')
        return 1  # its already created


def GetPlayerFromDB(player_id):
    """Extruding player from db and creating class PLAYER"""
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute(f"""SELECT data_b FROM users_data WHERE id = '{player_id}'""")
    data = sql.fetchone()[0]
    if data is not None:
        player = pickle.loads(data)

        return player
    else:
        return None


def RewritePLayerDataInDB(player_id, player):
    """Put new player dataa in the current row in db"""
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    player_bytes = pickle.dumps(player)
    sql.execute('''UPDATE users SET data_b = ? WHERE id = ?;''', (player_bytes, player_id))
    db.commit()


def EquipTool(player_id, player, inv_num):
    """Equip any tool from inventory"""
    if len(player.inventory) >= inv_num: # is there item ith this id
        item = player.inventory[inv_num]
        if item.type_.split('.')[0] == 'tool': # is it a tool
            if player.lvl >= item.lvl: # does can equip it
                if player.tool is not None:
                    player.inventory.append(player.tool)
                player.tool = item
                player.inventory.remove(item)
                RewritePLayerDataInDB(player_id, player) # save changes
                return 0, f'{item.type_.split(".")[-1]} successfully equipped!'  # success
            else:
                return 3, "Your lvl is to low to use it!" # lvl of item bigger than player lvl
        else:
            return 2, "It's not a tool!" # cant equip not a tool
    return 1, "Too big number" # in case there no item with this id in inventory


def DeEquipTool(player_id, player):
    """Remove item from tool and place it in the inventory"""
    if player.tool is not None:
        player.inventory.append(player.tool)
        player.tool = None
        RewritePLayerDataInDB(player_id, player)
        return 0, "Tool was successfully removed" # success
    else:
        return 1, "There is nothing to remove" # in case there no item in tool


def EquipClothes(player_id, player, inv_num):
    """Equip any clothes from inventory"""
    if len(player.inventory) >= inv_num: # is there item ith this id
        item = player.inventory[inv_num]
        if item.type_.split('.')[0] == 'clothes': # is it a clothes
            if player.lvl >= item.lvl: # does can equip it
                if player.clothes[item.body_part] is not None:
                    player.inventory.append(player.clothes[item.body_part])
                player.clothes[item.body_part] = item
                player.inventory.remove(item)

                RewritePLayerDataInDB(player_id, player) # save changes
                return 0, f'{item.type_.split(".")[-1]} successfully equipped!'
            else:
                return 3, "Your lvl is to low to use it!" # lvl of item bigger than player lvl
        else:
            return 2, "It's not a clothes!" # cant equip not a clothes
    return 1, "Too big number" # in case there no item with this id in inventory


def DeEquipClothes(player_id, player, body_part=None):
    """Remove item from clothes and place it in the inventory"""
    if body_part is not None:
        if body_part in ['head', 'legs', 'body']:
            if player.clothes[body_part] is not None:
                player.inventory.append(player.clothes[body_part])
                player.clothes[body_part] = None
                RewritePLayerDataInDB(player_id, player)
                return 0, f"Successfully removed item from `{body_part}`!" # success
            else:
                return 1, f"Nothing to remove from `{body_part}`!" # nothing to remove
        else:
            return 2, 'No such body part only `[head, body, legs]`!'
    else:
        flag = False
        for key in list(player.clothes):
            if player.clothes[key] is not None:
                player.inventory.append(player.clothes[key])
                player.clothes[key] = None
                flag = True
        if flag:
            RewritePLayerDataInDB(player_id, player)
            return 0, "Equipment successfully removed!" # success
        else:
            return 1, "There is nothing to remove!" # nothing to remove


def RemoveFromInventory(player_id, player, inv_num, amount=None):
    """"for removing items from inventory"""
    if len(player.inventory) >= inv_num:
        item = player.inventory[inv_num]
        if item.is_stackable:
            if amount is None:
                player.inventory.remove(item)
            else:
                if item.amount < amount:
                    return 2 # there no that amount of item with this id
                else:
                    item.amount -= amount
                    if item.amount == 0:
                        player.inventory.remove(item)
        else:
            player.inventory.remove(item)

        RewritePLayerDataInDB(player_id, player)  # save changes
        return 0 # success
    return 1 # in case there no item with this id in inventory


def getDataFromDb(table_name, db_name, id_):
    """Extruding data about item from db"""
    db = sqlite3.connect(db_name)
    sql = db.cursor()
    sql.execute(f"SELECT id FROM {table_name} WHERE id = '{id_}'")
    if sql.fetchone() is None:
        print('Id doesnt exist')
        return None
    else:
        data = []
        for i in sql.execute(f"SELECT * FROM {table_name} WHERE (id = '{id_}')").fetchone():
            data.append(i)

    return data


def GetItemFromDB(item_id, amount, durability=None, enchant=None, bonuses=None, effect=None):
    """Create class object by id"""
    item_classed = None
    table_num = item_id // 1000  # 0 < item_id < 3999

    if table_num == 0:
        table = 'food'
        data = getDataFromDb(table, 'items.db', item_id)
        item_classed = FOOD(data[0], f'food.{data[1]}', data[2],
                            amount, data[3], data[6],  data[4],
                            effect=effect)
    elif table_num == 1:
        table = 'clothes'
        data = getDataFromDb(table, 'items.db', item_id)
        item_classed = CLOTHES(data[0], f'clothes.{data[1]}', data[2],
                               amount, data[3],  data[4],
                               data[5],
                               durability if durability is not None else data[6],
                               data[6], data[7], data[8],
                               enchant=enchant,
                               bonuses=bonuses)
    elif table_num == 2:
        table = 'tool'
        data = getDataFromDb(table, 'items.db', item_id)
        item_classed = TOOL(data[0], f'tool.{data[1]}', data[2],
                            amount, data[3], data[4],
                            data[5],
                            durability if durability is not None else data[6],
                            data[6], data[7], data[8], data[9],
                            enchant=enchant,
                            bonuses=bonuses)
    elif table_num == 3:
        table = 'potion'
        data = getDataFromDb(table, 'items.db', item_id)
        item_classed = POTION(data[0], f'potion.{data[1]}', data[2],
                              amount, data[3], data[7], data[4],
                              data[5],
                              data[6] | effect if effect is not None else data[6])

    return item_classed


def AddToInventory(player_id, player, items_list, amount):
    """adding any item to the players inventory or increasing amount of this item"""

    for item in items_list:
        # item = GetItemFromDB(item_id, amount, durability, enchant, bonuses, effect) # class object
        if item.is_stackable and item.effect is None:
            for player_item in player.inventory:
                if player_item.id_ == item.id_:
                    player_item.amount += amount # increasing amount
                    break
        else:
            player.inventory.append(item) # adding new item to the inventory

    RewritePLayerDataInDB(player_id, player)
    return 0  # success


def ChangeLocation(player_id, new_location):
    db = sqlite3.connect('map_db.db')
    sql = db.cursor()

    player = GetPlayerFromDB(player_id)

    sql.execute('''UPDATE locations SET players_in = REPLACE(players_in, ?, ?) WHERE region_id = ?''',
                (player_id + ",", "", player.cur_loc))
    sql.execute('''UPDATE locations SET players_in = CONCAT(players_in, ?) WHERE region_id = ?''',
                (player_id + ",", new_location))
    player.cur_loc = new_location

