from rest_framework import serializers
from team.models import Team


class TeamCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description']
