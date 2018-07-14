from django.shortcuts import render,redirect
from axf.models import SlideShow, Cart,MainDescription, Product,CategorieGroup,ChildGroup,User,Address,Order
from django.contrib.auth import  logout
import random
from axf.sms import send_sms
from django.http import JsonResponse
import uuid

# Create your views here.
def home(request):
    #获取轮播图数据
    slideList = SlideShow.objects.all()
    #获取5大模块数据
    mainList = MainDescription.objects.all()
    for item in mainList:
        products = Product.objects.filter(categoryId=item.categoryId)
        item.product1 = products.get(productId=item.product1)
        item.product2 = products.get(productId=item.product2)
        item.product3 = products.get(productId=item.product3)
    return render(request, "home/home.html", {"slideList":slideList, "mainList":mainList})
def market(request, gid, cid, sid):
    #左侧分组数据
    leftCategorieList = CategorieGroup.objects.all()

    #获取分组商品的信息
    products = Product.objects.filter(categoryId=gid)
    #获取子类数据
    if cid != "0":
        products = products.filter(childId=cid)
    #排序
    if sid == "1":
        # products = products.order_by()
        pass
    elif sid == "2":
        products = products.order_by("price")
    elif sid == "3":
        products = products.order_by("-price")

    #获取子组信息
    childs = ChildGroup.objects.filter(categorie__categorieId=gid)

    return render(request, "market/market.html", {"leftCategorieList":leftCategorieList, "products":products, "childs":childs, "gid":gid, "cid":cid})
def cart(request):
    # 判断是否登录
    tokenValue = request.COOKIES.get("token")
    if not tokenValue:
        # 说明没登录
        return redirect("/login/")
    try:
        user = User.objects.get(tokenValue=tokenValue)
    except User.DoesNotExist as e:
        return redirect("/login/")
    carts = Cart.objects.filter(user__tokenValue=tokenValue)
    return render(request, "cart/cart.html", {"carts":carts})
def mine(request):
    phone = request.session.get('phoneNum',default='未登录')
    return render(request, "mine/mine.html",{'phone':phone})
# def login(request):
#     if request.method == 'GET':
#         if request.is_ajax():
#             strNum = '0123456789'
#             rand_str=''
#             for i in range(0,6):
#                 rand_str += strNum[random.randrange(0,len(strNum))]
#             msg ="您的验证码是：%s。请不要把验证码泄露给其他人。"%rand_str
#             phone = request.GET.get('phoneNum')
#             send_sms(msg,phone)
#             #存入session
#             request.session['code'] = rand_str
#             return JsonResponse({'data':'ok'})
#         else:
#             return render(request,'mine/login.html')
#     else:
#         phone = request.POST.get('username')
#         passwd = request.POST.get('passwd')
#         code = request.session.get('code')
#
#         if passwd == code:
#             uuidStr=str(uuid.uuid4())
#             try:
#                 user= User.objects.get(pk=phone)
#                 user.tokenValue = uuidStr
#                 user.save()
#             except User.DoesNotExist as e:
#                 user = User.create(phone,None,uuidStr,'000000')
#                 user.save()
#                 request.session['phoneNum'] = phone
#                 return redirect('/mine/')
#             else:
#                 return redirect('/login/')
def login(request):
    if request.method == "GET":
        if request.is_ajax():
            # 生产验证码
            strNum = '1234567890'
            # 随机选取4个值作为验证码
            rand_str = ''
            for i in range(0, 6):
                rand_str += strNum[random.randrange(0, len(strNum))]
            msg = "您的验证码是：%s。请不要把验证码泄露给其他人。"%rand_str
            phone = request.GET.get("phoneNum")
            send_sms(msg, phone)
            # print('*************',rand_str)
            #存入session
            request.session["code"] = rand_str
            return JsonResponse({"data":"ok"})
        else:
            return render(request, "mine/login.html")
    else:
        phone  = request.POST.get("username")
        passwd = request.POST.get("passwd")
        code   = request.session.get("code")

        if passwd == code:
            #验证码验证成功
            #判断用户是否存在
            uuidStr = str(uuid.uuid4())
            try:
                user = User.objects.get(pk=phone)
                user.tokenValue = uuidStr
                user.save()
            except User.DoesNotExist as e:
                #注册
                user = User.create(phone,None,uuidStr,"sunck good")
                user.save()
            request.session["phoneNum"] = phone
            #将tokenvalue写入cookie
            response = redirect("/mine/")
            response.set_cookie('token',uuidStr)
            return response
        else:
            # 验证码验证失败
            return redirect("/login/")
