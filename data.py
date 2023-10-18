from typing import List, Optional

from pydantic import BaseModel, Field

class LootMessageModel(BaseModel):
    XivChatType: int = Field(alias="xivChatType")
    LogKind: int = Field(alias="logKind")
    LogKindName: str = Field(alias="logKindName")
    LootMessageType: int = Field(alias="lootMessageType")
    LootMessageTypeName: str = Field(alias="lootMessageTypeName")
    Message: str = Field(alias="message")
    MessageParts: List[str] = Field(alias="messageParts")
    ItemId: int = Field(alias="itemId")
    ItemName: str = Field(alias="itemName")
    IsHq: bool = Field(alias="isHq")


class KaptureModel(BaseModel):
    Timestamp: int = Field(alias="timestamp")
    LootMessage: LootMessageModel = Field(alias="lootMessage")
    LootEventType: int = Field(alias="lootEventType")
    LootEventTypeName: str = Field(alias="lootEventTypeName")
    IsLocalPlayer: bool = Field(alias="isLocalPlayer")
    PlayerName: str = Field(alias="playerName")
    World: str = Field(alias="world")
    Roll: int = Field(alias="roll")
    TerritoryTypeId: int = Field(alias="territoryTypeId")
    ContentId: int = Field(alias="contentId")
    LootEventId: str = Field(alias="lootEventId")
    ItemName: str = Field(alias="itemName")

class LootModel(BaseModel):
    Item: str = Field(alias="Item")
    Quantity: int = Field(alias="Quantity")

class PlayerLoot(BaseModel):
    Name: str = Field(alias="Name")
    World: str = Field(alias="World")
    LastUpdate: int = Field(alias="LastUpdate")
    Loot: List[LootModel] = Field(alias="Loot")

    def addLoot(self, loot: LootModel):
        exists = False
        for item in self.Loot:
            if item.Item == loot.Item:
                item.Quantity += loot.Quantity
                exists = True
        if not exists:
            self.Loot.append(loot)
