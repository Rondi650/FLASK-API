from functools import wraps
from flask import request, jsonify, current_app
import jwt  # Certifique-se de importar o módulo jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # Extrai o token do formato "Bearer <token>"
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token Malformado"}), 401
        
        if not token:
            return jsonify({"message": "Token ausente"}), 401
        
        try:
            # Apenas valida o token, mas não usa os dados
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception as e:
            return jsonify({"message": f"Token inválido: {e}"}), 401
        
        # Passa o token para a função decorada
        return f(token, *args, **kwargs)
    
    return decorated