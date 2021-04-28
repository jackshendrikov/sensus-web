from django.shortcuts import render, redirect
from django.contrib import messages
from analyzer.models import Sentence
from analyzer.models import Document
from analyzer.forms import DocumentForm


def home(request):
    # Load documents for the list page
    documents = Document.objects.all()

    lang = request.session['lang'] = 'ua'

    # someone clicks the link to change to English
    def switch_to_en(request):
        lang = request.session['lang'] = 'en'
        return lang

    # Render list page with the documents and the form
    context = {'documents': documents, 'lang': lang}
    return render(request, 'analyzer/home.html', context)


def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            messages.success(request, "Your data has been saved!")

            # Redirect to the document list after POST
            return redirect('upload')
        else:
            messages.error(request, "Error! Try one more time...")
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form}
    return render(request, 'analyzer/upload.html', context)


VALID = []


def prediction(request):
    text = request.POST.get('Text', False)

    if text != False:
        sent = Sentence(str(text))
        predict = sent.prediction()
        VALID.append(predict)
    else:
        predict = VALID[-1]

    print("Prediction is :", float(predict))
    context = {'prediction':  round(float(predict), 2) * 100, 'sent': str(text)}

    return render(request, 'analyzer/predict.html', context)