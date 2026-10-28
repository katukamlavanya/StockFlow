from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    return redirect("accounts:login")
