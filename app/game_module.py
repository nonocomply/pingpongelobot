import json
from math import sqrt


class Game:
    def __init__(
        self, id_player1: str, id_player2: str, score_player1: str, score_player2: str
    ) -> None:
        self.id_player1 = int(id_player1)
        self.id_player2 = int(id_player2)
        self.score_player1 = int(score_player1)
        self.score_player2 = int(score_player2)
        self.game_length = score_player1 + score_player2

        if score_player1 > score_player2:
            self.winner = id_player1
            self.winner_score = score_player1
            self.loser = id_player2
            self.loser_score = score_player2
        else:
            self.winner = id_player2
            self.winner_score = score_player2
            self.loser = id_player1
            self.loser_score = score_player1

    def difference_player1(self) -> int:
        with open("players.json", "r") as file:
            data = json.load(file)

        elo_player1 = int(data["players"][self.id_player1]["elo"])
        elo_player2 = int(data["players"][self.id_player2]["elo"])

        elo_difference_player_1 = elo_player1 - elo_player2

        return elo_difference_player_1

    def difference_player2(self) -> int:
        with open("players.json", "r") as file:
            data = json.load(file)

        elo_player1 = int(data["players"][self.id_player1]["elo"])
        elo_player2 = int(data["players"][self.id_player2]["elo"])

        elo_difference_player_2 = elo_player2 - elo_player1

        return elo_difference_player_2

    def expected_winner_points_player1(self) -> float:
        chance = 1 / (1 + 10 ** (self.difference_player2() / 400))

        return round(chance, 1)

    def expected_winner_points_player2(self) -> float:
        chance = 1 / (1 + 10 ** (self.difference_player1() / 400))

        return round(chance, 1)

    def winner_points(self) -> int:
        with open("players.json", "r") as file:
            data = json.load(file)

        elo_player1 = int(data["players"][self.id_player1]["elo"])
        elo_player2 = int(data["players"][self.id_player2]["elo"])

        if self.winner == self.id_player1:
            winner_elo = elo_player1 + 18 * (1 - self.expected_winner_points_player1())
            return round(winner_elo)
        else:
            winner_elo = elo_player2 + 18 * (1 - self.expected_winner_points_player2())
            return round(winner_elo)

    def loser_points(self) -> int:
        with open("players.json", "r") as file:
            data = json.load(file)

        elo_player1 = int(data["players"][self.id_player1]["elo"])
        elo_player2 = int(data["players"][self.id_player2]["elo"])

        if self.loser == self.id_player1:
            loser_elo = elo_player1 + 18 * (0 - self.expected_winner_points_player1())
        else:
            loser_elo = elo_player2 + 18 * (0 - self.expected_winner_points_player2())

        return round(loser_elo)

    def update_elo(self) -> None:
        with open("players.json") as file:
            data = json.load(file)

        data["players"][self.winner]["elo"] = self.winner_points()
        data["players"][self.loser]["elo"] = self.loser_points()

        with open("players.json", "w") as file:
            json.dump(data, file, indent=4)

    def update_stats(self) -> None:
        with open("players.json") as file:
            data = json.load(file)

        data["players"][self.winner]["games"] += 1
        data["players"][self.winner]["wins"] += 1
        data["players"][self.winner]["hits"] += self.winner_score
        data["players"][self.winner]["misses"] += self.loser_score

        data["players"][self.loser]["games"] += 1
        data["players"][self.loser]["looses"] += 1
        data["players"][self.loser]["hits"] += self.loser_score
        data["players"][self.loser]["misses"] += self.winner_score

        with open("players.json", "w") as file:
            json.dump(data, file, indent=4)

    def winner_name(self) -> None:
        with open("players.json") as file:
            data = json.load(file)

        return data["players"][self.winner]["first_name"]

    def loser_name(self) -> None:
        with open("players.json") as file:
            data = json.load(file)

        return data["players"][self.loser]["first_name"]

    def winner_elo_gain(self) -> int:
        with open("players.json") as file:
            data = json.load(file)

        return self.winner_points() - data["players"][self.winner]["elo"]

    def loser_elo_lost(self) -> int:
        with open("players.json") as file:
            data = json.load(file)

        return data["players"][self.loser]["elo"] - self.loser_points()


if __name__ == "__main__":
    game1 = Game(0, 1, score_player1=11, score_player2=9)
    print(f"winner id is {game1.winner}")
    print(game1.winner_points())
    print(f"loser id is {game1.loser}")
    print(game1.loser_points())
    print()

    game2 = Game(0, 1, score_player1=9, score_player2=11)
    print(f"winner id is {game2.winner}")
    print(game2.winner_points())
    print(f"loser id is {game2.loser}")
    print(game2.loser_points())
    print()

    game2.update_elo()
    game2.update_info()