def quit(request):
    logout(request)
    return redirect('/mine/')
def showaddress(request):
    addrList= Address.objects.filter(user__phoneNum=request.session.get('phoneNum'))
    return render(request,'mine/showaddress.html',{'addrList':addrList})
def addaddr(request):
    if request.method == 'GET':
        return render(request, 'mine/addaddr.html')
    else:
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        if sex == '0':
            sex = False
        sex = True
        telephone = request.POST.get('phone')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        street = request.POST.get('street')
        postCode = request.POST.get('postCode')
        detailAddress=request.POST.get('detailAddress')

        phone = request.session.get('phoneNum')
        print(phone)
        user = User.objects.get(pk=phone)
        # name, sex, phoneNum, postCode, address, province, city, county, street, detailAddress, user
        alladdress = province+city+county+street+postCode+detailAddress
        address = Address.create(name,sex,telephone,postCode,alladdress,province,city,county,street,detailAddress,user)
        address.save()
        return redirect('/mine/')


def changecart(request,flag):
    num = 1
    if flag == '1':
        num = -1
    #判断是否登陆
    tokenValue=request.COOKIES.get('token')
    if not tokenValue:
        return JsonResponse({'error':1})
    try:
        user = User.objects.get(tokenValue=tokenValue)
    except User.DoesNotExist as e:
        return JsonResponse({'error':2})

    gid = request.POST.get('gid')
    cid = request.POST.get('cid')
    pid = request.POST.get('pid')
    product = Product.objects.filter(categoryId=gid,childId=cid).get(productId=pid)
    try:
        cart = Cart.objects.filter(user__tokenValue=tokenValue).filter(product__categoryId=gid).filter(product__childId=cid).get(product__productId=pid)
        if flag == '2':
            if product.storeNums == '0':
                return JsonResponse ({'error':0,'num':cart.num})
        cart.num = cart.num + num
        product.storeNums = str(int(product.storeNums) - num)
        product.save()
        if cart.num == 0:
            cart.delete()
        else:
            cart.save()

    except Cart.DoesNotExist as e:
        if flag == '1':
            return  JsonResponse({'error':0,'num':0})
        try:
            order = Order.orders2.filter(user__tokenValue=tokenValue).get(flag=0)
        except Order.DoesNotExist as e:
            orderId = str(uuid.uuid4())
            address = Address.objects.get(pk=3)
            order = Order.create(orderId,user,address,0)
            order.save()
        cart = Cart.create(user,product,order,1)
        cart.save()
        product.storeNums = str(int(product.storeNums) - num)
        product.save()

    return  JsonResponse({'error':0,'num':cart.num})
def changecart2(request):
    cartid = request.POST.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.isCheck = not cart.isCheck
    cart.save()
    return JsonResponse({'error':0,'flag':cart.isCheck})
def qOrder(request):
    tokenValue = request.COOKIES.get('token')
    order = Order.orders2.filter(user__tokenValue=tokenValue).get(flag=False)
    order.flag = 1
    order.save()

    carts = Cart.objects.filter(user__tokenValue=tokenValue).filter(order=order).filter(isCheck=True)
    for cart in carts:
        cart.isOrder = False
        cart.save()
    newOrder = Order.create(str(uuid.uuid4()),User.objects.get(tokenValue=tokenValue),Address.objects.get(pk=3),0)
    newOrder.save()
    oldCarts =  Cart.objects.filter(user__tokenValue=tokenValue)
    for cart in oldCarts:
        cart.order = newOrder
        cart.save()
    return JsonResponse({'error':0})

