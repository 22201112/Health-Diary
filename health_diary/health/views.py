from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ProfileForm, HealthEntryForm
from .models import Profile, HealthEntry
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'health/home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # User is saved and profile is created automatically using signals
            login(request, user)
            print("User signed up and logged in, redirecting to profile")
            return redirect('profile')
        else:
            print("Form errors:", form.errors)
    else:
        form = SignUpForm()

    return render(request, 'health/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials, please try again.')
            return render(request, 'health/login.html')
    return render(request, 'health/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    # AI: BMI Calculation
    height_in_meters = profile.height / 100
    bmi = round(profile.weight / (height_in_meters ** 2), 2) if height_in_meters > 0 else None

    # BMI Category
    if bmi:
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi < 25:
            bmi_category = "Normal"
        elif 25 <= bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"
    else:
        bmi_category = "Unknown"

    # Eating Advice
    if bmi_category == "Underweight":
        eating_advice = "Increase calorie intake with healthy foods like nuts, dairy, and whole grains."
    elif bmi_category == "Normal":
        eating_advice = "Focus on balanced meals rich in fruits, vegetables, lean proteins, and whole grains."
    elif bmi_category == "Overweight":
        eating_advice = "Focus on portion control, eat more fiber, and stay active daily."
    else:
        eating_advice = "Consult a healthcare provider for personalized advice."

    return render(request, 'health/profile.html', {
        'profile': profile,
        'bmi': bmi,
        'bmi_category': bmi_category,
        'eating_advice': eating_advice
    })

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'health/edit_profile.html', {'form': form})

@login_required
def diary(request):
    entries = HealthEntry.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = HealthEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('diary')
    else:
        form = HealthEntryForm()
    return render(request, 'health/diary.html', {'form': form, 'entries': entries})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(HealthEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        form = HealthEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health entry updated successfully!')
            return redirect('diary')  # Redirect to the diary page or another page
        else:
            messages.error(request, 'There was an error updating the health entry.')
    else:
        form = HealthEntryForm(instance=entry)

    return render(request, 'health/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, entry_id):
    # Fetch the entry to be deleted for the current user
    entry = get_object_or_404(HealthEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the entry
        entry.delete()
        messages.success(request, 'Health entry deleted successfully!')
        return redirect('diary')  # Redirect to the diary page after deletion

    return render(request, 'health/delete_entry_confirm.html', {'entry': entry})