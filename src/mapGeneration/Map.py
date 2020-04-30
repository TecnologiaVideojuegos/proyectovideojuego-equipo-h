import arcade
from random import randrange


class Map:
    def __init__(self):
        """This is just a class to handle all 25 rooms at the same time"""
        self.main_path = []
        self.rooms = []
        for x in range(0, 5632, 1408):
            for y in range(0, 5632, 1408):
                self.rooms.append(Room(x, y))

    def __update_main_path(self):
        """Clears the main path and creates a new one"""
        # Clearing main path
        self.main_path.clear()

        # Adding first two rooms to the path
        self.main_path.append((randrange(5), 0))
        if self.main_path[0][0] == 0:
            if randrange(2):  # up
                self.main_path.append((0, 1))
            else:  # right
                self.main_path.append((1, 0))
        elif self.main_path[0][0] == 4:
            if randrange(2):  # up
                self.main_path.append((4, 1))
            else:  # left
                self.main_path.append((3, 0))
        else:
            r = randrange(3)
            if r == 0:  # up
                self.main_path.append((self.main_path[0][0], 1))
            elif r == 1:  # left
                self.main_path.append((self.main_path[0][0] - 1, 0))
            else:  # right
                self.main_path.append((self.main_path[0][0] + 1, 0))

        # Creating the rest of the main path
        while self.main_path[-1][1] != 5:
            # Check what happened with last two rooms in the main path
            a = self.main_path[-1]  # Room we're in
            b = self.main_path[-2]  # Room we were in
            c = (a[0] - b[0], a[1] - b[1])  # Last movement we did
            if c[1] == 1:  # We've just moved upwards
                if a[0] == 0:
                    if randrange(2):  # up
                        self.main_path.append((0, a[1] + 1))
                    else:  # right
                        self.main_path.append((1, a[1]))
                elif a[0] == 4:
                    if randrange(2):  # up
                        self.main_path.append((4, a[1] + 1))
                    else:  # left
                        self.main_path.append((3, a[1]))
                else:
                    r = randrange(3)
                    if r == 0:  # up
                        self.main_path.append((a[0], a[1] + 1))
                    elif r == 1:  # left
                        self.main_path.append((a[0] - 1, a[1]))
                    else:  # right
                        self.main_path.append((a[0] + 1, a[1]))
            elif c[0] == 1:  # We've just moved rightwards
                if a[0] == 4:
                    self.main_path.append((4, a[1] + 1))
                else:
                    if randrange(2):  # up
                        self.main_path.append((a[0], a[1] + 1))
                    else:  # right
                        self.main_path.append((a[0] + 1, a[1]))
            else:  # We've just moved leftwards
                if a[0] == 0:
                    self.main_path.append((4, a[1] + 1))
                else:
                    if randrange(2):  # up
                        self.main_path.append((a[0], a[1] + 1))
                    else:  # left
                        self.main_path.append((a[0] - 1, a[1]))
        self.main_path.pop()

    def new_map(self):
        """Creates a new set of rooms, following a new main path"""
        self.__update_main_path()
        # Setting up the rooms
        for x in range(5):
            for y in range(5):
                ri = x+5*y  # Room index
                if y == 0:
                    if x == 0:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), False, False)
                    if x == 4:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), False, randrange(2), False)
                    else:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), randrange(2), False)
                elif y < 4:
                    if x == 0:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), False, randrange(2))
                    if x == 4:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), False, randrange(2), randrange(2))
                    else:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(randrange(2), randrange(2), randrange(2), randrange(2))
                else:
                    if x == 0:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(False, randrange(2), False, randrange(2))
                    if x == 4:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(False, False, randrange(2), randrange(2))
                    else:
                        if (x, y) in self.main_path:
                            pass
                        else:
                            self.rooms[ri]. setup_room(False, randrange(2), randrange(2), randrange(2))
