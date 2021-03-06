from django.db import models

# Create your models here.
class SlideShow(models.Model):
    trackid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    img = models.CharField(max_length=150)
    sort = models.CharField(max_length=20)
    class Meta:
        db_table= 'slideshows'
        ordering=['sort']

class Product(models.Model):
    name = models.CharField(max_length=100)
    longName = models.CharField(max_length=200)
    productId = models.CharField(max_length=20)
    storeNums = models.CharField(max_length=20)
    specifics = models.CharField(max_length=20)
    sort = models.CharField(max_length=20)
    marketPrice = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    categoryId = models.CharField(max_length=20)
    childId = models.CharField(max_length=20)
    img = models.CharField(max_length=200)
    keywords = models.CharField(max_length=100)
    brandId = models.CharField(max_length=20)
    brandName = models.CharField(max_length=100)
    safeDay = models.CharField(max_length=20)
    safeUnit = models.CharField(max_length=20)
    safeUnitDesc = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table='products'
        ordering=['sort']

class MainDescription(models.Model):
    categoryId= models.CharField(max_length=20)
    categoryName= models.CharField(max_length=40)
    img= models.CharField(max_length=200)
    sort= models.CharField(max_length=20)
    product1= models.CharField(max_length=20)
    product2= models.CharField(max_length=20)
    product3= models.CharField(max_length=20)
    class Meta():
        db_table='mainDecriptions'
        ordering=['sort']



class CategorieGroup(models.Model):
    name = models.CharField(max_length=20)
    categorieId = models.CharField(max_length=20)
    sort = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table='categroriegroups'
        ordering=['sort']
class ChildGroup(models.Model):
    cid = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    sort = models.CharField(max_length=20)
    categorie = models.ForeignKey("CategorieGroup")
    isDelete = models.BooleanField(default=False)

    class Meta():
        db_table='childgroup'
        ordering = ['sort']

'''
用户表      users
phoneNum     手机号(主键)
passwd      密码（允许为空）
tokenValue   token值
headImg      头像
integral     积分
vipLevel      会员等级
createTime       创建时间         
lastLoginTime     最后登陆时间
'''
class UserManager(models.Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(isDelete=False)
class User(models.Model):
    objects = UserManager()
    phoneNum = models.CharField(max_length=20, primary_key=True)
    passwd  = models.CharField(max_length=20, null=True, default=None)
    tokenValue = models.CharField(max_length=100)
    headImg = models.CharField(max_length=200)
    integral = models.CharField(max_length=20)
    vipLevel = models.CharField(max_length=20)
    createTime = models.DateTimeField(auto_now_add=True)
    lastLoginTime = models.DateTimeField(auto_now=True)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table = "users"
    def __str__(self):
        return self.phoneNum
    @classmethod
    def create(cls, phoneNum, passwd, tokenValue, headImg):
        return cls(phoneNum=phoneNum, passwd=passwd, tokenValue=tokenValue, headImg=headImg)



'''
地址表   addresses
name          姓名
sex           性别
phoneNum   手机号
postCode   邮编
address    收货地址
province   省份
city       城市
county     区县
street     街道
detailAddress 详细地址
user          所属用户(外键)
'''
class Address(models.Model):
    name = models.CharField(max_length=20)
    sex = models.BooleanField()
    phoneNum = models.CharField(max_length=20)
    postCode = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    province = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    county = models.CharField(max_length=40)
    street = models.CharField(max_length=40)
    detailAddress = models.CharField(max_length=200)
    user = models.ForeignKey("User")
    class Meta():
        db_table = "addresses"
    def __str__(self):
        return self.address
    @classmethod
    def create(cls, name, sex, phoneNum, postCode, address, province, city, county, street, detailAddress, user):
        return cls(name=name, sex=sex, phoneNum=phoneNum, postCode=postCode, address=address, province=province, city=city, county=county, street=street, detailAddress=detailAddress, user=user)



'''
购物车表  carts
user   用户
product  商品
num     数量
order  属于哪个订单
'''
class CartManager(models.Manager):
    def get_queryset(self):
        return super(CartManager, self).get_queryset().filter(isOrder=True)
class Cart(models.Model):
    objects = CartManager()
    user = models.ForeignKey("User")
    product = models.ForeignKey("Product")
    order = models.ForeignKey("Order")
    num = models.IntegerField()
    isOrder = models.BooleanField(default=True)
    isCheck = models.BooleanField(default=True)
    class Meta():
        db_table = "carts"
    @classmethod
    def create(cls, user, product, order, num):
        return cls(user=user, product=product, order=order, num=num)

'''
订单表       orders
orderId    订单号(主键)
user      用户
price      总价
address     地址
flag        状态
createTime   创建时间
lastTime    修改时间
isDelete   是否删除
'''
class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDelete=False)
class Order(models.Model):
    orders1 = models.Manager()
    orders2 = OrderManager()
    orderId = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey("User")
    address = models.ForeignKey("Address")
    price = models.FloatField()
    flag = models.IntegerField(default=0)
    createTime = models.DateTimeField(auto_now_add=True)
    lastTime = models.DateTimeField(auto_now=True)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table = "orders"
    @classmethod
    def create(cls, orderId, user, address, price):
        return cls(orderId=orderId, user=user, address=address, price=price)

