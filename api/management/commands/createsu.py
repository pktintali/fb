from api.models import User
def handle(self, *args, **options):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@domain.com", "@@4444@@")
        self.stdout.write(self.style.SUCCESS('Successfully created new super user'))