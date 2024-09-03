from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from users.models import Subscription
from courses.models import Course


def make_payment(request, pk: int) -> Subscription:
    """Совершение оплаты"""

    course = get_object_or_404(Course, pk=pk)
    user = request.user
    
    if user.balance.value < course.price:
        raise HttpResponseBadRequest('Баланс из овер (((')
    
    user.balance.value = user.balance.value - course.price
    user.balance.save()
    
    sub = Subscription(user=user, course=course)
    sub.save()

    return sub
