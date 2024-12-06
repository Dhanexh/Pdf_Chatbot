# routes.py
from flask import Blueprint
# from .auth import register_routes
from auth import register_routes
from bot import bot_create, chat, get_chat_history, get_bot
from file import upload_file 

# Blueprint Setup
auth_routes = Blueprint('auth_routes', __name__)
bot_routes = Blueprint('bot_routes', __name__)
file_routes = Blueprint('file_routes', __name__)

# Registering Routes for different functionalities
register_routes(auth_routes)
bot_routes.add_url_rule("/bot_create", "bot_create", bot_create, methods=["POST"])
bot_routes.add_url_rule("/chat", "chat", chat, methods=["POST"])
bot_routes.add_url_rule("/get_chat_history", "get_chat_history", get_chat_history, methods=["GET"])
bot_routes.add_url_rule("/get_bots", "get_bot", get_bot, methods=["GET"])
file_routes.add_url_rule("/upload_file", "upload_file", upload_file, methods=["POST"])

