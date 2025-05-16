from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Page d'accueil
    path('formulaire/', views.formulaire, name='formulaire'),  # Page formulaire
    path('chatbot/', views.chatbot_view, name='chatbot'),  # Page chatbot
    path('about_us/', views.about_us, name='about_us'),  # Page "À propos"
    path('predict/', views.predict, name='predict'),  # Page de prédiction
    path('generate_sopk_graph/', views.generate_sopk_graph, name='generate_sopk_graph'),  # Graphique SOPK
]
