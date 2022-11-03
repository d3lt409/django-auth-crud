from django.urls import path
from .views import home, signup, tasks, signout, signin, \
        create_task,task_detail,task_complete,task_delete,complete_task

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('tasks/', tasks, name='tasks'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    path('tasks/create', create_task, name='create_task'),
    path('tasks/complete', complete_task, name='complete_tasks'),
    path('tasks/<int:id>', task_detail, name='task_detail'),
    path('tasks/<int:id>/complete', task_complete, name='task_complete'),
    path('tasks/<int:id>/delete', task_delete, name='task_delete')
]