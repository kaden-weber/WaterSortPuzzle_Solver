class Beaker:
    capacity = 4

    def __init__(self, contents):
        self.contents = contents

    def top_color(self):
        if len(self.contents) == 0:
            return None
        else:
            return self.contents[-1]

    def pour_in(self, color, count):
        for _ in range(count):
            self.contents.append(color)
        return

    def pour_out(self, count):
        starting_color = self.top_color()
        poured = 0
        for _ in range(count):
            self.contents.pop()
            poured += 1
            if self.top_color() != starting_color:
                break
        return poured

    def homogenous(self):
        color = self.contents[0]
        for c in self.contents:
            if color != c:
                return False
        return True

    def solved(self):
        if len(self.contents) == self.capacity:
            return self.homogenous()
        else:
            return False

    def empty(self):
        return len(self.contents) == 0

    def available(self):
        if len(self.contents) == self.capacity:
            return None, 0
        elif self.empty():
            return None, 4
        else:
            return self.top_color(), self.capacity - len(self.contents)

    def contents_at(self, index):
        if index < len(self.contents):
            return self.contents[index]
        else:
            return None


class Game:
    def __init__(self, input):
        self.beakers = input
        self.moves = []

    def pour(self, a, b):
        self.moves.append((a+1, b+1))  # offset for human readable indices
        a = self.beakers[a]
        b = self.beakers[b]
        color, availability = b.available()
        if availability == 0:
            return 1
        elif color is None or color == a.top_color():
            color_in = a.top_color()
            poured = a.pour_out(availability)
            b.pour_in(color_in, poured)

    def won(self):
        for b in self.beakers:
            if not (b.solved() or b.empty()):
                return False
        return True

    def display_cmdl(self):
        for col in range(self.beakers[0].capacity-1, -1, -1):
            line = ''
            for beaker in self.beakers:
                contents = beaker.contents_at(col)
                if contents is not None:
                    line += contents
                else:
                    line += '| |'
                line += '\t'
            print(line)
        print()

    def possible_next_moves(self):
        moves = []
        availabilities = [b.available() for b in self.beakers]
        for receiver, (color, count) in enumerate(availabilities):
            if count > 0:
                # the receiver has space
                for giver, b in enumerate(self.beakers):
                    if giver != receiver and not b.empty():
                        # don't pour into self, and don't pour empty vials
                        if color is None or b.top_color() == color:
                            # accept if empty or the same color
                            if not (color is None and b.homogenous()):
                                # don't pour into empty vial if giver is
                                # already homogenous
                                moves.append((giver, receiver))
        return moves

    def stuck(self):
        max_loop_size = 10
        if len(self.moves) > 2:
            loop_size = min(len(self.moves)-2, max_loop_size)
            prev = self.moves[-1]
            for i in range(loop_size):
                if prev == self.moves[-2 - i]:
                    return True
        return False
