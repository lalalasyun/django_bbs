from django import forms
from .models import UploadImage
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ["image","position_x","position_y","zoom"]
        widgets = {
            'position_x': forms.HiddenInput(),
            'position_y': forms.HiddenInput(),
            'zoom': forms.HiddenInput(),
        }
        labels = {
            'image':''
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['id'] = 'upload_image'

    def save(self, commit=True):
        table = super().save(commit=False)
        if self.upload_by:
            table.upload_by = self.upload_by
        if commit:
            table.save()
        return table
    
class TrimImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ["position_x","position_y","zoom"]
        widgets = {
            'position_x': forms.HiddenInput(),
            'position_y': forms.HiddenInput(),
            'zoom': forms.HiddenInput(),
        }
        # exclude = "__all__"
        # exclude = ["image","upload_by"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        table = super().save(commit=False)
        table.is_edited = True
        if commit:
            table.save()
        return table