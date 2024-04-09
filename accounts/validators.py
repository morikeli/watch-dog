from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator
from phonenumber_field.phonenumber import PhoneNumber
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone


def check_username_exists(request):
    """ This function validates if the typed username exists. """

    _username = request.POST.get('username')
    username_exists = get_user_model().objects.filter(username=_username).exists()

    if _username != '' and username_exists:
        return HttpResponse('<div class="error">This username exists!</div>')
    elif _username == '' or str(_username).isspace():
        return HttpResponse('<div class="error">Invalid username!</div>')
    else:
        return HttpResponse(f'<div class="success">"{_username}" is available.</div>')


def email_address_validation(request):
    """ This function validates if the typed email address exists or is valid. """

    _email = request.POST.get('email')

    email_exists = get_user_model().objects.filter(email=_email).exists()
    
    if email_exists:
        return HttpResponse('<div class="error">Email address provided exists!</div>')
    
    try:
        validate_email(_email)      # validate email address
    
    except ValidationError as error:
        return HttpResponse('<div class="error">Invalid email address!</div>')

    return HttpResponse('')


def validate_phone_number(phone_number):
    """ This is a function used to parse a mobile number and check if it is a valid. """
    try:
        # parse the number
        parsed_number = PhoneNumber.from_string(phone_number)
        
        # Check if the phone number is valid
        if not parsed_number.is_valid():
            raise ValidationError('Invalid phone number!')
    
    except Exception as e:
        # If parsing fails, raise a validation error
        raise ValidationError("Invalid mobile number!")

    return None     # if validation is successful, return None


def mobile_number_validation(request):
    """ Validate the mobile number provided by the user. """
    _mobile_no = request.POST.get('mobile_no', '')

    try:
        validate_phone_number(_mobile_no)   # validate the mobile number
    
    except ValidationError as error:
        return HttpResponse(f'<div class="error">{"".join(error)}</div>')

    return HttpResponse('<div class="success">Phone number is valid.</div>')


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


def validate_password_with_django_validators(password):
    """ This function validates passwords using in-built django password validators. """
    
    validators = [
        MinimumLengthValidator(),
        CommonPasswordValidator(),
        NumericPasswordValidator(),
        UserAttributeSimilarityValidator(),
    ]

    errors = []
    for validator in validators:
        try:
            # Validate the password using each validator
            validator.validate(password)
        except ValidationError as e:
            # If validation fails, collect the error message
            errors.extend(e.messages)

    return errors


def password_match_and_length_validation(request):
    """ This function checks performs password validation on the passwords input by the user. """

    _password1 = request.POST.get('password1')
    _password2 = request.POST.get('password2')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')

    errors = validate_password_with_django_validators(_password1 if not _password1 is None else new_password1)
    
    if errors:
        # Separate error messages with the <br> - HTML break tag
        error_message = "<br>".join(errors)
        return HttpResponse(f'<div class="error">{error_message}</div>')
    
    if (_password1 and _password2 and _password1 != _password2) or (new_password1 and new_password2 and new_password1 != new_password2):
        return HttpResponse('<div class="error">Passwords didn\'t match</div>')

    return HttpResponse('<div class="success">You\'re good to go!</div>')


def validate_old_password(request):
    """ This function checks if the old password entered in `PasswordChangeForm` matches the current user password. """

    _old_password = request.POST.get('old_password')
    user_password = get_user_model().objects.get(username=request.user)
    
    if _old_password and (user_password.password != _old_password):
        return HttpResponse('<div class="error">Your old password was entered incorrectly. Please enter it again.</div>')
    
    return HttpResponse('<div class="success">Good to go!</div>')