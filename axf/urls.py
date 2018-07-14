from django.conf.urls import url
from axf import views

urlpatterns = [
    url(r'', views.home),
    url(r'market/(\w+)/(\w+)/(\w+)/$', views.market),

    url(r'^cart/$', views.cart),
    url(r'^changecart2/$', views.changecart2),
    url(r'^qOrder/$', views.qOrder),


    url(r'^mine/$', views.mine),
    url(r'^login/$', views.login),
    url(r'^quit/$', views.quit),

    url(r'^showaddress/$', views.showaddress),
    url(r'^addaddr/$', views.addaddr),

    url(r'^changecart/(\d+)/$',views.changecart)

    # url(r'products/(\w+)')

]