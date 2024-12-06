from flask import request, jsonify
from models import File, Chat_bot, Chat_details, db
from ai_processing.preprocessing_files import embedding_and_store, pdf_document_load
from ai_processing.generate_answer_ai import get_result, generate_answer
import os


def bot_create():
    user_id = request.headers.get('Userid')  # Get user ID from headers
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    # Extract data from the request
    data = request.json
    bot_name = data.get('bot_name')
    file_id = data.get('file_id')

    if not bot_name or not file_id:
        return jsonify({"error": "Bot name and file_id are required"}), 400

    # Retrieve the file by file_id
    file = File.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404

    # Process the PDF file and add embeddings with user-specific metadata
    chunked = pdf_document_load(file.index_file_path)  # Updated to handle PDFs
    embedding_path = embedding_and_store(chunked, file.filename, bot_name)

    # Save chatbot information
    new_chatbot = Chat_bot(
        bot_name=bot_name,
        user_id=user_id,
        file_id=file_id
    )

    try:
        db.session.add(new_chatbot)
        db.session.commit()
        return jsonify({"message": "Bot created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create bot", "message": str(e)}), 500


# Handle chat with bot
def chat():
    user_id = request.headers.get('Userid')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    data = request.json
    question = data.get("question")
    file_id = data.get("file_id")

    if not question or not file_id:
        return jsonify({"error": "Question and file_id are required"}), 400

    # Use the shared FAISS index for retrieval
    file = Chat_bot.query.filter_by(file_id=file_id).first()
    if not file:
        return jsonify({"error": "File not found"}), 406

    result_retrive = get_result(f"uploads/shared_index", question, user_id)
    response = generate_answer(result_retrive, question, file_id)

    # Save the AI interaction in the AI_info table
    new_chat_details = Chat_details(
        questions=question,
        answers=response,
        file_id=file_id,
        user_id=user_id
    )
    
    try:
        db.session.add(new_chat_details)
        db.session.commit()
        print(f"Chat details record added: {new_chat_details}")  # Debugging line
        return jsonify({'response': response}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to process chat", "message": str(e)}), 500


# Retrieve chat history
def get_chat_history():
    user_id = request.headers.get('userId')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    file_id = request.args.get('file_id')

    if file_id:
        # Retrieve history for a specific file_id and user_id
        history = Chat_details.query.filter_by(user_id=user_id, file_id=file_id).all()
    else:
        # Retrieve all history for a user
        history = Chat_details.query.filter_by(user_id=user_id).all()

    print(f"Retrieved history: {history}")  # Debugging line

    # Format the history response
    history_data = [{'question': h.questions, 'answer': h.answers} for h in history]
    return jsonify({'history': history_data})


# Get list of bots
def get_bot():
    # Retrieve user_id from the request headers (not session)
    user_id = request.headers.get('Userid')  # Get userId from request headers
    
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403  # If userId is missing, return 403 error

    # Get all bots for the logged-in user
    bots = Chat_bot.query.filter_by(user_id=user_id).all()

    # Format the bots response
    bots_report = [{'bot_name': b.bot_name, "file_id": b.file_id} for b in bots]
    return jsonify({'bots': bots_report})
