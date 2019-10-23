from django.contrib.auth.models import User
from adventure.models import Player, Room
from random import randint


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
        start_room = Room(id=1, title='start_room', 
                          description='The starting room',
                          x=start_x, y=start_y)
        self.grid[start_room.x][start_room.y] = start_room
        self.room_count += 1

        self.start = start_room

        return start_room

    def exit_room(self, room):
        room.title = 'Exit'
        room.description = 'You have reached the Exit'
        self.exit = room

    def make_key_room(self, room):
        room.title = 'Key Room'
        room.description = 'A golden key sits in front of you'
        room.key = True
        self.key_room = room

    def add_room(self,id, x, y):
        """
        Add a new room. Future version will specificy type of room
        """
        new_room = Room(id, title='new_room',
                        description='An additional room', 
                        x=x, y=y)
        new_room.save()
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
                    #changed new_room.connect_rooms to new_room.connectRooms
                    new_room.connectRooms(selected_room, direction)
                    self.rooms.append(new_room)
                    room_roll = randint(0,len(self.rooms)-1)
                    selected_room = self.rooms[room_roll]

                else:
                    room_roll = randint(0,len(self.rooms)-1)
                    selected_room = self.rooms[room_roll]
                    pass

            else:
                #! empty range for randrange() (0,0, 0)
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

w = World()
w.generate_world(10,10, 100)
w.print_rooms()

players=Player.objects.all()
for p in players:
  p.currentRoom=w.start_room
  p.save()
print(players, 'players')


