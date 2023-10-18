import requests
import json
import lodestonescraper as lss
from data import PlayerLoot

def resend_remind(webhook:str):
    embed = {
        "embeds": [{
            "title": "Resend Reminder",
            "description": "It's been 48 hours since last known update by Money Goblin",
            "color": 13503757,
        }]
    }
    requests.post(webhook, data=json.dumps(embed), headers={'Content-Type': 'application/json'})

def send_to_discord(webhook: str, loot: PlayerLoot):
    # Create an embed object for each Free Company
    embed = {
        "embeds": [{
            "title": lss.getFreeCompanyName(loot.Name, loot.World),
            "description": "<t:" + str(int(loot.LastUpdate//1)) + ":F>",
            "color": 15115589,
            "fields": [],
            "author": {
                "name": loot.Name,
                "icon_url": lss.getIconURL(loot.Name, loot.World)
            }
        }]
    }

    multipliers = {
        "Salvaged Ring": 8000,
        "Salvaged Bracelet": 9000,
        "Salvaged Earring": 10000,
        "Salvaged Necklace": 13000,
        "Extravagant Salvaged Ring": 27000,
        "Extravagant Salvaged Bracelet": 28500,
        "Extravagant Salvaged Earring": 30000,
        "Extravagant Salvaged Necklace": 34500
    }

    total = 0

    fields = []

    for item in loot.Loot:
        fields.append({
            "name": item.Item,
            "value": "{} | {:,}g".format(item.Quantity, multipliers[item.Item] * item.Quantity)
        })
        total += multipliers[item.Item] * item.Quantity
    
    fields.append({"name":"Total Income","value":"{:,}g".format(total)})

    embed["embeds"][0]["fields"] = fields

    requests.post(webhook, data=json.dumps(embed), headers={'Content-Type': 'application/json'})