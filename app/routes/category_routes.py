from flask import Blueprint, jsonify, request
from app.models.category import Category
from pydantic import ValidationError

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/category', methods=['POST'])
def category():
    try:
        dados = request.get_json()
        categoria = Category(**dados)
        return jsonify({"mensagem": f"{categoria}"})
    except ValidationError as e:
        return jsonify({"mensagem": f"{e}"})
    
    
