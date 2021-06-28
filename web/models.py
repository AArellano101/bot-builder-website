from django.db import models

# Create your models here.
class bot(models.Model):
    title = models.CharField(max_length=1000)
    image = models.CharField(max_length=100000)
    description = models.CharField(max_length=1000000, default="")
    valid_image = models.BooleanField(default=False)
    failsafe = models.CharField(max_length=100000, default="")
    saved = models.BooleanField(default=False)
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "description": self.description,
            "valid_image": self.valid_image,
            "failsafe": self.failsafe,
            "saved": self.saved
        }
        

class click(models.Model):
    bot_id = models.IntegerField(default=-1)
    order = models.IntegerField(default=0)
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)
    def serialize(self):
        return {
            "bot_id": self.bot_id,
            "order": self.order,
            "x_position": self.x_position,
            "y_position": self.y_position
        }

class scroll(models.Model):
    bot_id = models.IntegerField(default=-1)
    order = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    def serialize(self):
        return {
            "bot_id": self.bot_id,
            "order": self.order,
            "amount": self.amount
        }

class write(models.Model):
    bot_id = models.IntegerField(default=-1)
    order = models.IntegerField(default=0)
    string = models.CharField(max_length=1000)
    def serialize(self):
        return {
            "bot_id": self.bot_id,
            "order": self.order,
            "string": self.string
        }

class press(models.Model):
    bot_id = models.IntegerField(default=-1)
    order = models.IntegerField(default=0)
    button = models.CharField(max_length=10)
    def serialize(self):
        return {
            "bot_id": self.bot_id,
            "order": self.order,
            "button": self.button
        }

class loop(models.Model):
    bot_id = models.IntegerField(default=-1)
    order_start = models.IntegerField(default=0)
    order_end = models.IntegerField(default=0)
    iterations = models.IntegerField(default=0)
    def serialize(self):
        return {
            "bot_id": self.bot_id,
            "order_start": self.order_start,
            "order_end": self.order_end,
            "iterations": self.iterations
        }

class wait(models.Model):
    bot_id = models.IntegerField(default=-1)
    order = models.IntegerField(default=0)
    milliseconds = models.IntegerField(default=0)
    def serialize(self):
        return {
            "bot_id": self.bot_id,
            "milliseconds":self.milliseconds
        } 

class drag(models.Model):
   bot_id = models.IntegerField(default=-1)
   order = models.IntegerField(default=0)
   startx = models.IntegerField(default=0)
   starty = models.IntegerField(default=0)
   endx = models.IntegerField(default=0)
   endy = models.IntegerField(default=0)
   time = models.IntegerField(default=-1)
   hold = models.BooleanField(default=False)

   def serialize(self):
       return {
           "bot_id": self.bot_id,
           "order": self.order,
           "startx": self.startx,
           "starty": self.starty,
           "endx": self.endx,
           "endy": self.endy,
           "time": self.time,
           "hold": self.hold,
       } 

class control(models.Model):
   bot_id = models.IntegerField(default=-1)
   order = models.IntegerField(default=0)
   button = models.CharField(max_length=30, default="none")
   key = models.CharField(max_length=2, default="none")
   def serialize(self):
       return {
           "bot_id": self.bot_id,
           "order": self.order,
           "button": self.button,
           "key": self.key
       } 



#class new_action(models.Model):
#   bot_id = models.IntegerField(default=-1)
#   order = models.IntegerField(default=0)
#   info = info
#   def serialize(self):
#       return {
#           "bot_id": self.bot_id,
#           "order": self.order,
#           info: info
#       } 


class status(models.Model):
    status = models.BooleanField(default=False)
    def serialize(self):
        return {
            "status": self.status
        }