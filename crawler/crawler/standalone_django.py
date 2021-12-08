from django.conf import settings
settings.configure(
    DATABASES=settings.DATABASES,
    INSTALLED_APPS=settings.INSTALLED_APPS,
)
if __name__ == '__main__':
    import django
    django.setup()