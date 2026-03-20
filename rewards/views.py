from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .gamification import get_leaderboard, get_or_create_profile


@login_required
def leaderboard_view(request):
    period = request.GET.get('period', None)  # daily, weekly, monthly veya None
    leaders = get_leaderboard(limit=20, period=period)
    my_profile = get_or_create_profile(request.user)
    return render(request, 'rewards/leaderboard.html', {
        'leaders': leaders,
        'period': period,
        'my_profile': my_profile,
    })
