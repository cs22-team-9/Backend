from django.contrib.auth.models import User
from adventure.models import Player, Room

# Refresh the rooms
Room.objects.all().delete()

w = World()
w.generate_world(10,10, 50)

players=Player.objects.all()
for p in players:
  p.currentRoom=w.start.id
  p.save()
  

