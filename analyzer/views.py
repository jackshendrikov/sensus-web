from django.shortcuts import render, redirect
from django.contrib import messages
from analyzer.models import Sentence
from analyzer.models import Document
from analyzer.forms import DocumentForm
from sensus.settings import MEDIA_ROOT

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def home(request):
    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents}
    return render(request, 'analyzer/home.html', context)


def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            messages.success(request, "Ваш документ було збережено!")

            # Redirect to the document list after POST
            return redirect('upload')
        else:
            messages.error(request, "Помилка! Спробуйте ще раз...")
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form}
    return render(request, 'analyzer/upload.html', context)


def convert_pdf_to_txt(path):
    rsrcmgr, retstr, laparams = PDFResourceManager(), StringIO(), LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password, maxpages, caching, pagenos = "", 0, True, set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


VALID = []


def prediction(request):
    link = request.POST.get('Link', False)

    if link != False:
        text = convert_pdf_to_txt(MEDIA_ROOT.replace('\\', '/') + '/' + link)
        sent = Sentence(str(text))
        predict = sent.prediction()
        VALID.append(predict)
    else:
        predict = VALID[-1]

    print("Prediction is :", float(predict))
    context = {'prediction':  round(float(predict), 2) * 100}

    return render(request, 'analyzer/predict.html', context)