from django import forms
from .models import BinaryDocument


class BinaryDocumentForm(forms.ModelForm):
    upload_file = forms.FileField(required=True)

    # list_display = ["name", "download_link", "expansion", "status_file"]
    class Meta:
        model = BinaryDocument
        fields = ['name', 'upload_file', "expansion", "status_file"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_file = self.cleaned_data['upload_file']
        instance.file_data = uploaded_file.read()
        if commit:
            instance.save()
        return instance


class TextActionForm(forms.Form):
    message = forms.CharField(label="Сообщение", widget=forms.Textarea(attrs={"rows": 4}), required=True)
