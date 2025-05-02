from django import forms



class UploadCSVForm(forms.Form):
    archivo = forms.FileField(
        label='Seleccionar archivo CSV',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )