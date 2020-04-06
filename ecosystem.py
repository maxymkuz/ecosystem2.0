import random

from animals import Bear, Fish, Otter


class River:
    def __init__(self, size, bears_num, otter_num, fish_num):
        self._elements = self.generate(size, bears_num, otter_num, fish_num)
        self._powers = {'F': 0, 'O': 1, 'B': 2}
        self._children_num = {'F': 7, 'O': 3, 'B': 2}
        self._lifespan = {'F': 6, 'O': 13, 'B': 11}
        print('\nStage 0: ', end='')
        print(self)

    @staticmethod
    def generate(size, bears_num, otter_num, fish_num):
        """
        Generates an starting map
        """
        lst = [None] * size
        indexes = random.sample(range(size), bears_num + otter_num + fish_num)
        for i in indexes[:bears_num]:
            lst[i] = Bear()
        for i in indexes[bears_num: bears_num + otter_num]:
            lst[i] = Otter()
        for i in indexes[bears_num + otter_num:]:
            lst[i] = Fish()
        return lst

    @staticmethod
    def generate_moves(size):
        return [random.randint(-1, 1) for i in range(size)]

    @staticmethod
    def swap(arr, idx1, idx2):
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]

    @staticmethod
    def get_indexes(arr, name):
        """
        Returns a list of indexes, where an animal with a given name is
        :param arr: list
        :param name: str
        :return: list
        """
        indexes = []
        for i in range(len(arr)):
            if arr[i] is not None and arr[i].name == name:
                indexes.append(i)
        return indexes

    def collide(self, first, second, colliding_index):
        """
        Compares two instances of animal and returns appropriate animal for
        the colliding cell first, and then for second cell
        """
        # Two similar animal case
        if first.name == second.name:
            if first.male == second.male:
                if first.power > second.power:
                    return first, None
                elif first.power < second.power:
                    return second, None
                else:
                    return (first, None) if first.age < second.age \
                        else (second, None)

            # If they are of different sex, create a children:
            self.add_child(type(first), colliding_index)
            return second, first
        else:  # If there are different animals, the strongest type wins
            if self._powers[first.name] > self._powers[second.name]:
                return first, None
            elif self._powers[first.name] < self._powers[second.name]:
                return second, None

    def add_child(self, child_type, colliding_index):
        """
        Adds the children lefter than the colliding index if possible
        if not possible- add the child righter
        """
        child = child_type()
        # Adding needed amount of children
        for child_number in range(self._children_num[child.name]):
            child = child_type()
            found = False
            for j in range(colliding_index - 1, -1, -1):
                # If we find a place for a child:
                if self._elements[j] is None and not found:
                    self._elements[j] = child
                    found = True
            # If not possible, then placing it righter
            for j in range(colliding_index, len(self._elements)):
                # If we find a place for a child:
                if self._elements[j] is None and not found:
                    self._elements[j] = child
                    found = True

    def add_age_and_kill(self):
        # Kills old animals
        for i, animal in enumerate(self._elements):
            if animal is not None:
                animal.age += 1
                if animal.age >= self._lifespan[animal.name]:
                    self._elements[i] = None
        # If one species spreads on more than 60%:
        for name in self._lifespan:
            animal_indexes = self.get_indexes(self._elements, name)

            # If there is too much of some type of animals, randomly kill them
            while len(animal_indexes) > len(self._elements) * 0.6:
                animal_indexes = self.get_indexes(self._elements, name)
                idx = random.sample(animal_indexes, 1)[0]
                self._elements[idx] = None

    def move(self):
        """
        Main function that moves each animal exactly
        one postion in a random direction and handles collisions
        """
        # Generating random set of moves for a river:
        moves = self.generate_moves(len(self._elements))
        i = 0
        while i < len(self._elements):
            # In which direction does the current animal move
            current_move = moves[i]
            # Checking if in current cell there is an animal to move
            if self._elements[i] is None:
                i += 1
                continue

            # 1. If the animal moves forward:
            if current_move == 1:
                # Check if it is the last element:
                if i == len(self._elements) - 1:
                    i += 1
                    continue
                if self._elements[i + 1] is None:
                    self.swap(self._elements, i, i + 1)
                    i += 2
                # If current moves forward and the next animal backwards
                elif moves[i + 1] == -1:
                    self.swap(self._elements, i, i + 1)
                    i += 2
                # If the current animal collides with the next element:
                else:
                    try:
                        self._elements[i + 1], self._elements[i] = \
                            self.collide(self._elements[i],
                                         self._elements[i + 1], i)
                    except TypeError:  # This error is raised only in case
                        # if nothing is changed on the river, so do not pay
                        # attention on this
                        pass
                    finally:
                        i += 2

            # 2. If current animal moves backwards
            elif current_move == -1:
                # checking if it's the first element:
                if i == 0:
                    i += 1
                    continue
                if self._elements[i - 1] is None:
                    self.swap(self._elements, i - 1, i)
                    i += 2
                # If prev elem is also an animal, we collide them
                else:
                    try:
                        self._elements[i - 1], self._elements[i] = \
                            self.collide(self._elements[i - 1],
                                         self._elements[i], i - 1)
                    except TypeError:  # This error is raised only in case
                        # if nothing is changed on the river, so do not pay
                        # attention on this
                        pass
                    finally:
                        i += 2
            else:  # if current_move == 0, do nothing
                i += 1
        # Killing all the animals that are too old for this life
        self.add_age_and_kill()
        print(self)

    def get_animal_num(self, animal_type):
        """
        Just returns the amount of alive animals
        """
        return "".join([str(a) for a in self._elements if a is not
                        None]).count(animal_type().name)

    def __str__(self):
        return f"B:{self.get_animal_num(Bear)} O:" \
               f"{self.get_animal_num(Otter)} F:" \
               f"{self.get_animal_num(Fish)}  " + "".join(
            ['_' * 6 + ' ' if el is None else str(el) for el in
             self._elements])


if __name__ == '__main__':
    r = River(25, 5, 5, 5)
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
    r.move()
