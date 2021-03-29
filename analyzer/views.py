from django.shortcuts import render
from analyzer.models import Sentence


def home(request):
    return render(request, 'analyzer/home.html')


def prediction(request):
    text = request.POST.get('Text', False)
    sent = Sentence(str(text))
    predict = sent.prediction()

    print("Prediction is :", float(predict))

    return render(request, 'analyzer/home.html', {'prediction':  round(float(predict), 2) * 100})
