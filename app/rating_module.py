import json


class Rating:
    def __init__(self) -> int or None:
        pass

    def message_to_player_id(self, message):
        players_list = self.get_players_list()

        if message in players_list:
            return players_list.index(message)
        return -1

    def show_elo_sorted_list(self) -> str:
        with open("players.json", "r") as file:
            data = json.load(file)

        result_list = []
        [
            result_list.append(
                (item.get("first_name"), item.get("elo"), item.get("games"))
            )
            for item in data["players"]
        ]

        result_list = list(sorted(result_list, key=lambda x: x[1], reverse=True))

        result_list = [
            f"{index+1}. Рейтинг игрока <b>{item[0]}</b> - <b>{item[1]}</b>"
            for index, item in enumerate(result_list)
        ]

        for index, item in enumerate(result_list):
            if index == 0:
                result_list[index] = item + " 🥇"
            elif index == 1:
                result_list[index] = item + " 🥈"
            elif index == 2:
                result_list[index] = item + " 🥉"
            else:
                result_list[index] = item

        return "\n\n".join(result_list)

    def get_player_stats(self, player_id: int) -> dict | None:
        with open("players.json", "r") as file:
            data = json.load(file)

        if player_id != -1:
            player_stats: dict = data["players"][player_id]

            return player_stats

        return None

    def player_stats_to_message(self, player_id: int) -> str:
        player_stats = self.get_player_stats(player_id)

        if player_stats["games"] != 0:
            winrate = int(round(player_stats["wins"] / player_stats["games"], 2) * 100)
        else:
            winrate = 0

        if player_stats["hits"] == 0 or player_stats["misses"] == 0:
            hits_misses = 1
        else:
            hits_misses = round(float(player_stats["hits"] / player_stats["misses"]), 3)

        msg = [
            f"👤 Статистика <b>{player_stats['first_name']}</b>\n\n",
            f"🏓 Сыграно сетов - {player_stats['games']}\n",
            f"🏆 Количество побед - {player_stats['wins']}\n",
            f"❌ Количество поражений - {player_stats['looses']}\n",
            f"📊 Винрейт - {winrate}%\n\n"
            f"⚪️ Выйграно очков - {player_stats['hits']}\n",
            f"🔴 Проиграно очков - {player_stats['misses']}\n",
            f"🔘 Точность - {hits_misses}\n\n",
            f"📈 <b>Текущий рейтинг - {player_stats['elo']}</b>",
        ]

        return "".join(msg)

    def get_players_list(self) -> list:
        with open("players.json", "r") as file:
            data = json.load(file)

        players_list = []
        [players_list.append(item.get("first_name")) for item in data["players"]]

        return players_list


if __name__ == "__main__":
    r = Rating()
    r.show_elo_sorted_list()
    print(r.get_players_list())
    print(r.show_elo_sorted_list())
    print(r.get_player_stats(0))
    print(r.message_to_player_id("giorgio"))
