# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

from random import randint


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")
    def check_adjacent_rooms(self):
        """
        Checks each adjacent tile to see if there is a room there
        """
        pass

class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.room_count = 0
        self.rooms = []

    def generate_blank_matrix(self, size_x, size_y):
        # initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y 

        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x
        
    def start_room(self, start_x, start_y):
        start_room = Room(id=1, name='start_room', 
                          description='The starting room',
                          x=start_x, y=start_y)
        self.grid[start_room.x][start_room.y] = start_room
        self.room_count += 1

        return start_room

    def add_room(self,id, x, y):
        """
        Add a new room. Future version will specificy type of room
        """
        new_room = Room(id, name='new_room',
                        description='An additional room', 
                        x=x, y=y)
        self.grid[x][y] = new_room
        self.room_count += 1
        return new_room

    def generate_world(self, size_x, size_y, n_rooms):
        """
        Generates a map with n number rooms in x and y size
        """
        # Create Map
        self.generate_blank_matrix(size_x=size_x, size_y=size_y)
        # Generate Starting Location
        start_x = randint(0,size_x)
        start_y = randint(0,size_y)
        # Create Starting Room
        selected_room = self.start_room(start_x, start_y)

        while self.room_count < n_rooms:
            y_val = selected_room.y
            x_val = selected_room.x

            dir_roll = randint(0,3)

            if dir_roll == 0:
                x_val += 1
                direction = 's'
            elif dir_roll == 1:
                x_val -= 1
                direction = 'n'
            elif dir_roll == 2:
                y_val += 1
                direction = 'w'
            else:
                y_val -=1
                direction = 'e'

            if 0 <= x_val < size_x and 0 <= y_val < size_y:

                if self.grid[x_val][y_val] is None:    
                    new_room = self.add_room(self.room_count+1, x_val, y_val)

                    new_room.connect_rooms(selected_room, direction)
                    
                    self.rooms.append(new_room)

                    room_roll = randint(0,len(self.rooms)-1)
                    
                    selected_room = self.rooms[room_roll]
                    
                else:
                    room_roll = randint(0,len(self.rooms)-1)
                    selected_room = self.rooms[room_roll]
                    pass
            else:
                room_roll = randint(0,len(self.rooms)-1)
                selected_room = self.rooms[room_roll]
                pass

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)
