from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class DaysOfWeek(models.TextChoices):
    MONDAY = 'Понедельник', 'Понедельник'
    TUESDAY = 'Вторник', 'Вторник'
    WEDNESDAY = 'Среда', 'Среда'
    THURSDAY = 'Четверг', 'Четверг'
    FRIDAY = 'Пятница', 'Пятница'
    SATURDAY = 'Суббота', 'Суббота'
    SUNDAY = 'Воскресенье', 'Воскресенье'


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='lessons/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"


class Subscription(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.IntegerField()
    duration = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.cost} ({self.duration})'

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"


class Coach(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    lesson = models.CharField(max_length=255)
    image = models.ImageField(upload_to='coaches/', null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.lesson}'

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренера"


class CoachFeedback(models.Model):
    client_name = models.CharField(max_length=255)
    body = models.TextField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='feedback/', null=True, blank=True)

    def __str__(self):
        return f'{self.client_name} - {self.coach.name} - {str(self.body[:50])}...'

    class Meta:
        verbose_name = "Отзыв на тренера"
        verbose_name_plural = "Отзывы на тренера"


class LessonCoach(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_slots = models.IntegerField()
    # selection day of week - Понедельник, Вторник, Среда
    day_of_week = models.CharField(max_length=20, choices=DaysOfWeek.choices)

    def __str__(self):
        return f'{self.day_of_week} {self.lesson.name} - {self.coach.name.split()[0]} - {self.start_time} - {self.end_time}'

    class Meta:
        verbose_name = "Расписание тренера"
        verbose_name_plural = "Расписание тренеров"


class TicketToLessonCoach(models.Model):
    lesson_coach = models.ForeignKey(LessonCoach, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.client_name} - {self.lesson_coach.lesson.name}'

    class Meta:
        verbose_name = "Запись на тренеровку к тренеру"
        verbose_name_plural = "Записи на тренировку к тренеру"


class SubscriptionClient(models.Model):
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client_name} - {self.subscription.name}'

    class Meta:
        verbose_name = "Приобретенный абонемент"
        verbose_name_plural = "Приобретенные абонементы"


class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.email} - {str(self.body)[:30]}...'

    class Meta:
        verbose_name = "Контактная форма"
        verbose_name_plural = "Контактные данные"


@receiver(post_save, sender=TicketToLessonCoach)
def update_available_slots(sender, instance, created, **kwargs):
    if created:
        # Получаем запись тренера, связанную с созданной записью на тренеровку
        lesson_coach = instance.lesson_coach
        # Уменьшаем количество свободных мест на 1
        lesson_coach.available_slots -= 1
        lesson_coach.save()
