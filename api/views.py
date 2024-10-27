from lib2to3.fixes.fix_input import context
from random import sample

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import OrderedSet
from django.views.decorators.csrf import csrf_exempt

from api.models import (
    Lesson,
    CoachFeedback,
    Subscription,
    ContactForm,
    Coach,
    SubscriptionClient,
    LessonCoach, TicketToLessonCoach
)


# Create your views here.
def index(request):
    lessons = Lesson.objects.all()
    feedbacks = sample(list(CoachFeedback.objects.all()), 5)
    subscriptions = Subscription.objects.all()
    context = {
        'title': 'Главная',
        'lessons': lessons,
        'subscriptions': subscriptions,
        'feedbacks': feedbacks
    }
    return render(request, 'index.html', context=context)


from collections import OrderedDict


def schedule(request):
    lesson_coach_data = LessonCoach.objects.all().order_by('start_time', 'day_of_week')

    unique_days = list(OrderedSet([entry.day_of_week for entry in LessonCoach.objects.all()]))
    unique_timing = sorted(list(OrderedSet([entry.start_time for entry in lesson_coach_data])))

    schedule_data = OrderedDict()
    for time in unique_timing:
        schedule_data[time] = {}
        for day in unique_days:
            schedule_data[time][day] = list(lesson_coach_data.filter(start_time=time, day_of_week=day))

    context = {
        'title': 'Расписание',
        'unique_days': unique_days,
        'unique_timing': unique_timing,
        'schedule_data': schedule_data
    }

    return render(request, 'schedule.html', context=context)


def coaches(request):
    coaches = Coach.objects.all()
    context = {
        'title': 'Тренеры',
        'coaches': coaches
    }
    return render(request, 'about.html', context=context)


def contacts(request):
    context = {
        'title': "Контакты"
    }
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactForm.objects.create(name=name, email=email, body=message)
    return render(request, 'contact.html', context=context)


def ticket(request, lesson_coach_id):
    context = {
        'title': 'Запись на пробное занятие'
    }
    lesson_coach = LessonCoach.objects.get(pk=lesson_coach_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        TicketToLessonCoach.objects.create(client_name=name, lesson_coach=lesson_coach)
        return redirect('schedule')
    return render(request, 'for_zapic.html', context=context)


def subscription(request, subscription_id):
    subscriptions = Subscription.objects.all()
    context = {
        'subscriptions': subscriptions
    }
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subscription = Subscription.objects.filter(id=subscription_id).first()
        SubscriptionClient.objects.create(client_name=name, client_email=email, subscription=subscription)
    return render(request, 'for_abonement.html', context=context)


@csrf_exempt
def feedback(request, coach_id):
    coach_feedback = CoachFeedback.objects.filter(coach_id=coach_id)
    coach = coach_feedback.first().coach
    context = {
        'title': f'Отзыв на {coach.name}',
        'coach_feedback': coach_feedback,
        'coach': coach,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')

        # Сохраняем отзыв в базу данных
        coach_feedback = CoachFeedback.objects.create(coach_id=coach_id, client_name=name, body=text)

        # Возвращаем HTML-код отзыва для обновления страницы
        return JsonResponse({
            'client_name': coach_feedback.client_name,
            'body': coach_feedback.body,
        })
    return render(request, 'for_otz.html', context=context)
