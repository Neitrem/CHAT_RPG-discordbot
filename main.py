from classes import *
import sqlite3
import json


def CreateTable():
    """Creating database for saving players data
    only if there no database with same name"""
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id TEXT,
        lvl INT,
        exp BIGINT,
        hp BIGINT,
        max_hp BIGINT,
        base_armour INT,
        coins BIGINT,
        inventory JSON,
        tool JSON,
        clothes JSON,
        stats JSON,
        death_debuffs JSON,
        professions JSON

    )""")
    db.commit()  # creating table for players


def AddNewPLayerToDB(player_id):
    """Add new player and save it in the db"""
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute(f"SELECT id FROM users WHERE id = '{player_id}'")
    if sql.fetchone() is None:
        print('Creating new account...')

        new_inventory = [FOOD(0, 'food.apple', 'common', 5, True, 2),
                         TOOL(10, 'tool.junk_sword', 'common', 1, False, 0, True,
                            1000, 1000, 2, 'slash', 'short'),
                         CLOTHES(20, 'clothes.junk_chestplate', 'common', 1, False, 0, True,
                                 1000, 1000, 1)]
        new_player = PLAYER(10, 10, 0, 'player', 0,
                            {'dexterity': 1, 'physique': 1, 'intelligence': 1}, 'Player', 10, new_inventory)
        new_player_string = new_player.get_string()
        sql.execute(f"INSERT INTO users VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (player_id, new_player_string['lvl'],
                    new_player_string['exp'],
                    new_player_string['hp'],
                    new_player_string['max_hp'],
                    new_player_string['base_armour'],
                    new_player_string['coins'],
                    json.dumps(new_player_string['inventory']),
                    json.dumps(new_player_string['tool']),
                    json.dumps(new_player_string['clothes']),
                    json.dumps(new_player_string['stats']),
                    json.dumps(new_player_string['death_debuffs']),
                    json.dumps(new_player_string['professions'])))
        db.commit()

        return 0 # success
    else:
        print('Account have already created')
        return 1 # its already created


def GetPlayerFromDB(player_id):
    """Extruding player from db and creating class PLAYER"""

    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute(f"SELECT id FROM users WHERE id = '{player_id}'")
    if sql.fetchone() is None:
        print('User with this id doesnt exist')
    else:
        data = []
        for i in sql.execute(f"SELECT * FROM users WHERE (id = '{player_id}')").fetchone():
            data.append(i)

        print(data)

        # creating a list of classes from list of dict of items
        inv = json.loads(data[7])
        inventory = []
        for item in inv:
            class_item = item['type_'].split('.')[0]
            item_classed = None
            if class_item == "food":
                item_classed = FOOD(item['id_'], item['type_'], item['rarity'],
                                    item['amount'], item['is_stackable'], item['amount_hp_reg'])
            elif class_item == 'tool':
                item_classed = TOOL(item['id_'], item['type_'], item['rarity'],
                                    item['amount'], item['is_stackable'], item['lvl'],
                                    item['is_breakable'], item['durability'], item['max_durability'],
                                    item['damage'], item['damage_type'], item['damage_distance'],
                                    item['enchant'], item['bonuses'])
            elif class_item == 'clothes':
                item_classed = CLOTHES(item['id_'], item['type_'], item['rarity'],
                                       item['amount'], item['is_stackable'], item['lvl'],
                                       item['is_breakable'], item['durability'], item['max_durability'],
                                       item['resist'], item['resist_list'], item['enchant'],
                                       item['bonuses'])
            elif class_item == 'potion':
                item_classed = POTION(item['id_'], item['type_'], item['rarity'],
                                      item['amount'], item['is_stackable'], item['ban_use_time'],
                                      item['toxin_lvl'], item['effect'])
            inventory.append(item_classed)

        # creating class object of class TOOL from tool dict
        item_tool = json.loads(data[8])
        tool = None
        if item_tool != {}: # if not empty
            tool = TOOL(['id_'], item_tool['type_'], item_tool['rarity'],
                        item_tool['amount'], item_tool['is_stackable'], item_tool['lvl'],
                        item_tool['is_breakable'], item_tool['durability'], item_tool['max_durability'],
                        item_tool['damage'], item_tool['damage_type'], item_tool['damage_distance'],
                        item_tool['enchant'], item_tool['bonuses'])

        # creating class objects of class CLOTHES from clothes dict
        item_clothes = json.loads(data[9])
        clothes = {'head': None, 'body': None, 'legs': None}
        for key, item in item_clothes:
            cloth_classed = CLOTHES(item['id_'], item['type_'], item['rarity'],
                                    item['amount'], item['is_stackable'], item['lvl'],
                                    item['is_breakable'], item['durability'], item['max_durability'],
                                    item['resist'], item['resist_list'], item['enchant'],
                                    item['bonuses'])
            clothes[key] = cloth_classed
        player = PLAYER(data[3], data[4], data[1], 'player', data[5], json.loads(data[10]), 'Player', data[6],
                        inventory, tool, clothes, data[2], json.loads(data[11]),
                        json.loads(data[12]))

        return player


def RewritePLayerDataInDB(player_id, player):
    """Put new player dataa in the current row in db"""
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    player_string = player.get_string()

    sql.execute(
        '''UPDATE users SET lvl = ?, exp = ?, hp = ?, max_hp = ?, base_armour = ?,
         coins = ?, inventory = ?, tool = ?, clothes = ?, stats = ?, death_debuffs = ?, professions = ? WHERE id = ?;''',
        (player_string['lvl'],
        player_string['exp'],
        player_string['hp'],
        player_string['max_hp'],
        player_string['base_armour'],
        player_string['coins'],
        json.dumps(player_string['inventory']),
        json.dumps(player_string['tool']),
        json.dumps(player_string['clothes']),
        json.dumps(player_string['stats']),
        json.dumps(player_string['death_debuffs']),
        json.dumps(player_string['professions']),
        player_id))
    db.commit()


def EquipTool(player_id, player, item_id):
    for item in player.inventory:
        if item.id_ == item_id:
            if player.tool == {}:
                player.tool = item
                player.inventory.remove(item)
            else:
                player.inventory.append(player.tool)
                player.tool = item
                player.inventory.remove(item)

            RewritePLayerDataInDB(player_id, player)

            return 0 # success
    return 1 # in case there no item with this id in inventory


def Equipa

