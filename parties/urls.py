from django.urls import path
from . import views


app_name = 'parties'




urlpatterns =[
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('DS/',views.dataSubject, name='DsDashboard'),
    path('Rqp/',views.requestingParty, name='RqpDashboard'),
    path('Rqp/sendrequest/',views.SendRequest, name= 'RequestSend'),
    path('DS/approverequest/', views.ApproveRequest, name= 'RequestApprove'),
    
]

#RqP = requestingparty
#DS = Data Subject