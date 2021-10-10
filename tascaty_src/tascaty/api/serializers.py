from rest_framework.serializers import ModelSerializer
from tascaty.models import activity_tracker


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = activity_tracker
        fields = "__all__"
