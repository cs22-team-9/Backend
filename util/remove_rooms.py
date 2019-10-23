from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()
