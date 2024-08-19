from django.shortcuts import render
from league.models import Fixture
from django.core.paginator import Paginator


def home(request):
    error = request.GET.get('error')
    error_message = None

    if error == 'expired':
        error_message = 'Your session has expired. Please log in again.'
    elif error == 'invalid_signature':
        error_message = 'Invalid token signature. Please log in again.'
    elif error == 'decode_error':
        error_message = 'There was an error decoding your session. Please log in again.'
    elif error == 'user_not_found':
        error_message = 'User not found. Please log in again.'
    return render(request=request,template_name="index.html")

def regist(request):
    return render(request=request,template_name="user/register.html")




def FixtureList(request):
    fixtures = Fixture.objects.all().order_by('round_number')
    
    # Debug output
    print(f"Number of fixtures: {fixtures.count()}")
    
    fixtures_by_round = {}
    for fixture in fixtures:
        if fixture.round_number not in fixtures_by_round:
            fixtures_by_round[fixture.round_number] = []
        fixtures_by_round[fixture.round_number].append(fixture)
    
    rounds = sorted(fixtures_by_round.items())
    print(f"Number of rounds: {len(rounds)}")
    
    paginator = Paginator(rounds, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    print(f"Page number: {page_number}")
    print(f"Page object: {page_obj}")

    start_year = fixtures.first().match_date.year if fixtures.exists() else None
    end_year = fixtures.last().match_date.year if fixtures.exists() else None

    return render(request, 'league/League_Matches.html', {
        'page_obj': page_obj,
        'start_year': start_year,
        'end_year': end_year,
    })


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/admin/login/')


