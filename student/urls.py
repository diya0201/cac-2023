from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.student_dashboard, name='student_dashboard'),
    path('calendar/group/<int:group_id>', views.calendar_view, name='student_calendar'),
    path('day/<int:day>/<int:month>/<int:year>/group/<int:group_id>/', views.daydetail, name='daydetail'),
    path('day/<int:day>/<int:month>/<int:year>/group/<int:group_id>/time/', views.SavePracticeTimeView.as_view(), name='save_time'),
    path('analytics/group/<int:group_id>/month/<int:month>/year/<int:year>', views.analytics, name='analytics'),
    path('get_practice_time/group/<int:group_id>/<int:day>/<int:month>/<int:year>', views.get_practice_time, name='get_practice_time'),
    path('games/beat_the_met', views.beat_the_met, name='beat_the_met'),
    path('games/update_high_score_met', views.update_high_score_met, name='update_high_score_met'),
]
