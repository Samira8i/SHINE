from django.urls import path
from api.views import (
    index,
    schedule,
    coaches,
    contacts,
    ticket,
    subscription,
    feedback
)

urlpatterns = [
    path('', index, name='index'),
    path('schedule/', schedule, name='schedule'),
    path('coaches/', coaches, name='coaches'),
    path('contacts/', contacts, name='contacts'),
    path('ticket/<int:lesson_coach_id>', ticket, name='ticket'),
    path('subscription/<int:subscription_id>', subscription, name='subscription'),
    path('feedback/<int:coach_id>', feedback, name='feedback')
]
