from . import views
from django.urls import path,include
from django.conf.urls import url
from web3auth import views as vw


urlpatterns = [
    path('',views.voting,name='voting'),
    url(r'^', include('web3auth.urls')),
    url(r'^login_api/$', vw.login_api, name='web3auth_login_api'),
    url('verification',views.verification,name='verification'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]