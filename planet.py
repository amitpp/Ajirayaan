from flask import Flask, Blueprint, request

from helper import ajira_config
from schema import environment_config_schema
from flask_expects_json import expects_json



planet_blueprint = Blueprint('planet_blueprint', __name__)

@planet_blueprint.route('/configure', methods=['POST'])
# @expects_json(environment_config_schema)
def configure_environment():
    config = request.json
    if 'config' in ajira_config:
        return {"message":"Environment is already configured, Please use patch to update specic parameters. Here is the current configuration",
                "config": ajira_config}, 403
    else:
        ajira_config["config"] = config
    return ajira_config, 200

@planet_blueprint.route('/', methods=['PATCH'])
def update_environment():
    update = request.json
    for param in update:
        if 'config' in ajira_config:
            if param in ajira_config['config']:
                ajira_config['config'][param] = update[param]
            else:
                return "Invalid param", 403
        else:
            return "Configuration not initialized yet", 403
    if ajira_config['config']['storm']:
        for inventory in ajira_config['rover_config']['inventory']:
            if inventory["type"] == "storm-shield":
                inventory["quantity"] -= 1
    return "Updated Environment", 200
