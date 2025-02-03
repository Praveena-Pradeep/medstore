
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Medicine
from .forms import MedicineForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

def home(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and log them in
            user = form.save()
            login(request, user)  # Log the user in immediately after signup
            return redirect('login')  # Redirect to the add medicine page
        else:
            # If form is not valid, display error messages
            messages.error(request, "There was an error with your signup. Please try again.")
    else:
        form = UserCreationForm()  # Create an empty form instance
    
    return render(request, 'store/signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user if authentication is successful
            login(request, user)
            return redirect('add_medicine')  # Redirect to the medicine add page after login
        else:
            # Show an error message if the credentials are invalid
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'  







@login_required
def add_medicine(request):
    # Check if the user already has 5 medicines
    if Medicine.objects.filter(user=request.user).count() >= 5:
        # Show error message if they have 5 or more medicines
        if request.method == "POST":
            messages.error(request, "You can only add up to 5 medicines.")
            return render(request, 'store/add_medicine.html', {'form': MedicineForm()})

    # Handle POST request to add a medicine
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user  # Assign the current logged-in user
            medicine.save()  # Save the medicine instance
            return redirect('medicine_list')  # Redirect to the medicine list page after saving
    else:
        form = MedicineForm()

    return render(request, 'store/add_medicine.html', {'form': form})


@login_required
def medicine_list(request):
    # Fetch medicines for the logged-in user
    medicine_list = Medicine.objects.filter(user=request.user)
    
    # Create a paginator to paginate the medicines list (5 items per page)
    paginator = Paginator(medicine_list, 5)  # Show 5 medicines per page
    page_number = request.GET.get('page', 1)  # Default to page 1 if not specified
    page_obj = paginator.get_page(page_number)  # Get the page object

    # Debug: Log page_obj to console (for server-side check)
    print(f"Page Object: {page_obj}")  # Check if it's being created correctly

    return render(request, 'medicine_list.html', {'page_obj': page_obj})

@login_required

def search_medicine(request):
    query = request.GET.get('query', '')
    medicines = Medicine.objects.filter(user=request.user, name__icontains=query)
    return render(request, 'store/medicine_list.html', {'medicines': medicines})
@login_required

def edit_medicine(request, medicine_id):
    medicine = Medicine.objects.get(id=medicine_id, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'store/edit_medicine.html', {'form': form})

@login_required
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    # Ensure the logged-in user can only delete their own medicines
    if medicine.user != request.user:
        # Optionally, raise a 403 Forbidden error or just redirect
        return redirect('medicine_list')

    medicine.delete()
    return redirect('medicine_list')


@login_required
def user_logout(request):
    logout(request)
    return redirect('signup')

def home(request):
    return render(request, 'store/home.html')
# views.py

def medicine_list(request):
    medicines = Medicine.objects.all()  # Fetch all medicines from the database
    return render(request, 'medicine_list.html', {'medicines': medicines})
