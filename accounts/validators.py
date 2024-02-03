from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone


def check_username_exists(request):
    """ This function validates if the typed username exists. """

    _username = request.POST.get('username')
    username_exists = get_user_model().objects.filter(username=_username).exists()

    if _username != '' and username_exists:
        return HttpResponse('<div class="error">Username exists!</div>')
    else:
        return HttpResponse('<div class="success">Username available.</div>')


def check_email_exists(request):
    """ This function validates if the typed email address exists. """

    _email = request.POST.get('email')

    email_exists = get_user_model().objects.filter(email=_email).exists()
    
    if email_exists:
        return HttpResponse('<div class="error">Email addres provided exists!</div>')

    return HttpResponse('')


def date_and_users_age_validation(request):
    """ This function validates if the user is an adult by calculating his/her age using the DoB provided by the user in the signup form. """

    _dob = request.POST.get('dob')  # date format YYYY-MM-DD
    current_date = timezone.now().date()

    # convert _dob to a datetime.date object
    new_dob = timezone.datetime.strptime(_dob, '%Y-%m-%d').date()

    # check if the date is valid. Date should not be greater than the current date
    if _dob != '':
        if new_dob > current_date:
            return HttpResponse('<div class="error">Invalid date provided!</div>')

        # calculate user's age
        age = int((current_date - new_dob).days / 365.25)

        if age < 18:
            return HttpResponse('<div class="error">You must be at least be 18 years to use the site.</div>')
    
    return HttpResponse('')


def password_match_and_length_validation(request):
    """ This function checks if the password is too short or the passwords provided don't match. """

    _password1 = request.POST.get('password1', False)
    _password2 = request.POST.get('password2', False)

    if _password1:
        if len(_password1) < 8:
            return HttpResponse('<div class="error">Password too short!')

    if _password1 and _password2:
        if _password1 != _password2:
            return HttpResponse('<div class="error">Passwords didn\'t match</div>')
    
    return HttpResponse('<div class="success">You\'re good to go!</div>')
