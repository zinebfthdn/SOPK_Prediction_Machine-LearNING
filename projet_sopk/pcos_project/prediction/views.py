import os
import logging
import joblib
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
import matplotlib.pyplot as plt
import io
import urllib, base64

# Configure logging
logger = logging.getLogger(__name__)

# Charger le modèle de prédiction
model_path = os.path.join(os.path.dirname(__file__), 'model_pcos.pkl')
model = joblib.load(model_path)

# Page d'accueil (Dashboard)
def index(request):
    return render(request, 'index.html')

# Page formulaire
def formulaire(request):
    return render(request, 'formulaire.html')

# Page chatbot
def chatbot_view(request):
    if request.method == "POST":
        message = request.POST.get("message")  # Message envoyé par l'utilisateur
        logger.info(f"Received message: {message}")  # Log incoming message

        # Créer un client Dialogflow
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path("your-project-id", "session-id")

        text_input = dialogflow.TextInput(text=message, language_code="fr")
        query_input = dialogflow.QueryInput(text=text_input)

        try:
            # Envoie la requête à Dialogflow
            response = session_client.detect_intent(request={"session": session, "query_input": query_input})

            # Log Dialogflow response
            logger.info(f"Dialogflow response: {response}")

            # Extraction de la réponse de Dialogflow
            fulfillment_text = response.query_result.fulfillment_text
            logger.info(f"Fulfillment text: {fulfillment_text}")

            return JsonResponse({"response": fulfillment_text})
        
        except InvalidArgument as e:
            logger.error(f"Dialogflow request failed: {str(e)}")
            return JsonResponse({"error": "Dialogflow request failed: " + str(e)})

    return render(request, "chatbot.html")

# Page à propos
def about_us(request):
    return render(request, 'about_us.html')

# Fonction de prédiction
def predict(request):
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            data = [
                float(request.POST['age']),
                float(request.POST['weight']),
                float(request.POST['height']),
                float(request.POST['period_gap']),
                float(request.POST['period_duration']),
                int(request.POST.get('weight_gain', 0)),
                int(request.POST.get('hair_growth', 0)),
                int(request.POST.get('skin_darkening', 0)),
                int(request.POST.get('hair_loss', 0)),
                int(request.POST.get('pimples', 0)),
                int(request.POST.get('fast_food', 0)),
                int(request.POST.get('exercise', 0)),
                int(request.POST.get('mood_swings', 0)),
                int(request.POST.get('regular_periods', 0))
            ]
            
            # Faire la prédiction
            prediction = model.predict([data])[0]
            result = "⚠️ Risque détecté de SOPK." if prediction == 1 else "✅ Aucun risque détecté."

            # Renvoyer à la page de résultat avec la prédiction
            return render(request, 'result.html', {'result': result})

        except Exception as e:
            # En cas d'erreur, afficher un message d'erreur
            return render(request, 'result.html', {'result': f"Erreur dans les données : {e}"})

# Exemple de génération d'un graphique pour SOPK
def generate_sopk_graph(request):
    labels = ['Diagnostiquées', 'Non diagnostiquées']
    sizes = [20, 80]
    colors = ['#ff66b2', '#ffe6f2']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.read(), content_type='image/png')
