# Ajirayaan
Space rover possible navigation simulations
SpaceRover has some constraints viz. battery level, given mapped area and weather conditions e.g. it can't move in storm.
Environment variables can move only once however Rover's configuration can be done as many times as needed.

Initial Environment Configurations: POST /api/environment/configure

{
"temperature": 60,
"humidity": 65,
"solar-flare": false,
"storm": false,
"area-map": [
[ "dirt", "dirt", "dirt", "water", "dirt" ],
[ "dirt", "dirt", "water", "water", "water" ],
[ "dirt", "dirt", "dirt", "water", "dirt" ],
[ "dirt", "dirt", "dirt", "dirt", "dirt" ],
[ "dirt", "dirt", "dirt", "dirt", "dirt" ]
]
}

Subsequent environment change : PATCH /api/environment
{"storm":true}

Initial Rover configurations: POST /api/rover/configure 

{
"scenarios": [
{
"name": "battery-low",
"conditions": [
{
"type": "rover",
"property": "battery",
"operator": "lte",
"value": 2
}
],
"rover": [
{ "is": "immobile" }
]
},
{
"name": "encountering-water",
"conditions": [
{
"type": "environment",
"property": "terrain",
"operator": "eq",
"value": "water"
}
],
"rover": [
{
"performs": {
"collect-sample": {
"type": "water-sample",
"qty": 2
}
}
}
]
},
{
"name": "encountering-storm",
"conditions": [
{
"type": "environment",
"property": "storm",
"operator": "eq",
"value": true
}
],
"rover": [
{
"performs": {
"item-usage": {
"type": "storm-shield",
"qty": 1
}
}
}
]
}
],
"states": [
{
"name": "normal",
"allowedActions": [ "move", "collect-sample" ]
},
{
"name": "immobile",
"allowedActions": [ "collect-sample" ]
}
],
"deploy-point": {
"row": 3,
"column": 1
},
"initial-battery": 11,
"inventory": [
{
"type": "storm-shield",
"quantity": 1,
"priority": 1
}
]
}



Rover Status: GET /api/rover/status

{
    "environment": {
        "humidity": 65,
        "solar-flare": false,
        "storm": true,
        "temperature": 60,
        "terrain": "dirt"
    },
    "rover": {
        "battery": 10,
        "inventory": [
            {
                "priority": 1,
                "quantity": 0,
                "type": "storm-shield"
            }
        ],
        "location": {
            "column": 1,
            "row": 2
        }
    }
}



Rover Movement: POST /api/rover/move
{"direction":"up"}

PS: Validations not working as of now.
