import random
from django.db import models

# Create your models here.


class GameRoom(models.Model):
    player1 = models.SmallIntegerField(null=True, blank=True)
    player2 = models.SmallIntegerField(null=True, blank=True)
    currentTurn = models.SmallIntegerField(null=True, blank=True)
    currectEmoji = models.CharField(max_length=20, null=True, blank=True)
    guessedEmoji = models.CharField(max_length=20, null=True, blank=True)
    p1score = models.SmallIntegerField(default=0)
    p2score = models.SmallIntegerField(default=0)
    targetScore = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    gameClosed = models.BooleanField(default=False)

    op1 = models.CharField(max_length=20, null=True, blank=True)
    op2 = models.CharField(max_length=20, null=True, blank=True)
    op3 = models.CharField(max_length=20, null=True, blank=True)

class RoomMessage(models.Model):
    room = models.ForeignKey(GameRoom,on_delete = models.CASCADE)
    msg = models.CharField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    uid = models.PositiveSmallIntegerField()
    read = models.BooleanField(default=False)
    class Meta:
        ordering = ['-timestamp']