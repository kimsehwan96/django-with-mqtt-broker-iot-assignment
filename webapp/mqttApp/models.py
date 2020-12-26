import datetime
from django.db import models
from django.utils import timezone
# Create your models here.


#for testing class

#IoT 데이터에를 객체화 하기 위하 클래스.
#시간 값을 센서에서 찍어서 올리는게 맞겠지?
class Data(models.Model):
    def __str__(self):
        return "time : {} temp {} : humid : {}".format(
            self.timestamp, self.temp, self.humid
        )
    timestamp = models.DateTimeField(auto_now=True)
    temp = models.FloatField(default=0)
    humid = models.FloatField(default=0)

class Device(models.Model):
    def __str__(self):
        return self.device_id
    
    device_id = models.CharField(max_length=100)
    #디바이스가 운영된 시간을 초단위 저장
    running_time = models.IntegerField(default=0)
    