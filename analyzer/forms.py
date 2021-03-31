from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file', help_text='max. 42 megabytes')

    def clean_file(self):
        docfile = self.cleaned_data['docfile']
        ext = docfile.name.split('.')[-1].lower()
        if ext not in ["txt", "pdf"]:
            raise forms.ValidationError("Only txt and pdf files are allowed.")
        # return cleaned data is very important.
        return docfile
