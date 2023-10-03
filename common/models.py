from django.db import models

# Create your models here.
class Customer(models.Model):
  name = models.CharField(max_length=200)
  phone = models.CharField(max_length=200)
  address = models.CharField(max_length=200)

class Medicine(models.Model):
  name = models.CharField(max_length=200)
  sn = models.CharField(max_length=200)
  dec = models.CharField(max_length=200)

import datetime

class Order(models.Model):
  name = models.CharField(max_length=200)
  createdate = models.DateTimeField(default=datetime.datetime.now)
  customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
  medicine = models.ManyToManyField(Medicine,through='OrderMedicine')

class OrderMedicine(models.Model):
  order = models.ForeignKey(Order,on_delete=models.PROTECT)
  medicine = models.ForeignKey(Medicine,on_delete=models.PROTECT)
  amount = models.PositiveIntegerField()


# 以下是have a nice day后端建表的代码 
class Illustration(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=30,blank=False)
  author = models.CharField(max_length=30)
  illu = models.ImageField(upload_to='illustration')
  desc = models.CharField(max_length=200)
  updatetime = models.DateTimeField()
  tag = models.CharField(max_length=200)
  del_flag = models.SmallIntegerField(default=0)
  del_time = models.DateTimeField(blank=True,null=True)

class IlluPic(models.Model):
  picid = models.AutoField(primary_key=True)
  picname = models.CharField(max_length=200)
  illu = models.ImageField(upload_to='illustration')
