
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PredictionForm
from .models import Prediction
from .ml_model import predict_disease


def home(request):

    if request.method == "POST":
        form = PredictionForm(request.POST, request.FILES)

        if form.is_valid():

            obj = form.save(commit=False)

            obj.save()

            disease, confidence = predict_disease(obj.image.path)

            obj.predicted_disease = disease
            obj.confidence = confidence
            obj.save()

            return redirect("result", pk=obj.id)

    else:
        form = PredictionForm()

    return render(request, "prediction/home.html", {"form": form})


def result(request, pk):
    prediction = get_object_or_404(Prediction, id=pk)

    return render(
        request,
        "prediction/result.html",
        {"prediction": prediction}
    )