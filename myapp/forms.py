from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Choose a PDF file')
    split_size = forms.IntegerField(label='Max Page', required=False, initial=20)
    dpi = forms.IntegerField(label='dpi', required=False, initial=300)
