from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'       # all the atributes/columns of the model Room
        exclude = ['host', 'participants']