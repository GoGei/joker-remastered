from django.contrib.auth.decorators import login_required


def public_login_required(*args, **kwargs):
    kwargs.setdefault('login_url', '/account/login/')
    return login_required(*args, **kwargs)
