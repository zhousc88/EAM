from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView,View,CreateView,DetailView,UpdateView,DeleteView
from django.views.generic.base import TemplateResponseMixin
from .models import UserPost,Department,Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ProfileEditForm
import re
# Create your views here.
@login_required
def dashboard(request):
    #AdminSite.index_template='account/dashboard.html'
    #return AdminSite().index(request)

    return render(request,'account/dashboard.html',{'section':'index'})

class UserPostMixin(LoginRequiredMixin):
    model = UserPost
    extra_context = {'section': 'post'}
    success_url = reverse_lazy("account:post_list")

class UserPostView(UserPostMixin,ListView):
    template_name = 'account/post_list.html'
    paginate_by = 10
    paginate_orphans = 0

class UserPostDeleteView(PermissionRequiredMixin,View):
    permission_required = 'UserPost.delete_userpost'
    def post(self,request):
        post_name = request.POST.getlist('postname[]')
        post_ids = request.POST.getlist('post_id[]')
        post_ids=','.join(post_ids)
        try:

            UserPost.objects.extra(where=['id IN ( '+post_ids+')']).delete()
            msg = "已成功删除岗位 {}".format(' '.join(post_name))
            messages.success(request, msg)
            return  JsonResponse({'status':'ok'})
        except UserPost.DoesNotExist:
            msg = "删除失败 {}".format(post_name)
            messages.warning(request, msg)
            return JsonResponse({'status':'ko'})

class UserPostEditView(PermissionRequiredMixin,UserPostMixin,UpdateView):
    fields = ['name','active','order']
    template_name = "account/post_form.html"
    permission_required = 'UserPost.change_userpost'

class PostCreateView(PermissionRequiredMixin,UserPostMixin,CreateView):
    permission_required = 'UserPost.add_userpost'
    fields = ['name','active','order']
    template_name = "account/post_form.html"
    def post(self, request, *args, **kwargs):
        post_name = request.POST.get('name')
        if UserPost.objects.filter(name=post_name):
            msg = "岗位{}已经存在 ".format(post_name)
            messages.info(request, msg)
            return redirect(reverse_lazy("account:post_create"))
        else:
            if "_save" not in request.POST:
                self.success_url = reverse_lazy("account:post_create")
            msg = "成功添加岗位 {}".format(post_name)
            messages.success(request,msg)
            return super(PostCreateView,self).post(request, *args, **kwargs)

class DepartmentMixin(LoginRequiredMixin):
    model = Department
    extra_context = {'section': 'department'}
    success_url = reverse_lazy("account:department_list")

class DepartmentListView(DepartmentMixin,ListView):
    template_name = "account/department_list.html"
    paginate_by = 10
    paginate_orphans = 0

class DepartmentCreateView(PermissionRequiredMixin,DepartmentMixin,CreateView):
    template_name = "account/department_form.html"
    fields = ['name','active','order']
    permission_required = 'Department.add_department'

    def post(self, request, *args, **kwargs):
        de_name = request.POST.get('name')
        if Department.objects.filter(name=de_name):
            msg = "部门 {} 已经存在 ".format(de_name)
            messages.info(request, msg)
            return redirect(reverse_lazy("account:department_create"))
        else:
            if "_save" not in request.POST:
                self.success_url = reverse_lazy("account:department_create")
            msg = "成功添加部门 {}".format(de_name)
            messages.success(request, msg)
            return super(DepartmentCreateView, self).post(request, *args, **kwargs)

class DepartmentDeleteView(PermissionRequiredMixin,DepartmentMixin,DeleteView):
    permission_required = 'Department.delete_department'
    def post(self, request, *args, **kwargs):
        name = request.POST.getlist('checkbox')
        del_name=','.join(name)
        try:
            Department.objects.extra(where=['id IN ('+ del_name +')']).delete()
            msg = "已成功删除岗位{}".format(del_name)
            messages.success(request, msg)
        except UserPost.DoesNotExist:
            msg = "删除失败 {}".format(del_name)
            messages.warning(request, msg)
        return redirect(self.success_url)

class DepartmentEditView(PermissionRequiredMixin,DepartmentMixin,UpdateView):
    template_name = "account/department_form.html"
    permission_required = 'Department.change_department'
    fields = ['name', 'active', 'order']

class Usermixin(LoginRequiredMixin):
    model = User
    extra_context = {'section': 'user'}
    success_url = reverse_lazy("account:user_list")
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.method == "POST":
            p_form = ProfileEditForm(self.request.Post)
        else:
            p_form = ProfileEditForm(instance=self.request.user.profile)
        context['p_form'] = p_form
        return context
    def 

class UserListView(Usermixin,ListView):
    template_name = "account/user_list.html"

class UserDetailView(Usermixin,DetailView):
    template_name = "account/user_detail.html"


class UserEditView(PermissionRequiredMixin,Usermixin,UpdateView):
    template_name = "account/user_form.html"
    permission_required = 'user.change_user'
    fields = ['username','last_name','first_name','email','is_active','is_staff']




