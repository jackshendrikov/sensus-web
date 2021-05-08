from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')

    def clean_file(self):
        docfile = self.cleaned_data['docfile']
        ext = docfile.name.split('.')[-1].lower()
        if ext not in ["pdf"]:
            raise forms.ValidationError("Only pdf and pdf files are allowed.")

        return docfile
