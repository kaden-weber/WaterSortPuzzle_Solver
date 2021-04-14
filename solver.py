from copy import deepcopy

from game import Game, Beaker


class Solver():
    def __init__(self, game):
        self.game = game

    def solve(self):
        print("start:")
        self.game.display_cmdl()
        queue = [self.game]
        while len(queue) > 0:
            current_game = queue.pop()
            if current_game.won():
                print('end:')
                current_game.display_cmdl()
                print('Moves:')
                return current_game.moves
            elif not current_game.stuck():
                possible_moves = current_game.possible_next_moves()
                for move in possible_moves:
                    game_iteration = deepcopy(current_game)
                    game_iteration.pour(move[0], move[1])
                    # uncomment for help debugging
                    # game_iteration.display_cmdl()
                    queue.append(game_iteration)
        return None


def parse(filename):
    with open(filename) as input:
        beakers = []
        for line in input.readlines():
            colors = line.split(',')
            colors = [c.strip() for c in colors]
            if colors[0] == '':
                colors = []
            beakers.append(Beaker(colors))
    return Game(beakers)


def run(filename):
    parsed_game = parse(filename)
    for b in parsed_game.beakers:
        print(b.contents)
    print(Solver(parsed_game).solve())


# run('inputs/3.txt')
# run('inputs/105.txt')
run('inputs/115.txt')
