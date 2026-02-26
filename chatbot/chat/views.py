import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .langchain_engine import build_retriever_from_url, answer_with_source

# cache simples em memória (ok pra trabalho/atividade local)
SESSION_STORE = {}  # session_key -> {"url": str, "retriever": obj}

def index(request):
    # garante session
    if not request.session.session_key:
        request.session.create()
    return render(request, "chat/index.html")

@csrf_exempt
def set_source(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    url = (data.get("url") or "").strip()

    if not url.startswith("http"):
        return JsonResponse({"error": "URL inválida (comece com http/https)."}, status=400)

    session_key = request.session.session_key or request.session.create()

    try:
        retriever = build_retriever_from_url(url)
        SESSION_STORE[session_key] = {"url": url, "retriever": retriever}
        request.session["history"] = []  # zera histórico ao trocar fonte
        return JsonResponse({"ok": True, "url": url})
    except Exception as e:
        return JsonResponse({"error": f"Falha ao carregar site: {e}"}, status=400)

@csrf_exempt
def api_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    message = (data.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "Mensagem vazia"}, status=400)

    session_key = request.session.session_key
    state = SESSION_STORE.get(session_key)

    if not state:
        return JsonResponse({"error": "Defina primeiro a URL do site (fonte)."}, status=400)

    try:
        reply = answer_with_source(state["retriever"], message)

        history = request.session.get("history", [])
        history.append({"role": "user", "text": message})
        history.append({"role": "bot", "text": reply})
        request.session["history"] = history

        return JsonResponse({"reply": reply, "history": history, "url": state["url"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def clear_history(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)
    request.session["history"] = []
    return JsonResponse({"ok": True})