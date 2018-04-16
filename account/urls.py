from django.conf.urls import url
from django.contrib.auth.views import login,logout,logout_then_login
from django.contrib.auth.views import password_change,password_change_done
from .views import UserPostView,PostCreateView,UserPostEditView,UserPostDeleteView
from .views import DepartmentListView,DepartmentCreateView,DepartmentDeleteView,DepartmentEditView
from .views import UserListView,UserDetailView,UserEditView

from .views import dashboard
app_name='account'

urlpatterns = [
    url(r'^login/$',login,name='login'),
    url(r'^logout/$',logout,name='logout'),
    url(r'^logout-then-login/$',logout_then_login,name='logout-then-login'),
    url(r'^$',dashboard,name='dashboard'),
    url(r'^passwd-change/$',password_change,{'post_change_redirect':'account:passwd_done'},name='passwd_change'),
    url(r'passwd-change/done/$',password_change_done,name='passwd_done'),
    url(r'^post/$',UserPostView.as_view(),name='post_list'),
    url(r'^post/delete/$',UserPostDeleteView.as_view(),name='post_delete'),
    url(r'^post/create/$',PostCreateView.as_view(),name='post_create'),
    url(r'^post/(?P<pk>\d+)/edit/$',UserPostEditView.as_view(),name='post_edit'),
    url(r'^department/$',DepartmentListView.as_view(),name="department_list"),
    url(r'^department/create/$',DepartmentCreateView.as_view(),name='department_create'),
    url(r'^department/delete/$',DepartmentDeleteView.as_view(),name='department_delete'),
    url(r'department/(?P<pk>\d+)/edit/$',DepartmentEditView.as_view(),name='department_edit'),
    url(r'^user/$',UserListView.as_view(),name='user_list'),
    url(r'^user/(?P<pk>\d+)/$',UserDetailView.as_view(),name="user_detail"),
    url(r'^user/(?P<pk>\d+)/edit/$',UserEditView.as_view(),name="user_edit"),
    #url(r'^$',DashboardView().index,name='dashboard'),
]