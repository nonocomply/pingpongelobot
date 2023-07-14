import json


class Game:
    '''
    Class contains counting ELO methods and JSON info updates.

    Attributes:
        id_player1 (str): id of first player.
        id_player2 (str): id of second player.
        score_player1 (str): score gained by the first player.
        score_player2 (str): score gained by the second player.

    Note:
        All attributes we taking from user messages, that's why all 
        attributes is str.
    '''

    def __init__(
        self, id_player1: str, id_player2: str, score_player1: str, score_player2: str
    ) -> None:
        '''
        Args:
            id_player1 (str): id of first player.
            id_player2 (str): id of second player.
            score_player1 (str): score gained by the first player.
            score_player2 (str): score gained by the second player.
            winner (int): id of player who scored more points.
            loser (int): id of player who scored less points.
            game_length (int): sum of score both players.
        '''

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
        '''
        Method returns elo difference of first and second players.
        ELO rating info is taking from JSON file.
    
        Returns:
            elo difference between first and second players.
        '''

        with open("players.json", "r") as file:
            data = json.load(file)

        elo_player1 = int(data["players"][self.id_player1]["elo"])
        elo_player2 = int(data["players"][self.id_player2]["elo"])

        elo_difference_player_1 = elo_player1 - elo_player2

        return elo_difference_player_1

    def difference_player2(self) -> int:
        '''
        Method returns elo difference of second and first players. ELO
        rating info is taking from JSON file.
    
        Returns:
            int: elo difference between second and first players.
        '''

        with open("players.json", "r") as file:
            data = json.load(file)

        elo_player1 = int(data["players"][self.id_player1]["elo"])
        elo_player2 = int(data["players"][self.id_player2]["elo"])

        elo_difference_player_2 = elo_player2 - elo_player1

        return elo_difference_player_2

    def expected_winner_points_player1(self) -> float:
        '''
        Method calculating expected ELO points for first player.
    
        Returns:
            float: expected ELO point if first player wins.
        '''

        chance = 1 / (1 + 10 ** (self.difference_player2() / 400))

        return round(chance, 1)

    def expected_winner_points_player2(self) -> float:
        '''
        Method calculating expected ELO points for second player.
    
        Returns:
            float: expected ELO point if second player wins.
        '''

        chance = 1 / (1 + 10 ** (self.difference_player1() / 400))

        return round(chance, 1)

    def winner_points(self) -> int:
        '''
        Method calculating actual ELO points for winner based on expected 
        points and current ELO rating from JSON file.
    
        Returns:
            int: actual ELO points for winner.
        '''

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
        '''
        Method calculating actual ELO points for loser based on expected
        points and current ELO rating from JSON file.
    
        Returns:
            int: actual ELO points for loser.
        '''

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
        """
        Method updates ELO info in JSON file based on results of game.
        """

        with open("players.json") as file:
            data = json.load(file)

        data["players"][self.winner]["elo"] = self.winner_points()
        data["players"][self.loser]["elo"] = self.loser_points()

        with open("players.json", "w") as file:
            json.dump(data, file, indent=4)

    def update_stats(self) -> None:
        """
        Method updates games, wins, looses, hits, misses counts in JSON
        file based on results of game.
        """

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

    def winner_name(self) -> str:
        """
        Method returns winner_name from JSON file.
        
        Returns:
            str: winner name
        """

        with open("players.json") as file:
            data = json.load(file)

        return data["players"][self.winner]["first_name"]

    def loser_name(self) -> str:
        """
        Method returns loser name from JSON file.
        
        Returns:
            str: loser name
        """

        with open("players.json") as file:
            data = json.load(file)

        return data["players"][self.loser]["first_name"]

    def winner_elo_gain(self) -> int:
        """
        Method returns gained ELO from JSON file of player who wins the game.
        
        Returns:
            int: gained ELO for winner.
        """

        with open("players.json") as file:
            data = json.load(file)

        return self.winner_points() - data["players"][self.winner]["elo"]

    def loser_elo_lost(self) -> int:
        """
        Method returns lost ELO from JSON file of player who wins the game.
        
        Returns:
            int: lost ELO for loser.
        """

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
    game2.update_stats()
