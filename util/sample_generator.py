# # Sample Python code that can be used to generate rooms in
# # a zig-zag pattern.
# #
# # You can modify generate_rooms() to create your own
# # procedural generation algorithm and use print_rooms()
# # to see the world.


# class Room:
#     def __init__(self, id, name, description, x, y):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.n_to = None
#         self.s_to = None
#         self.e_to = None
#         self.w_to = None
#         self.x = x
#         self.y = y
#     def __repr__(self):
#         if self.e_to is not None:
#             return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#         return f"({self.x}, {self.y})"
#     def connect_rooms(self, connecting_room, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#         reverse_dir = reverse_dirs[direction]
#         setattr(self, f"{direction}_to", connecting_room)
#         setattr(connecting_room, f"{reverse_dir}_to", self)
#     def get_room_in_direction(self, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         return getattr(self, f"{direction}_to")


# class World:
#     def __init__(self):
#         self.grid = None
#         self.width = 0
#         self.height = 0
#     def generate_rooms(self, size_x, size_y, num_rooms):
#         '''
#         Fill up the grid, bottom to top, in a zig-zag pattern
#         '''

#         # Initialize the grid
#         self.grid = [None] * size_y
#         self.width = size_x
#         self.height = size_y
#         for i in range( len(self.grid) ):
#             self.grid[i] = [None] * size_x

#         # Start from lower-left corner (0,0)
#         x = -1 # (this will become 0 on the first step)
#         y = 0
#         room_count = 0

#         # Start generating rooms to the east
#         direction = 1  # 1: east, -1: west


#         # While there are rooms to be created...
#         previous_room = None
#         while room_count < num_rooms:

#             # Calculate the direction of the room to be created
#             if direction > 0 and x < size_x - 1:
#                 room_direction = "e"
#                 x += 1
#             elif direction < 0 and x > 0:
#                 room_direction = "w"
#                 x -= 1
#             else:
#                 # If we hit a wall, turn north and reverse direction
#                 room_direction = "n"
#                 y += 1
#                 direction *= -1

#             # Create a room in the given direction
#             room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
#             # Note that in Django, you'll need to save the room after you create it

#             # Save the room in the World grid
#             self.grid[y][x] = room

#             # Connect the new room to the previous room
#             if previous_room is not None:
#                 previous_room.connect_rooms(room, room_direction)

#             # Update iteration variables
#             previous_room = room
#             room_count += 1



#     def print_rooms(self):
#         '''
#         Print the rooms in room_grid in ascii characters.
#         '''

#         # Add top border
#         str = "# " * ((3 + self.width * 5) // 2) + "\n"

#         # The console prints top to bottom but our array is arranged
#         # bottom to top.
#         #
#         # We reverse it so it draws in the right direction.
#         reverse_grid = list(self.grid) # make a copy of the list
#         reverse_grid.reverse()
#         for row in reverse_grid:
#             # PRINT NORTH CONNECTION ROW
#             str += "#"
#             for room in row:
#                 if room is not None and room.n_to is not None:
#                     str += "  |  "
#                 else:
#                     str += "     "
#             str += "#\n"
#             # PRINT ROOM ROW
#             str += "#"
#             for room in row:
#                 if room is not None and room.w_to is not None:
#                     str += "-"
#                 else:
#                     str += " "
#                 if room is not None:
#                     str += f"{room.id}".zfill(3)
#                 else:
#                     str += "   "
#                 if room is not None and room.e_to is not None:
#                     str += "-"
#                 else:
#                     str += " "
#             str += "#\n"
#             # PRINT SOUTH CONNECTION ROW
#             str += "#"
#             for room in row:
#                 if room is not None and room.s_to is not None:
#                     str += "  |  "
#                 else:
#                     str += "     "
#             str += "#\n"

#         # Add bottom border
#         str += "# " * ((3 + self.width * 5) // 2) + "\n"

#         # Print string
#         print(str)


# w = World()
# num_rooms = 44
# width = 8
# height = 7
# w.generate_rooms(width, height, num_rooms)
# w.print_rooms()


# print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")

# from django.contrib.auth.models import User
from adventure.models import Player, Room
from random import randint

# class Room:
#     def __init__(self, id, name, description, x, y):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.n_to = None
#         self.s_to = None
#         self.e_to = None
#         self.w_to = None
#         self.x = x
#         self.y = y
#         self.key = False
#     def __repr__(self):
#         if self.e_to is not None:
#             return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#         return f"({self.x}, {self.y})"
#     def connect_rooms(self, connecting_room, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#         reverse_dir = reverse_dirs[direction]
#         setattr(self, f"{direction}_to", connecting_room)
#         setattr(connecting_room, f"{reverse_dir}_to", self)
#     def get_room_in_direction(self, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         return getattr(self, f"{direction}_to")

class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
        self.room_count = 0
        self.rooms = []
        self.start = None
        self.exit = None
        self.key_room = None

    def generate_blank_matrix(self, size_x, size_y):
        
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

        self.start = start_room

        return start_room

    def exit_room(self, room):
        room.name = 'Exit'
        room.description = 'You have reached the Exit'
        self.exit = room

    def make_key_room(self, room):
        room.name = 'Key Room'
        room.description = 'A golden key sits in front of you'
        room.key = True
        self.key_room = room

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
        self.generate_blank_matrix(size_x=size_x, size_y=size_y)
        start_x = randint(0,size_x)
        start_y = randint(0,size_y)
        self.start = self.start_room(start_x, start_y)
        selected_room = self.start
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
        
        self.exit_room(self.rooms[-1])

        i = int(self.room_count * 0.66667)
        self.make_key_room(self.rooms[i])   

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        str = "# " * ((3 + self.width * 5) // 2) + "\n"

      
        reverse_grid = list(self.grid)
        reverse_grid.reverse()
        for row in reverse_grid:
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
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
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        print(str)


# Room.objects.all().delete()

w = World()
w.generate_world(10,10, 50)
w.print_rooms()

# rooms = Room.objects.all()
# for r in rooms:
#     r.save()

# players=Player.objects.all()
# for p in players:
#     p.currentRoom=w.start.id
#     p.save()