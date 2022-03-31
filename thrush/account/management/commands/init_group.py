"""Initialize groups and their permissions."""
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Initialize default groups in the database."

    def _get_or_create_users_default_group(self):
        """Check and create users default group if not exists."""
        try:
            group = Group.objects.get(name=settings.DEFAULT_USER_GROUP)
            self.stdout.write(f"Group '{group.name}' already exists.")
        except Group.DoesNotExist:
            group = Group.objects.create(name=settings.DEFAULT_USER_GROUP)
            self.stdout.write(
                f"Creating group '{group.name}'... {self.style.SUCCESS('OK')}"
            )

        for defined_permission in settings.DEFAULT_USER_GROUP_PERMISSIONS:
            app_label, model, codename = defined_permission.split(".")
            if not group.permissions.filter(
                codename=f"{codename}_{model}",
                content_type__app_label=app_label,
                content_type__model__iexact=model,
            ).exists():
                permission = Permission.objects.get(
                    codename=f"{codename}_{model}",
                    content_type__app_label=app_label,
                    content_type__model__iexact=model,
                )
                group.permissions.add(permission)
                self.stdout.write(
                    f"Granting permission '{defined_permission}' to the group"
                    f" '{group.name}'... {self.style.SUCCESS('OK')}"
                )
            else:
                self.stdout.write(
                    f"The permission '{defined_permission}' was"
                    f" already granted to the group '{group.name}'."
                )
        group.save()

    def handle(self, *args, **kwargs):
        self._get_or_create_users_default_group()
        self.stdout.write("Finished")
