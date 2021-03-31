from django.shortcuts import render, redirect
from analyzer.models import Sentence
from analyzer.models import Document
from analyzer.forms import DocumentForm


def home(request):
    return render(request, 'analyzer/home.html')


def my_view(request):
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'analyzer/list.html', context)


def prediction(request):
    text = request.POST.get('Text', False)
    sent = Sentence(str(text))
    predict = sent.prediction()

    print("Prediction is :", float(predict))

    return render(request, 'analyzer/home.html', {'prediction':  round(float(predict), 2) * 100})
