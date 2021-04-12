import random
from statistics import mode
import matplotlib.pyplot as plt
from pylint.lint import Run


class Tournament():

    def __init__(self, player1, player2, number_of_games):
        self.player1 = player1
        self.player2 = player2
        self.number_of_games = number_of_games

    def arrange_singlegame(self):
        print(self.player1.receive_result(self.player2))
        print("Player1: ", self.player1.points)
        print("Player2: ", self.player2.points)
        self.player1.reset()
        self.player2.reset()

    def arrange_tournament(self):
        for i in range(self.number_of_games):
            print(self.player1.receive_result(self.player2))

        print("Player 1: ", self.player1.points)
        print("Player 2: ", self.player2.points)

        self.player1.plot_graph()

        self.player1.reset()
        self.player2.reset()


class Player():

    def __init__(self, name):

        names = ["random", "sequential", "mostcommon", "historian"]
        if not names.__contains__(str(name).lower()):
            print("Invalid name")

        self.name = str(name).lower()
        self.points = 0
        self.sequential_counter = 0
        self.opponent_choices = []
        self.remember = 0
        self.number_of_games = 0
        self.graph = []

    def select_action(self):
        action = None

        if self.name == "random":
            action = random.randint(0, 2)

        elif self.name == "sequential":
            self.sequential_counter = self.sequential_counter % 3
            action = self.sequential_counter
            self.sequential_counter += 1

        elif self.name == "mostcommon":
            if len(self.opponent_choices) == 0:
                action = random.randint(0, 2)
            else:
                action = (mode(self.opponent_choices) + 2) % 3

        elif self.name == "historian":
            if len(self.opponent_choices) > self.remember:
                next_play_counter = [0, 0, 0]
                for i in range(len(self.opponent_choices) - self.remember):
                    if self.opponent_choices[i: i + self.remember] == \
                            self.opponent_choices[-self.remember:]:
                        next_play_counter[self.opponent_choices[i + self.remember]] += 1

                action = (next_play_counter.index(max(next_play_counter)) + 2) % 3

            else:
                action = random.randint(0, 2)

        print(action)
        return action

    def receive_result(self, opponent):
        player1 = self.select_action()
        player2 = opponent.select_action()

        self.number_of_games += 1
        opponent.number_of_games += 1

        self.opponent_choices.append(player2)
        opponent.opponent_choices.append(player1)

        if player1 == player2:
            self.points += 0.5
            opponent.points += 0.5
            self.graph.append(self.points)
            opponent.graph.append(opponent.points)
            return "Draw"

        if (player1 + 1) % 3 == player2:
            self.points += 1
            self.graph.append(self.points)
            opponent.graph.append(opponent.points)
            return "Player 1"

        opponent.points += 1
        self.graph.append(self.points)
        opponent.graph.append(opponent.points)
        return "Player 2"

    def set_remember(self, remember):
        self.remember = remember

    def reset(self):
        self.points = 0
        self.sequential_counter = 0
        self.opponent_choices = []
        self.number_of_games = 0
        self.graph = []

    def plot_graph(self):
        plt.plot(self.graph)
        plt.suptitle("{} points per game".format(self.name))
        plt.xlabel("Number of games")
        plt.ylabel("Points")
        plt.show()


p1 = Player("historian")
p2 = Player("mostcommon")
p1.set_remember(2)

T = Tournament(player1=p1, player2=p2, number_of_games=100)
T.arrange_singlegame()
T.arrange_tournament()

results = Run(['rock_scissors_paper.py'], do_exit=False)
# `exit` is deprecated, use `do_exit` instead
print(results.linter.stats['global_note'])
