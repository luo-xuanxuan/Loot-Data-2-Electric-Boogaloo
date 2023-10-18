import json
import threading
import time
import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException
from data import KaptureModel, PlayerLoot, LootModel
from discord import send_to_discord, resend_remind

t_stop_event = threading.Event()

queue: List[PlayerLoot] = []

def process_queue(stop_event):
    config = {}
    reminded = False
    with open('config.json', 'r') as f:
        config = json.load(f)
    while not stop_event.is_set():
        if queue:
            if queue[0].LastUpdate + 300 <= time.time():
                send_to_discord(config["webhookURL"], queue.pop(0))
                config["last_resend"] = time.time()
                reminded = False
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=4)
        else:
            if config["last_resend"] + 172800 <= time.time() and not reminded:
                resend_remind(config["webhookURL"])
                reminded = True
            time.sleep(300)
        

def start_thead():
    t = threading.Thread(target=process_queue, args=(t_stop_event,))
    t.daemon = True
    t.start()


def stop_thread():
    # Set the stop event when the program exits
    t_stop_event.set()


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_event_handler("startup", start_thead)
    app.add_event_handler("shutdown", stop_thread)

    return app


app = create_app()

@app.post("/", tags=["upload"])
async def upload(data_array: List[KaptureModel]):
    try:
        for data in data_array:
            if data.TerritoryTypeId not in [423,424,425,653,984]:
                return {"message": "Not in workshop"}
            
            if data.LootMessage.ItemId not in [22500,22501,22502,22503,22504,22505,22506,22507]:
                return {"message": "Not salvage"}
            
            for player in queue:
                if data.PlayerName == player.Name and data.World == player.World:
                    player.LastUpdate = data.Timestamp / 1000
                    player.addLoot(LootModel.parse_obj({
                        "Item":data.LootMessage.ItemName,
                        "Quantity": 1   if len(data.LootMessage.MessageParts[0].split(" ")) == 2
                                        else int(data.LootMessage.MessageParts[0].split(" ")[2])
                    }))
                    with open('example.txt', 'a') as file:
                        # Append a string to the file
                        file.write('\n'+str(player))
                    return {"message": "JSON received"}

            queue.append(PlayerLoot.parse_obj({
                "Name":data.PlayerName,
                "World":data.World,
                "LastUpdate":data.Timestamp / 1000,
                "Loot": [LootModel.parse_obj({
                    "Item":data.LootMessage.ItemName,
                    "Quantity": 1   if len(data.LootMessage.MessageParts[0].split(" ")) == 2
                                    else int(data.LootMessage.MessageParts[0].split(" ")[2])
                })]
            }))

            return {"message": "JSON received"}
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=ex)

if __name__ == '__main__':
    uvicorn.run("app:app",host="0.0.0.0", port=5000)