"""File serializers."""
from rest_framework import serializers

# List of valid actions.
ACTIONS = (
    ("new_folder", "new_folder"),
    ("rename", "rename"),
    ("copy", "copy"),
    ("move", "move"),
)


class FileActionSerializer(serializers.Serializer):
    """File action serializer."""

    action = serializers.ChoiceField(choices=ACTIONS)
    params = serializers.DictField(
        allow_empty=False,
        help_text=(
            "based on actions:"
            'new_folder: {"name": str},\n'
            'rename: {"old_name": str, "new_name": str},\n'
            'copy: {"source": str, "destination": str},\n'
            'move: {"source": str, "destination": str}'
        ),
    )


class NewFolderActionSerializer(serializers.Serializer):
    """New folder action serializer."""

    name = serializers.CharField(max_length=255)

    def validate_name(self, name):
        """Validate name."""
        if "/" in name or ".." in name:
            raise serializers.ValidationError("invalid name")
        return name


class RenameActionSerializer(serializers.Serializer):
    """Rename action serializer."""

    old_name = serializers.CharField(max_length=255)
    new_name = serializers.CharField(max_length=255)

    def validate_old_name(self, old_name):
        """Validate old name."""
        if "/" in old_name or ".." in old_name:
            raise serializers.ValidationError("invalid old name")
        return old_name

    def validate_new_name(self, new_name):
        """Validate new name."""
        if "/" in new_name or ".." in new_name:
            raise serializers.ValidationError("invalid new name")
        return new_name


class CopyActionSerializer(serializers.Serializer):
    """Copy action serializer."""

    source = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length=1024)


class MoveActionSerializer(serializers.Serializer):
    """Move action serializer."""

    source = serializers.CharField(max_length=255)
    destination = serializers.CharField(max_length=1024)
