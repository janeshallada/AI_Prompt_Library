import json
from django.http import JsonResponse
from .models import Prompt
from .redis_client import redis_client

def prompt_list(request):
    if request.method == "GET":
        prompts = list(Prompt.objects.all().values("id","title","complexity","created_at"))
        return JsonResponse(prompts, safe=False)

    elif request.method == "POST":
        body = json.loads(request.body)
        prompt = Prompt.objects.create(
            title=body["title"],
            content=body["content"],
            complexity=body["complexity"]
        )
        return JsonResponse({"id": str(prompt.id)}, status=201)

def prompt_detail(request, id):
    try:
        prompt = Prompt.objects.get(id=id)
        key = f"prompt:{id}:views"
        views = redis_client.incr(key)
        return JsonResponse({
            "id": str(prompt.id),
            "title": prompt.title,
            "content": prompt.content,
            "complexity": prompt.complexity,
            "created_at": prompt.created_at,
            "view_count": views
        })
    except Prompt.DoesNotExist:
        return JsonResponse({"error":"Not found"}, status=404)
