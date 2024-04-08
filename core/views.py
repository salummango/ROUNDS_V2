from django.shortcuts import render
import nltk
from nltk.chat.util import Chat, reflections
from django.http import HttpResponse
# from food.models import FoodInfo
import random
import re

def home(request):
    return render(request=request,template_name="index.html")

def regist(request):
    return render(request=request,template_name="user/registration.html")


# def download_nltk_resources():
#     nltk.download('punkt')
#     nltk.download('wordnet')

# # Call the function to download the resources
# download_nltk_resources()


# # def get_chatbot_response(user_input):
# #     pairs = [
# #         [
# #             r"hi|hey|hello",
# #             ["Hello!", "Hey there!", "Hi! How can I assist you today?"]
# #         ],
# #         [
# #             r"bye|goodbye",
# #             ["Goodbye!", "Have a great day!", "See you later!"]
# #         ],
# #         [
# #             r"What types of pasta dishes do you serve?",
# #             get_pasta_types()
# #         ],
# #         [
# #             r"What types of pizza do you offer?",
# #             get_pizza_types()
# #         ],
# #         [
# #             r"Is there a vegan pasta option on the menu?",
# #             has_vegan_pasta()
# #         ],
# #         [
# #             r"Are there any seafood pasta options?",
# #             has_seafood_pasta()
# #         ],
# #         [
# #             r"Are there any pasta dishes with spicy flavors?",
# #             has_spicy_pasta()
# #         ],
# #         # Add more pattern-response pairs as needed
# #     ]

# #     chatbot = Chat(pairs, reflections)
# #     return chatbot.respond(user_input)

# # def get_pasta_types():
# #     pasta_types = FoodInfo.objects.filter(type='pasta')
# #     response = "We offer the following types of pasta dishes:\n"
# #     for pasta in pasta_types:
# #         response += f"- {pasta.name}\n"
# #     return response

# # def get_pizza_types():
# #     pizza_types = FoodInfo.objects.filter(type='pizza')
# #     response = "We offer the following types of pizza:\n"
# #     for pizza in pizza_types:
# #         response += f"- {pizza.name}\n"
# #     return response

# # def has_vegan_pasta():
# #     vegan_pasta = FoodInfo.objects.filter(type='pasta', description__icontains='vegan')
# #     if vegan_pasta:
# #         return "Yes, we have vegan pasta options available."
# #     else:
# #         return "Unfortunately, we do not have vegan pasta options on the menu."

# # def has_seafood_pasta():
# #     seafood_pasta = FoodInfo.objects.filter(type='pasta', description__icontains='seafood')
# #     if seafood_pasta:
# #         return "Yes, we have seafood pasta options available."
# #     else:
# #         return "Currently, we do not offer seafood pasta dishes."

# # def has_spicy_pasta():
# #     spicy_pasta = FoodInfo.objects.filter(type='pasta', description__icontains='spicy')
# #     if spicy_pasta:
# #         return "Yes, we have pasta dishes with spicy flavors."
# #     else:
# #         return "Our pasta dishes are not specifically spicy."




# def get_chatbot_response(user_input):
#     pairs = [
#         [
#             r"hi|hey|hello",
#             ["Hello!", "Hey there!", "Hi! How can I assist you today?"]
#         ],
#         [
#             r"bye|goodbye",
#             ["Goodbye!", "Have a great day!", "See you later!"]
#         ],
#         [
#             r"What types of pasta dishes do you serve?",
#             get_pasta_types
#         ],
#         [
#             r"What types of pizza do you offer?",
#             get_pizza_types
#         ],
#         [
#             r"Is there a vegan pasta option on the menu?",
#             has_vegan_pasta
#         ],
#         [
#             r"Are there any seafood pasta options?",
#             has_seafood_pasta
#         ],
#         [
#             r"Are there any pasta dishes with spicy flavors?",
#             has_spicy_pasta
#         ],
#         # Add more pattern-response pairs as needed
#     ]

#     chatbot = Chat(pairs, reflections)
#     for pattern, response in chatbot._pairs:
#         match = re.match(pattern, user_input)
#         if match:
#             if callable(response):
#                 # If the response is a function, execute it to get the actual response
#                 return response()
#             else:
#                 # If the response is a list of possible responses, pick a random one
#                 return random.choice(response)

#     # If no pattern matches the user input, return a default response
#     return "I'm sorry, I don't have the answer to that question."


# def get_pasta_types():
#     pasta_types = FoodInfo.objects.filter(type='pasta')
#     response = "We offer the following types of pasta dishes:\n"
#     for pasta in pasta_types:
#         response += f"- {pasta.name}\n"
#     return response

# def get_pizza_types():
#     pizza_types = FoodInfo.objects.filter(type='pizza')
#     response = "We offer the following types of pizza:\n"
#     for pizza in pizza_types:
#         response += f"- {pizza.name}\n"
#     return response

# def has_vegan_pasta():
#     vegan_pasta = FoodInfo.objects.filter(type='pasta', description__icontains='vegan').exists()
#     if vegan_pasta:
#         return "Yes, we have vegan pasta options available."
#     else:
#         return "Unfortunately, we do not have vegan pasta options on the menu."

# def has_seafood_pasta():
#     seafood_pasta = FoodInfo.objects.filter(type='pasta', description__icontains='seafood').exists()
#     if seafood_pasta:
#         return "Yes, we have seafood pasta options available."
#     else:
#         return "Currently, we do not offer seafood pasta dishes."

# def has_spicy_pasta():
#     spicy_pasta = FoodInfo.objects.filter(type='pasta', description__icontains='spicy').exists()
#     if spicy_pasta:
#         return "Yes, we have pasta dishes with spicy flavors."
#     else:
#         return "Our pasta dishes are not specifically spicy."










# # def chat_view(request):
# #     if request.method == 'POST':
# #         user_input = request.POST.get('user_input')
# #         chatbot_response = get_chatbot_response(user_input)
# #         return HttpResponse(chatbot_response)
# #     return render(request, 'chat.html')


# # chat_messages = []

# # def chat_view(request):
# #     if request.method == 'POST':
# #         user_input = request.POST.get('user_input')
# #         user_message = {
# #             'sender': 'user',
# #             'content': user_input
# #         }
# #         chat_messages.append(user_message)
# #         bot_response = get_chatbot_response(user_input)
# #         bot_message = {
# #             'sender': 'bot',
# #             'content': bot_response
# #         }
# #         chat_messages.append(bot_message)
# #         return render(request, 'chat.html', {'chat_messages': chat_messages})
# #     return render(request, 'chat.html', {'chat_messages': chat_messages})

# chat_messages = []

# def chat_view(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')
#         user_message = {
#             'sender': 'user',
#             'content': user_input
#         }
#         chat_messages.append(user_message)
        
#         # Check if the user is logged in and has an email
#         if request.user.is_authenticated and request.user.email:
#             # Get the user's email
#             user_email = request.user.email
#             # Display welcome message
#             welcome_message = f"Welcome {user_email}! were here to help you"
#             bot_message = {
#                 'sender': 'bot',
#                 'content': welcome_message
#             }
#             chat_messages.append(bot_message)
        
#         bot_response = get_chatbot_response(user_input)
#         bot_message = {
#             'sender': 'bot',
#             'content': bot_response
#         }
#         chat_messages.append(bot_message)
#         return render(request, 'chat.html', {'chat_messages': chat_messages})
    
#     return render(request, 'chat.html', {'chat_messages': chat_messages})

