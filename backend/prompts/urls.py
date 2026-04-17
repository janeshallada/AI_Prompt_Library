from django.urls import path
from .views import prompt_list, prompt_detail

urlpatterns = [
    path('prompts/', prompt_list),
    path('prompts/<uuid:id>/', prompt_detail),
]
