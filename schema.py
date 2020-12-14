rover_config_schema = {
"scenarios": [
{
"name": { "type": "string" },
"conditions": [
{
"type": { "type": "string" },
"property": { "type": "string" },
"operator": { "type": "string" },
"value": { "type": "number" }
}
],
"rover": [
{ "is": { "type": "string" } }
]
},
{
"name": { "type": "string" },
"conditions": [
{
"type": { "type": "string" },
"property": { "type": "string" },
"operator": { "type": "string" },
"value": { "type": "string" }
}
],
"rover": [
{
"performs": {
"collect-sample": {
"type": { "type": "string" },
"qty": { "type": "number" }
}
}
}
]
},
{
"name": "encountering-storm",
"conditions": [
{
"type": { "type": "string" },
"property": { "type": "string" },
"operator": { "type": "string" },
"value": { "type": "boolean" }
}
],
"rover": [
{
"performs": {
"item-usage": {
"type": { "type": "string" },
"qty": { "type": "number" }
}
}
}
]
}
],
"states": [
{
"name": { "type": "string" },
"allowedActions": [ "move", "collect-sample" ]
},
{
"name": { "type": "string" },
"allowedActions": [ "collect-sample" ]
}
],
"deploy-point": {
"row": { "type": "number" },
"column": { "type": "number" }
},
"initial-battery": { "type": "number" },
"inventory": [
{
"type": { "type": "string" },
"quantity": { "type": "number" },
"priority": { "type": "number" }
}
]
}



rover_status_schema = {
"rover": {
"location": {
"row": { "type": "number" },
"column": { "type": "number" }
},
"battery": { "type": "number" },
"inventory": { "type": "array" }
},
"environment": {
"temperature": { "type": "number" },
"humidity": { "type": "number" },
"solar-flare": { "type": "boolean" },
"storm": { "type": "boolean" },
"terrain": { "type": "string" }
}
}


environment_config_schema = {
"temperature": { "type": "number" },
"humidity": { "type": "number" },
"solar-flare": { "type": "boolean" },
"storm": { "type": "boolean" },
"area-map": {"type": "array",
             "items": {
                 "type": "array",
                 "items": { "type":"string"}
                }
    }
}