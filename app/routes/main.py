from flask import Blueprint, jsonify, request
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import *

main_bp = Blueprint('main_bp', __name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data =LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"message": f"Erro: {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"Erro: {e}"}), 500

    if user_data.username == 'rondi' and user_data.password == '123':
        return jsonify({"message": f"Logado com sucesso: {user_data.model_dump_json()}"})
    else:
        return jsonify({"message": "Credenciais incorretas"})    


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = []  # Inicializa a lista vazia
    
    for product in products_cursor:  # Loop sobre cada produto
        # Cria o modelo Pydantic e converte para dicionário
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        # Adiciona o dicionário à lista
        products_list.append(product_model)
    return jsonify(products_list)

# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route('/products', methods=['POST'])
def create_product():
    return jsonify({"message":"Esta é a rota de criação de produto"})

# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"menssage": f"Erro ao transformar o {product_id} em ObjectID {e}"})

    product = db.products.find_one({'_id': oid})
    
    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({"error": f"Produto com o id: {product_id} - Não encontrado"})
    
# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message":f"Esta é a rota de atualizacao do produto com o id {product_id}"})

# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({"message":f"Esta é a rota de deleção do produto com o id {product_id}"})

# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message":"Esta é a rota de upload do arquivo de vendas"})