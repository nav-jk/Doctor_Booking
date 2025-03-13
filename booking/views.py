from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import DoctorAvailability, Token
from .forms import DoctorAvailabilityForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Token, DoctorAvailability
from .utils import generate_pdf_token
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Token
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DoctorAvailability, Token
from django.http import HttpResponseRedirect



def home(request):
    return render(request, 'home.html')


@login_required
def doctor_dashboard(request):
    if request.method == "POST":
        date = request.POST.get("date")
        if date:
            DoctorAvailability.objects.get_or_create(date=date)  # Avoid duplicate dates

    available_dates = DoctorAvailability.objects.all()
    tokens = Token.objects.all().order_by("date", "token_number")

    return render(request, "doctor_dashboard.html", {
        "available_dates": available_dates,
        "tokens": tokens,
    })

@login_required
def delete_date(request, date_id):
    date = get_object_or_404(DoctorAvailability, id=date_id)
    date.delete()
    return redirect("doctor_dashboard")



from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Token, DoctorAvailability
from .utils import generate_pdf_token

def book_token(request):
    error_message = None  # Initialize error message

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date_str = request.POST.get("date")  # Get date as string

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert to date format
        except ValueError:
            error_message = " Invalid date format!"
        else:
            # ✅ Check if the phone number already booked for the selected date
            if Token.objects.filter(date=date, phone_number=phone).exists():
                error_message = "⚠️ You have already booked a token for this date!"
            else:
                tokens_today = Token.objects.filter(date=date)
                token_number = tokens_today.count() + 1

                new_token = Token.objects.create(
                    patient_name=name,
                    phone_number=phone,
                    date=date,  # Save as a proper DateField
                    token_number=token_number
                )

                return generate_pdf_token(new_token)  # Redirect to PDF generation

    available_dates = DoctorAvailability.objects.all()
    return render(request, "book_token.html", {
        "available_dates": available_dates,
        "error_message": error_message,  # Pass error message to template
    })


from django.shortcuts import render
from .models import Token, DoctorAvailability


def view_tokens(request):
    available_dates = DoctorAvailability.objects.all()
    tokens = []
    user_position = None
    phone_number = None
    selected_date = None

    if request.method == "POST":
        date_str = request.POST.get("date")
        phone_number = request.POST.get("phone")

        if date_str and phone_number:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Ensure correct format
            except ValueError:
                return HttpResponse("Invalid date format", status=400)

            # Filter tokens by selected date and entered phone number
            tokens = Token.objects.filter(date=selected_date, phone_number__iexact=phone_number).order_by("token_number")

            # Find user’s position in queue
            if tokens.exists():
                user_position = tokens.first().token_number
            else:
                user_position = "Not Found"

    return render(request, "view_tokens.html", {
        "available_dates": available_dates,
        "tokens": tokens,  # Now only contains the tokens of the entered phone number
        "user_position": user_position,
        "selected_date": selected_date,
        "phone_number": phone_number,
    })

from .models import Token  # Import your Token model

def delete_token(request, token_id):
    token = get_object_or_404(Token, id=token_id)
    token.delete()
    return redirect('doctor_dashboard')  # Redirect back to dashboard

from django.http import JsonResponse
from django.contrib.auth import get_user_model

def get_superuser_details(request):
    User = get_user_model()
    superusers = User.objects.filter(is_superuser=True).values("id", "username", "email", "date_joined", "last_login")
    
    return JsonResponse({"superusers": list(superusers)}, safe=False)


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')


def privacy(request):
    return render(request, 'privacy.html')

def news(request):
    return render(request, 'news.html')

def help(request):
    return render(request, 'helpcenter.html')

def contact(request):
    return render(request, 'contactsupport.html')

from .models import Token
def delete_appointment(request, token_id):
    appointment = get_object_or_404(Token, id=token_id)
    
    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Your appointment has been canceled successfully.")
    
    return redirect('view_tokens')  # Redirect to the main view where appointments are displayed




 