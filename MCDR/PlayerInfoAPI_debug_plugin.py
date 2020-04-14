import json
"""
这只是一个用于在MCDR测试UserInfoApi的一个测试插件
使用：!!test
"""


def on_info(server, info):
    if info.content.startswith('!!test') and info.is_player:
        server.logger.info("UserInfoApiDebug:Get plugin instance")
        PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
        server.logger.info("UserInfoApiDebug:Get user info")
        result = PlayerInfoAPI.getPlayerInfo(server, info.player)
        server.logger.info(f"UserInfoApiDebug:Received result (type){type(result)}")
        item = result["Inventory"][result["SelectedItemSlot"]]
        server.reply(info, f"SelectedItemSlotIndex: {result['SelectedItemSlot']}")
        if "tag" in item and "display" in item["tag"]:
            loads = json.loads(item["tag"]["display"]["Name"])
            item_name = loads["text"]
        else:
            item_name = item["id"]
        position = result["Pos"]
        position_show = "[" + str(int(position[0])) + "," + str(int(position[1])) + "," + str(int(position[2])) + "]"
        server.say(f"position_show: {position_show}")
        server.reply(info, f"你手上拿的是 {item_name}")
