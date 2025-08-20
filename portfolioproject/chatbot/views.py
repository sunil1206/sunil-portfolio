# # chatbot/views.py
#
# from textblob import TextBlob
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json
#
# from portfolio.models import (
#     AboutMe, Qualification, Experience, Skill, Tools,
#     Portfolio, Service
# )
# from .models import ChatbotIntentResponse
#
# # In-memory session
# session_state = {}
#
# def correct_grammar(user_input):
#     return str(TextBlob(user_input).correct()).lower()
#
# @csrf_exempt
# def chatbot_response(request):
#     if request.method != "POST":
#         return JsonResponse({"response": "Invalid request method"}, status=405)
#
#     data = json.loads(request.body)
#     user_input_raw = data.get("message", "")
#     user_input = correct_grammar(user_input_raw)
#     session_id = request.COOKIES.get("sessionid", "default")
#
#     state = session_state.get(session_id, {
#         "step": None,
#         "projects": [],
#         "selected_project": None
#     })
#
#     # === About Me ===
#     if any(k in user_input for k in ["yourself", "about", "name", "who are you"]):
#         about = AboutMe.objects.first()
#         response = f"I'm {about.name}, with {about.experience} years of experience. Contact: {about.email}, Phone: {about.phone}."
#
#     # === Education ===
#     elif any(k in user_input for k in ["education", "study", "degree", "qualification"]):
#         quals = Qualification.objects.all().order_by("order_number")
#         response = "Education:\n" + "\n".join([f"- {q.degree} at {q.institution} ({q.date_range})" for q in quals])
#
#     # === Experience ===
#     elif any(k in user_input for k in ["experience", "work", "job", "career"]):
#         exp = Experience.objects.all().order_by("order_number")
#         response = "Work Experience:\n" + "\n".join([f"- {e.position} at {e.company} ({e.date_range})" for e in exp])
#
#     # === Skills ===
#     elif "skill" in user_input:
#         skills = Skill.objects.all()
#         response = "My skills include: " + ", ".join([s.name for s in skills])
#
#     # === Tools ===
#     elif any(k in user_input for k in ["tool", "technology", "tech stack"]):
#         tools = Tools.objects.all()
#         response = "I use tools/technologies such as: " + ", ".join([t.name for t in tools])
#
#     # === Services ===
#     elif any(k in user_input for k in ["service", "offer", "provide"]):
#         services = Service.objects.all()
#         response = "Here are the services I offer:\n" + "\n".join([f"- {s.title}: {s.description}" for s in services])
#
#     # === Portfolio Start ===
#     elif "portfolio" in user_input or "project" in user_input:
#         projects = list(Portfolio.objects.all().order_by('-popularity')[:5])
#         state["projects"] = projects
#         state["step"] = "select_project"
#         session_state[session_id] = state
#         response = "Which project would you like to know about?\n" + "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(projects)])
#
#     # === Portfolio Selection ===
#     elif state["step"] == "select_project":
#         try:
#             index = int(user_input.strip()) - 1
#             project = state["projects"][index]
#             state["selected_project"] = project
#             state["step"] = "project_action"
#             session_state[session_id] = state
#             response = f"You selected: {project.name}\n1. Show project details\n2. Visit project link"
#         except:
#             response = "Please select a valid project number."
#
#     # === Portfolio Action ===
#     elif state["step"] == "project_action":
#         project = state["selected_project"]
#         if "1" in user_input:
#             response = f"\U0001F4CA Objective: {project.objective or 'N/A'}\n\U0001F9E0 Solution: {project.solution or 'N/A'}\n\U0001F527 Tools: {project.technologies_used or 'N/A'}"
#             state["step"] = None
#         elif "2" in user_input and project.url:
#             response = f"Visit project: {project.url}"
#             state["step"] = None
#         else:
#             response = "Please type 1 for details or 2 to visit link."
#         session_state[session_id] = state
#
#     # === Social Links ===
#     elif any(k in user_input for k in ["linkedin", "github", "instagram", "facebook"]):
#         about = AboutMe.objects.first()
#         links = {
#             "LinkedIn": about.linkedin,
#             "GitHub": about.github,
#             "Instagram": about.instagram,
#             "Facebook": about.facebook
#         }
#         response = "Social Profiles:\n" + "\n".join([f"{k}: {v}" for k, v in links.items() if v])
#
#     # === CV / Resume ===
#     elif "cv" in user_input or "resume" in user_input:
#         about = AboutMe.objects.first()
#         if about.cv:
#             response = f"Download my CV here: {about.cv.url}"
#         else:
#             response = "My CV is currently not uploaded."
#
#     # === Fallback ===
#     else:
#         fallback = ChatbotIntentResponse.objects.filter(question__icontains=user_input).first()
#         response = fallback.response if fallback else "I can help with skills, experience, tools, services, or portfolio. Try asking about any of these."
#
#     return JsonResponse({"response": response})


