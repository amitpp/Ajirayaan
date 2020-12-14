from flask import request, Blueprint
from helper import check_if_destroyed, collect_sample
from helper import  ajira_config
from schema import  rover_config_schema, rover_status_schema
from flask_expects_json import expects_json


rover_blueprint = Blueprint('rover_blueprint',  __name__)

@rover_blueprint.route('/configure', methods=['POST'])
# @expects_json(rover_config_schema)
def configure_rover():
    is_yan_destroyed = check_if_destroyed()
    if is_yan_destroyed:
        return "", 404
    rover_config = request.json
    ajira_config['rover_config'] = rover_config
    collect_sample(ajira_config)
    if ajira_config['config']['storm']:
        for inventory in ajira_config['rover_config']['inventory']:
            if inventory["type"] == "storm-shield":
                inventory["quantity"] -= 1
    return ajira_config, 200

@rover_blueprint.route('/move', methods=['POST'])
def move_rover():
    is_yan_destroyed = check_if_destroyed()
    if is_yan_destroyed:
        return "", 404
    direction = request.json
    possible_movement = {
        "up": {"row_change": -1, "column_change":0},
        "down": {"row_change": 1, "column_change":0},
        "left": {"row_change": 0, "column_change":-1},
        "right": {"row_change": 0, "column_change":1}
    }
    col_limit = len(ajira_config['config']['area-map'][0])
    row_limit = len(ajira_config['config']['area-map'])
    if 'rover_config' in ajira_config:
        if ajira_config['rover_config']['initial-battery'] <= 0:
            return 404
        if ajira_config['config']['storm']:
            return {"message": "Cannot move during a storm"}, 428
        if (0 <= ajira_config['rover_config']['deploy-point']['column'] + possible_movement[direction['direction']]['column_change'] <= col_limit):
            ajira_config['rover_config']['deploy-point']['column'] += possible_movement[direction['direction']]['column_change']
        else:
            return {"message": "Can move only within mapped area"}, 428
        if (0 <= ajira_config['rover_config']['deploy-point']['row'] + possible_movement[direction['direction']]['row_change'] <= row_limit):
            ajira_config['rover_config']['deploy-point']['row'] += possible_movement[direction['direction']]['row_change']
        else:
            return {"message": "Can move only within mapped area"}, 428
    else:
        return "rover config not set", 403
    ajira_config['movement_counter'] += 1
    ajira_config['rover_config']['initial-battery'] -= 1
    if ajira_config['movement_counter'] == 10:
        ajira_config['rover_config']['initial-battery'] += 10
        ajira_config['movement_counter'] = 0
    collect_sample(ajira_config)
    return f"Moved in {direction['direction']} direction", 200


@rover_blueprint.route('/status', methods=['GET'])
# @expects_json(rover_status_schema)
def get_rover_status():
    if 'config' not in ajira_config:
        return "Environment config not initialized", 403
    is_yan_destroyed = check_if_destroyed()
    if is_yan_destroyed:
        return "", 404
    if 'rover_config' in ajira_config:
        rover_status = {
            "rover": {
                'location': ajira_config['rover_config']['deploy-point'],
                'battery': ajira_config['rover_config']['initial-battery'],
                'inventory': ajira_config['rover_config']['inventory']
        },
        "environment": {
            "temperature": ajira_config['config']['temperature'],
            "humidity": ajira_config['config']['humidity'],
            "solar-flare": ajira_config['config']['solar-flare'],
            "storm": ajira_config['config']['storm'],
            "terrain": ajira_config['config']['area-map'][ajira_config['rover_config']['deploy-point']['row']]\
                [ajira_config['rover_config']['deploy-point']['column']]
        }
        }
    else:
        return "rover config not set", 403
    return rover_status, 200