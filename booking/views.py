from django.shortcuts import render


from django.shortcuts import render, redirect
from .models import DoctorAvailability, Token
from .forms import DoctorAvailabilityForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Token, DoctorAvailability
from .utils import generate_pdf_token

def home(request):
    return render(request, 'home.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DoctorAvailability, Token
from django.http import HttpResponseRedirect

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
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date_str = request.POST.get("date")  # Get date as string

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert to date format
        except ValueError:
            return HttpResponse("Invalid date format", status=400)

        tokens_today = Token.objects.filter(date=date)
        token_number = tokens_today.count() + 1

        new_token = Token.objects.create(
            patient_name=name,
            phone_number=phone,
            date=date,  # Save as a proper DateField
            token_number=token_number
        )

        return generate_pdf_token(new_token)

    available_dates = DoctorAvailability.objects.all()
    return render(request, "book_token.html", {"available_dates": available_dates})


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

        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Ensure correct format
            except ValueError:
                return HttpResponse("Invalid date format", status=400)

            tokens = Token.objects.filter(date=selected_date).order_by("token_number")

            # Find user’s position in queue if they entered their phone number
            if phone_number:
                try:
                    user_token = tokens.get(phone_number__iexact=phone_number)  # Case-insensitive matching
                    user_position = user_token.token_number
                except Token.DoesNotExist:
                    user_position = "Not Found"

    return render(request, "view_tokens.html", {
        "available_dates": available_dates,
        "tokens": tokens,
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

def check_superuser(request):
    User = get_user_model()
    superuser_exists = User.objects.filter(is_superuser=True).exists()
    
    return JsonResponse({"superuser_exists": superuser_exists})


