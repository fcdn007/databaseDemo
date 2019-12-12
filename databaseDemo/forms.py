from django import forms

from .models import UploadFile


class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('uploadFile', 'uploadUrl', 'uploadOperator')
        widgets = {
            'uploadUrl': forms.TextInput(attrs={'class': 'form-control'}),
            'uploadOperator': forms.TextInput(attrs={'class': 'form-control'}),
            'uploadFile': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        file = super().clean().get('uploadFile')
        ext = file.name.split('.')[-1].lower()

        if ext not in ["txt", "csv", "xlsx"]:
            raise forms.ValidationError("只允许上传以下格式文件：txt, csv and xlsx。")
        # return cleaned data is very important.
        return super().clean()
