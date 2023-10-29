from django.urls import path
from . import views


urlpatterns = [
    path('classes/', views.group_list, name='educator_classes'),
    path('group_detail/<int:group_id>/', views.group_detail, name='group_detail'),
    path('view_student/<int:group_id>/<int:student_id>/', views.view_student_calendar, name='view_student_calendar'),
    path('get_student_practice_time/<int:student_id>/group/<int:group_id>/<int:day>/<int:month>/<int:year>', views.get_student_practice_time, name='get_student_practice_time'),
    path('student_daydetail/<int:student_id>/group/<int:group_id>/<int:day>/<int:month>/<int:year>', views.student_daydetail, name='student_daydetail'),
]
