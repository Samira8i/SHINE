from django.contrib import admin

from api.models import *

admin.site.register(Lesson)
admin.site.register(Subscription)
admin.site.register(Coach)
admin.site.register(CoachFeedback)
admin.site.register(LessonCoach)
admin.site.register(TicketToLessonCoach)
admin.site.register(SubscriptionClient)
admin.site.register(ContactForm)