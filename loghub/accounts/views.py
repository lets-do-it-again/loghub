from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import UpdateProfile
from accounts.models import User

class ProfileView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get('username'))
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.image_file.url if user.image_file else None,
            'professional': list(user.professional.values('specialty', 'level'))
        }

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get('username'))
        form = UpdateProfile(request.POST, request.FILES, instance= user)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Profile updated successfully'}, status=200)
        return JsonResponse({'errors': form.errors}, status=400)


      #
        # if 'old_password' in request.POST and 'new_password' in request.POST:
        #     change_password_form = ChangePasswordForm(request.POST)
        #     if change_password_form.is_valid():
        #         old_password = change_password_form.cleaned_data['old_password']
        #         new_password = change_password_form.cleaned_data['new_password']
        #         confirm_password = change_password_form.cleaned_data['confirm_password']
        #
        #         if not user.check_password(old_password):
        #             return JsonResponse({'error': 'Old password is incorrect'}, status=400)
        #
        #         if new_password != confirm_password:
        #             return JsonResponse({'error': 'New password and confirm password do not match'}, status=400)
        #
        #         user.set_password(new_password)
        #         user.save()
        #         return JsonResponse({'message': 'Password changed successfully'}, status=200)
        #     return JsonResponse({'errors': change_password_form.errors}, status=400)