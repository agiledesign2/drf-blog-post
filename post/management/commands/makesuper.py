from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from post.models import Post


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@domain.com", "admin")
        if not User.objects.filter(username="editor").exists():
            editor = User.objects.create_user(
            	'editor', 'editor@domain.com', 'editor')
            #new_group, created = Group.objects.get_or_create(name='Editors')
            group = Group.objects.create(name='Editors')
            ct = ContentType.objects.get_for_model(Post)
            #Post._meta.app_label
            #Post._meta.model_name
            #permissions = Permission.objects.filter(content_type__app_label='app label', content_type__model='model name')
            permissions = Permission.objects.filter(content_type=ct)
            group.user_set.add(editor)
            group.permissions.set(permissions)
        if not User.objects.filter(username="normal").exists():
            User.objects.create_user(
            	'normal', 'normal@domain.com', 'normal')

		# g1.user_set.add(user1, user2, user5, user7)
		# g1.permissions.add(perm1, perm3, perm4)

		#proj_add_perm = Permission.objects.get(name='Can add project')
            self.stdout.write(self.style.SUCCESS('Group and Users has been created'))
        else:
            self.stdout.write(self.style.SUCCESS('Group and Users already exists'))
