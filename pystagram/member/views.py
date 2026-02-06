from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import SignupForm, LoginForm
from utils.email import send_email
from config import settings

User = get_user_model()

class SignupView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    # success_url = reverse_lazy('signup_done') 대신 form_valid에서 렌더링

    def form_valid(self, form):
        user = form.save()
        # 이메일 발송
        # 특정정보 암호화
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        # print(signer_dump)
        # decoded_user_email = signer.loads(signer_dump)
        # print(decoded_user_email)
        # email = signer.unsign(decoded_user_email, max_age=60 * 30)
        # print(email)

        # http://localhost:8000/verify/?code=asdasdas
        url = f'{self.request.schema}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}'
        if settings.DEBUG:
            print(url)
        else:
            subject = '[pystagram]이메일 인증을 완료해주세요.'
            message = f'다음 링크를 클릭해주세요. <br><a href="{url}">{url}</a>'

            send_email(subject, message, user.email)

        return render(
            self.request,
            template_name='auth/signup_done.html',
            context={'user': user}
        )

# 이메일에서 받은 코드를 확인하여 회원체크하기
def verify_email(request):
    code = request.GET.get('code', '')
    signer = TimestampSigner()

    try:
        decoded_user_email = signer.loads(code)
        email = signer.unsign(decoded_user_email, max_age=60 * 30)
    except (TypeError, SignatureExpired):
        return render(request, 'auth/not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False)
    user.is_active = True
    user.save()
    # TODO: 나중에 Redirect 시키기
    # return redirect(reverse('login'))
    return render(request, 'auth/email_verified_done.html', {'user': user})

class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    # TODO: 나중에 메인페이지로 리다이렉트
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # email = form.cleaned_data['email']
        # user = User.objects.get(email=email)
        user = form.user
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)

        return HttpResponseRedirect(self.get_success_url())
