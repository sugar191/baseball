from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # ユーザー作成後ログイン画面へ
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})