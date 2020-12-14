
ajira_config = {"movement_counter": 0, "inventory_max_limit" : 100}


def collect_sample(terrain_type):
    does_not_exist = True
    priority = 1
    quantity = 1
    sample_type = "storm-shield"
    capacity_of_inventory = sum([inventory['quantity'] for inventory in ajira_config['rover_config']['inventory'] ])
    for inventory in ajira_config['rover_config']['inventory']:
        if inventory["type"] == "rock-sample" and  terrain_type == "rock":
            does_not_exist = False
            if capacity_of_inventory < 98:
                inventory["quantity"] += 3
            else:
                is_available = reduce_inventory(2)
                if is_available:
                    inventory["quantity"] += 3
        elif inventory["type"] == "water-sample" and terrain_type == "water":
            does_not_exist = False
            if capacity_of_inventory < 99:
                inventory["quantity"] += 2
            else:
                is_available = reduce_inventory(1)
                if is_available:
                    inventory["quantity"] += 2
        elif inventory["type"] == "storm-shield":
            does_not_exist = False
    if does_not_exist:
        if terrain_type == "rock":
            sample_type = "rock-sample"
            quantity = 3
            priority = 3
        elif terrain_type == "water":
            sample_type = "water-sample"
            quantity = 2
            priority = 2
        inventory = {
            "priority": priority,
            "quantity": quantity,
            "type": sample_type
        }
        ajira_config['rover_config']['inventory'].append(inventory)


def reduce_inventory(priority):
    reduced = 0
    if priority == 2:
        for inventory in ajira_config['rover_config']['inventory']:
            if inventory["type"] == "storm-shield":
                if inventory["quantity"] > 2:
                    inventory["quantity"] -= 3
                    return True
                else:
                    reduced = inventory["quantity"]
                    inventory["quantity"] = 0
            if inventory["type"] == "water-sample":
                if inventory["quantity"] > 2:
                    inventory["quantity"] -= 3
                    return True
                else:
                    reduced += inventory["quantity"]
                    inventory["quantity"] = 0
        if reduced > 2:
            return True
    elif priority == 1:
        for inventory in ajira_config['rover_config']['inventory']:
            if inventory["type"] == "storm-shield":
                if inventory["quantity"] > 1:
                    inventory["quantity"] -= 2
                    return True
    return False


def check_if_destroyed():
    shield = 0
    if 'rover_config' not in ajira_config:
        return False
    for inventory in ajira_config['rover_config']['inventory']:
        if inventory["type"] == "storm-shield":
            shield = inventory["quantity"]
    if 'config' not in ajira_config:
        return False
    if ajira_config['config']['storm'] and shield == -1:
        return True
    return False