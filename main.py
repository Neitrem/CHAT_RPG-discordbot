import sqlite3
import json
import pickle
from classes import *
import sub_functions
import time


def CreateTable() -> NoReturn:
    """Creating database for saving players data
    only if there no database with same name"""

    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users_data(
        id TEXT,
        data_b VARBINARY(2048)
        )""")

    db.commit()  # creating table for players


def AddNewPLayerToDB(player_id: int) -> int:
    """Add new player and save it in the db"""
    # Connecting to the db
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    # Looking for row where id equals to 'player_id'
    sql.execute(f"SELECT id FROM users_data WHERE id = '{player_id}'")

    if sql.fetchone() is None: # If there isn't desired row
        print('Creating new account...')

        # Creating the base inventory list
        new_inventory = [GetItemFromDB(0, 5, 0), GetItemFromDB(2000, 1, 0), GetItemFromDB(1002, 1, 0)]

        # Creating base class obj PLAYER
        new_player = PLAYER(10, 10, 0, 'player', 0,
                            {'dexterity': 1, 'physique': 1, 'intelligence': 1}, 'Player', 10, new_inventory, 0,
                            {'head': None, 'body': None, 'legs': None}, "Start Village", {"Start_Village": 0})

        # Dumps class obj in to bytes line
        new_player_bytes = pickle.dumps(new_player)

        # Save bytes line in the db
        sql.execute(f"INSERT INTO users_data VALUES (?, ?)", (player_id, new_player_bytes))

        # Confirm changes in db
        db.commit()

        return 0  # success
    else: # If desired row already exists
        print('Account have already created')
        return 1  # its already created


def GetPlayerFromDB(player_id: int) -> Optional[PLAYER]:
    """Extruding player from db and creating class object PLAYER"""
    # Connecting to the db
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    # Looking for row where id equals to 'player_id'
    sql.execute(f"""SELECT data_b FROM users_data WHERE id = '{player_id}'""")

    # Save our bytes row from db
    data = sql.fetchone()[0]
    if data is not None: # If player with id equal to 'player_id' exists

        # Refactoring bytes line back in to class obj PLAYER
        player = pickle.loads(data)

        return player
    else: # If it doesn't
        return None


def RewritePLayerDataInDB(player_id: int, player: PLAYER) -> NoReturn:
    """Put new player data to the current row in db"""
    # Connecting to the db
    db = sqlite3.connect('db_player.db')
    sql = db.cursor()

    # Dumps class obj in to bytes line
    player_bytes = pickle.dumps(player)

    # Change data for row where id equal to 'player_id'
    sql.execute('''UPDATE users_data SET data_b = ? WHERE id = ?;''', (player_bytes, player_id))

    # Confirm changes in db
    db.commit()


def EquipTool(player_id: int, player: PLAYER, inv_num: int) -> tuple[int, str]:
    """Equip any tool from inventory"""
    if len(player.inventory) >= inv_num: # is there is item with this id in players inventory

        # Gets item from player inventory
        item = player.inventory[inv_num]

        if item.type_.split('.')[0] == 'tool': # If item is a tool
            if player.lvl >= item.lvl: # If player lvl allows to equip this item
                if player.tool is not None: # If there is some tool in tool slot now

                    # Puts the tool from tool slot in the inventory
                    player.inventory.append(player.tool)

                # Puts item in to the tool slot
                player.tool = item

                # Remove item from players inventory
                player.inventory.remove(item)

                # Saves changes
                RewritePLayerDataInDB(player_id, player)

                return 0, f'{item.type_.split(".")[-1]} successfully equipped!'  # success
            else: # If player lvl smaller then tool lvl
                return 3, "Your lvl is to low to use it!" # lvl of item bigger than player lvl
        else: # If this item isn't a tool
            return 2, "It's not a tool!" # cant equip not a tool
    return 1, "Too big number" # in case there no item with this id in inventory


def EquipClothes(player_id: int, player: PLAYER, inv_num: int) -> tuple[int, str]:
    """Equip any clothes from inventory"""
    if len(player.inventory) >= inv_num: # is there is item with this id in players inventory

        # Gets item from player inventory
        item = player.inventory[inv_num]

        if item.type_.split('.')[0] == 'clothes': # If item is a clothes
            if player.lvl >= item.lvl: # If player lvl allows to equip this item
                if player.clothes[item.body_part] is not None: # If there is some clothes in clothes slot now

                    # Puts the clothes from clothes slot in the inventory
                    player.inventory.append(player.clothes[item.body_part])

                # Puts item in to the clothes slot
                player.clothes[item.body_part] = item

                # Remove item from players inventory
                player.inventory.remove(item)

                # Saves changes
                RewritePLayerDataInDB(player_id, player) # save changes

                return 0, f'{item.type_.split(".")[-1]} successfully equipped!'
            else: # If player lvl smaller then tool lvl
                return 3, "Your lvl is to low to use it!" # lvl of item bigger than player lvl
        else: # If this item isn't a tool
            return 2, "It's not a clothes!" # cant equip not a clothes
    return 1, "Too big number" # in case there no item with this id in inventory


def DeEquipTool(player_id: int, player: PLAYER) -> tuple[int, str]:
    """Remove item from tool and place it in the inventory"""
    if player.tool is not None: # If players tool slot isn't empty

        # Puts tool from tool slot in to inventory
        player.inventory.append(player.tool)

        # Makes tool slot empty
        player.tool = None

        # Saves changes
        RewritePLayerDataInDB(player_id, player)

        return 0, "Tool was successfully removed" # success
    else: # If it's empty
        return 1, "There is nothing to remove" # in case there no item in tool


def DeEquipClothes(player_id: int, player: PLAYER, body_part: str = None) -> tuple[int, str]:
    """Remove item from clothes and place it in the inventory"""

    if body_part is not None: # If body part is given
        if body_part in ['head', 'legs', 'body']: # If given body part is correct
            if player.clothes[body_part] is not None: # If this body part slot isn't empty

                # Put clothes from body part slot to inventory
                player.inventory.append(player.clothes[body_part])

                # Makes this body part slot empty
                player.clothes[body_part] = None

                # Saves changes
                RewritePLayerDataInDB(player_id, player)

                return 0, f"Successfully removed item from `{body_part}`!" # success
            else: # If it's empty
                return 1, f"Nothing to remove from `{body_part}`!" # nothing to remove
        else: # If it wrong
            return 2, 'No such body part only `[head, body, legs]`!'
    else: # If body part isn't given

        # Variable for checking if we did something
        flag = False

        for key in list(player.clothes): # Sorts through all body part
            if player.clothes[key] is not None: # If body part slot isn't empty

                # Put clothes from body part slot to inventory
                player.inventory.append(player.clothes[key])

                # Makes this body part slot empty
                player.clothes[key] = None

                # Mark that we did some changes
                flag = True
        if flag: # If we did something
            RewritePLayerDataInDB(player_id, player)
            return 0, "Equipment successfully removed!" # success
        else: # If we didn't
            return 1, "There is nothing to remove!" # nothing to remove


def RemoveFromInventory(player_id: int, player: PLAYER, inv_num: int, amount: int = None) -> int:
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


def getDataFromDb(table_name: str, db_name: str, id_: int) -> dict:
    """Extruding data about item from db"""
    # Connect to db
    db = sqlite3.connect(db_name)
    db.row_factory = sqlite3.Row # For extruding in dict type
    sql = db.cursor()

    # Looking for row where id_ equals to given id_
    sql.execute(f"SELECT id FROM {table_name} WHERE id = '{id_}'")

    if sql.fetchone() is None: # If there isn't row with this id_
        print('Id doesnt exist')
        return {}
    else: # If it exists

        # Gets data from db and convert it to dict
        data = dict(sql.execute(f"SELECT * FROM {table_name} WHERE (id = '{id_}')").fetchone())

    return data


def GetItemFromDB(item_id: int, amount: int, durability: int = None, enchant: dict = None,
                  bonuses: dict = None, effect: dict = None) -> Union[FOOD, POTION, CLOTHES, TOOL]:
    """Create class object by id"""
    # Variable for keeping our class obj
    item_classed: Union[FOOD, POTION, CLOTHES, TOOL] = ClassVar[FOOD, POTION, CLOTHES, TOOL]

    # Var that contains num that specify table
    table_num = item_id // 1000  # 0 < item_id < 3999

    if table_num == 0: # For food table

        # Defines the table name
        table = 'food'

        # Gets data for this item from certain table
        data = getDataFromDb(table, 'items.db', item_id)

        # Change effect if necessary
        if effect is not None:
            data |= {"effect": effect}

        # Set the amount
        data |= {"amount": amount}

        # Creates class obj FOOD by data
        item_classed = FOOD(**data)

    elif table_num == 1: # For clothes table

        # Defines the table name
        table = 'clothes'

        # Gets data for this item from certain table
        data = getDataFromDb(table, 'items.db', item_id)

        # Set enchants
        data |= {"enchant": enchant}

        # Set bonuses
        data |= {"bonuses": bonuses}

        # Set max durability
        data |= {"durability": durability if durability is not None else data['max_durability']}

        # Creates class obj CLOTHES by data
        item_classed = CLOTHES(**data)

    elif table_num == 2: # For tool table

        # Defines the table name
        table = 'tool'

        # Gets data for this item from certain table
        data = getDataFromDb(table, 'items.db', item_id)

        # Set enchants
        data |= {"enchant": enchant}

        # Set bonuses
        data |= {"bonuses": bonuses}

        # Set max durability
        data |= {"durability": durability if durability is not None else data['max_durability']}

        # Creates class obj TOOL by data
        item_classed = TOOL(**data)
    elif table_num == 3: # For potion table

        # Defines the table name
        table = 'potion'

        # Gets data for this item from certain table
        data = getDataFromDb(table, 'items.db', item_id)

        # Change effect if necessary
        if effect is not None:
            data |= {"effect": effect}

        # Creates class obj POTION by data
        item_classed = POTION(**data)

    return item_classed


# Not sure it has it's final variant, maybe then i will make this stuff in other way!
def AddToInventory(player_id: int, player: PLAYER,
                   items_list: List[Union[TOOL, POTION, CLOTHES, FOOD]], amount: int) -> int:
    """add any item to the players inventory or increase amount of this item"""

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


# Not completed yet!
def ChangeLocation(player_id: int, new_location: str):
    """Moving player between two locations"""
    # Connect to the db
    db = sqlite3.connect('map_db.db')
    sql = db.cursor()

    # Get player from db by id
    player = GetPlayerFromDB(player_id)

    if player is not None:

        # Save current player location
        cur_loc = player.cur_loc

        # Delete player from current location
        sql.execute('''UPDATE locations SET players_in = REPLACE(players_in, ?, ?) WHERE name = ?''',
                    (str(player_id) + ",", "", cur_loc))

        # Put player in to new location
        sql.execute('''UPDATE locations SET players_in = CONCAT(players_in, ?) WHERE name = ?''',
                    (str(player_id) + ",", new_location))

        # Count time spended on this location
        player.visited_locs[cur_loc]['time_total'] += time.time()-player.visited_locs[cur_loc]['time_in']

        # Change location in player data
        player.cur_loc = new_location

        if new_location not in list(player.visited_locs): # If it's new location

            # Add new loc to player visited locs and set time in
            player.visited_locs |= {new_location: {"time_total": 0, "time_in": time.time()}}

