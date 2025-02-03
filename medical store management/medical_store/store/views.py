from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Medicine, Stock
from .forms import MedicineForm, StockForm

# Check if the user is a manager (store manager)
def is_manager(user):
    return user.is_authenticated

# User Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

# Add a Medicine (limited to 5 medicines)
@login_required
def add_medicine(request):
    if Medicine.objects.filter(user=request.user).count() >= 5:
        return render(request, 'store/error.html', {'message': 'You can add only 5 medicines!'})

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user
            medicine.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'store/add_medicine.html', {'form': form})

# Add stock for a medicine
@login_required
def add_stock(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.medicine = medicine
            stock.save()
            return redirect('medicine_list')
    else:
        form = StockForm()
    return render(request, 'store/add_stock.html', {'form': form, 'medicine': medicine})

# Medicine list view with pagination
@login_required
def medicine_list(request):
    medicines = Medicine.objects.filter(user=request.user)
    paginator = Paginator(medicines, 5)  # 5 medicines per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'store/medicine_list.html', {'page_obj': page_obj})

# Search Medicines (AJAX)
def search_medicines(request):
    query = request.GET.get('query', '')
    medicines = Medicine.objects.filter(name__icontains=query)
    results = [{'name': medicine.name, 'id': medicine.id} for medicine in medicines]
    return JsonResponse({'results': results})

# Edit Medicine
@login_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'store/edit_medicine.html', {'form': form, 'medicine': medicine})

# Delete Medicine
@login_required
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    if request.method == 'POST':
        medicine.delete()
        return redirect('medicine_list')
    return render(request, 'store/delete_medicine.html', {'medicine': medicine})

# Logout
@login_required
def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')