from textblob import TextBlob
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from openai import OpenAI

from analytics.models import DataScienceProject
from portfolio.models import (
    AboutMe, Qualification, Experience, Skill, Tools,
    Portfolio, Service
)
from .models import ChatbotIntentResponse

session_state = {}

def correct_grammar(user_input):
    return str(TextBlob(user_input).correct()).lower()

def normalize_input(text):
    substitutions = {
        "hru": "how are you",
        "hwr u": "how are you",
        "hw r u": "how are you",
        "gm": "good morning",
        "gn": "good night",
        "sup": "what's up"
    }
    for k, v in substitutions.items():
        text = text.replace(k, v)
    return text.strip().lower()

client = OpenAI(
    base_url="https://inference.baseten.co/v1",
    api_key="Ff2pDjis.SmcQFiifsbD6Cf4lmhTPa3wDXCElEVer"  # <-- IMPORTANT: Replace with your actual key
)
@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"response": "Invalid request method"}, status=405)

    data = json.loads(request.body)
    user_input_raw = data.get("message", "")
    user_input = normalize_input(correct_grammar(user_input_raw))
    session_id = request.COOKIES.get("sessionid", "default")

    state = session_state.get(session_id, {
        "step": None,
        "projects": [],
        "selected_project": None
    })

    # === 1. Intent-based DB match ===
    intent_match = ChatbotIntentResponse.objects.filter(question__iexact=user_input).first()
    if intent_match:
        state["step"] = None
        session_state[session_id] = state
        return JsonResponse({"response": intent_match.response})

    # === 2. Custom rule-based flows ===
    if any(k in user_input for k in ["yourself", "about", "name", "who are you"]):
        about = AboutMe.objects.first()
        response = f"I'm {about.name}, with {about.experience} years of experience. Contact: {about.email}, Phone: {about.phone}."

    elif any(k in user_input for k in ["education", "study", "degree", "qualification"]):
        quals = Qualification.objects.all().order_by("order_number")
        response = "Education:\n" + "\n".join([f"- {q.degree} at {q.institution} ({q.date_range})" for q in quals])

    elif any(k in user_input for k in ["experience", "work", "job", "career"]):
        exp = Experience.objects.all().order_by("order_number")
        response = "Work Experience:\n" + "\n".join([f"- {e.position} at {e.company} ({e.date_range})" for e in exp])

    elif "skill" in user_input:
        skills = Skill.objects.all()
        response = "My skills include: " + ", ".join([s.name for s in skills])

    elif any(k in user_input for k in ["tool", "technology", "tech stack"]):
        tools = Tools.objects.all()
        response = "I use tools/technologies such as: " + ", ".join([t.name for t in tools])

    elif any(k in user_input for k in ["service", "offer", "provide"]):
        services = Service.objects.all()
        response = "Here are the services I offer:\n" + "\n".join([f"- {s.title}: {s.description}" for s in services])

    # === Portfolio project flow ===
    elif "portfolio" in user_input or "project" in user_input:
        projects = list(Portfolio.objects.all().order_by('-popularity')[:10])
        state["projects"] = projects
        state["step"] = "select_project"
        session_state[session_id] = state
        response = "Which project would you like to know about?\n" + "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(projects)])

    elif state["step"] == "select_project":
        try:
            index = int(user_input.strip()) - 1
            project = state["projects"][index]
            state["selected_project"] = project
            state["step"] = "project_action"
            session_state[session_id] = state
            response = f"You selected: {project.name}\n1. Show project details\n2. Visit project link"
        except:
            response = "Please select a valid project number."

    elif state["step"] == "project_action":
        project = state["selected_project"]
        if "1" in user_input:
            response = f"\U0001F4CA Objective: {project.objective or 'N/A'}\n\U0001F9E0 Solution: {project.solution or 'N/A'}\n\U0001F527 Tools: {project.technologies_used or 'N/A'}"
            state["step"] = None
        elif "2" in user_input and project.url:
            response = f"Visit project: {project.url}"
            state["step"] = None
        else:
            response = "Please type 1 for details or 2 to visit link."
        session_state[session_id] = state

    # === Data Science Project flow ===
    elif "data science" in user_input or "ml project" in user_input or "ai project" in user_input:
        ds_projects = list(DataScienceProject.objects.all().order_by('-popularity')[:10])
        state["projects"] = ds_projects
        state["step"] = "select_ds_project"
        session_state[session_id] = state
        response = "Here are my top Data Science projects:\n" + "\n".join([f"{i+1}. {p.title}" for i, p in enumerate(ds_projects)])

    elif state["step"] == "select_ds_project":
        try:
            index = int(user_input.strip()) - 1
            project = state["projects"][index]
            state["selected_project"] = project
            state["step"] = "ds_project_action"
            session_state[session_id] = state
            response = f"You selected: {project.title}\n1. Show project details\n2. Visit project link"
        except:
            response = "Please select a valid Data Science project number."

    elif state["step"] == "ds_project_action":
        project = state["selected_project"]
        if "1" in user_input:
            response = (
                f"\U0001F4D8 Title: {project.title}\n"
                f"\U0001F4CA Problem: {project.problem or 'N/A'}\n"
                f"\U0001F52C Objective: {project.objective or 'N/A'}\n"
                f"\U0001F9E0 Solution: {project.solution or 'N/A'}\n"
                f"\U0001F527 Tools: {project.technologies_used or 'N/A'}\n"
                f"\U0001F6AB Challenges: {project.challenges_faced or 'N/A'}\n"
                f"\U0001F4C8 Methodology: {project.methodology or 'N/A'}\n"
                f"\U0001F3C6 Result: {project.result or 'N/A'}"
            )
            state["step"] = None
        elif "2" in user_input and project.url:
            response = f"Visit project: {project.url}"
            state["step"] = None
        else:
            response = "Please type 1 for details or 2 to visit link."
        session_state[session_id] = state

    # === Social / Contact Info ===
    elif any(k in user_input for k in ["linkedin", "github", "instagram", "facebook"]):
        about = AboutMe.objects.first()
        links = {
            "LinkedIn": about.linkedin,
            "GitHub": about.github,
            "Instagram": about.instagram,
            "Facebook": about.facebook
        }
        response = "Social Profiles:\n" + "\n".join([f"{k}: {v}" for k, v in links.items() if v])

    elif "cv" in user_input or "resume" in user_input:
        about = AboutMe.objects.first()
        if about.cv:
            response = f"Download my CV here: {about.cv.url}"
        else:
            response = "My CV is currently not uploaded."

    # === 3. Fallback ===
    else:
        partial_match = ChatbotIntentResponse.objects.filter(question__icontains=user_input).first()
        if partial_match:
            response = partial_match.response
        # else:
        #     response = "I can help with skills, experience, tools, services, data science or portfolio. Try asking about any of these."
        # state["step"] = None
        else:
            # NEW: If no partial match, call the external LLM API
            try:
                api_response = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3-0324",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. Keep your answers concise."},
                        {"role": "user", "content": user_input}
                    ]
                )
                response = api_response.choices[0].message.content
            except Exception as e:
                # Log the error for debugging, e.g., print(f"API Error: {e}")
                response = "I'm sorry, I'm having a bit of trouble thinking right now. Could you please ask something else?"

            # Reset the state in the fallback case
        state["step"] = None

    session_state[session_id] = state
    return JsonResponse({"response": response})

