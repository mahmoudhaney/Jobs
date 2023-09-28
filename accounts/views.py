from django.shortcuts import redirect, render
from .models import Profile
from accounts.forms import SignupForm, UserForm, ProfileForm

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.save()
            return redirect('/accounts/login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    print(profile, profile.image)
    old_image = profile.image

    if request.method=='POST':
        userform = UserForm(request.POST,instance=request.user)
        profileform = ProfileForm(request.POST,request.FILES,instance=profile )
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            myprofile = profileform.save(commit=False)
            myprofile.user = request.user
            myprofile.save()
            if old_image != request.FILES['image']:
                old_image.delete(save=False)
            return redirect('accounts:profile')
    else :
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request,'accounts/profile_edit.html',{'userform':userform , 'profileform':profileform})