from flasgger import Swagger
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração do Swagger
template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Cadastro de Empresas",
        "description": "Endpoints para realizar operações de CRUD em registros de empresas",
        "version": "1.0"   
    },
    "tags": [
        {
            "name": "Empresas",
            "description": "Operações relacionadas ao cadastro de empresas"
        }
    ],
    "basePath": "/",
    "schemes":["http", "https"]
}
swagger = Swagger(app, template=template)


# Simulando lista de empresas
empresas = [
    {
        "cnpj": "11111111111111",
        "nome_razao": "Empresa 1 LTDA",
        "nome_fantasia": "Empre1",
        "cnae": "1234-5/00"
    },
    {
        "cnpj": "22222222222222",
        "nome_razao": "Empresa 2 S.A.",
        "nome_fantasia": "Empre2",
        "cnae": "5678-9/00"
    },
    # Mais empresas aqui...
]

#Endpoint para cadastrar uma nova empresa
@app.route('/empresas/', methods=['POST'])


def cadastrar_empresa():
    nova_empresa = request.get_json()
    if 'cnpj' not in nova_empresa or 'name_razao' not in nova_empresa or 'nome_fantasia' not in nova_empresa or 'cnae' not in nova_empresa:
        return jsonify({'erro': 'Os campos CNPJ, Nome Razão, Nome Fantasia  e CNAE são obrigatórios'}), 400

    empresas.append(nova_empresa)
    return jsonify({'messagem': 'Empresa cadastrada com sucesso'}), 201

#Endpoint para editar uma empresa existente
@app.route('/empresas/<string:cnpj>', methods=['PUT'])
def editar_empresa(cnpj):
    empresa_editada = request.get_json()
    for empresa in empresas:
        if empresa['cnpj'] == cnpj:
            if 'nome_fantasia' in empresa_editada:
                empresa['nome_fantasia'] = empresa_editada['nome_fantasia']
            if 'cnae' in empresa_editada:
                empresa['cnae'] = empresa_editada['cnae']
            return jsonify({'mensagem': 'Empresa editada com sucesso'}), 200
    return jsonify({'erro': 'Empresa não encontrada'}), 404

#Endpoint para remover uma empresa existente
@app.route('/empresas/<string:cnpj>', methods=['DELETE'])
def remover_empresa(cnpj):
    for empresa in empresas:
        if empresa['cnpj'] == cnpj:
            empresas.remove(empresa)
            return jsonify({'mensagem': 'Empresa removida com sucesso'}), 200
    return jsonify({'erro': 'Empresa não encontrada'}), 404

#Endpoint de listagem e empresas para paginação, ordenação e limite
@app.route('/empresas/', methods=['GET'])
def listar_empresas():
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('limit', 10))
    sort = request.args.get('sort', 'cnpj')
    dir = request.args.get('dir', 'asc')

    ordenando_empresas = sorted(empresas, key=lambda x: x[sort], reverse=(dir == 'desc'))
    empresas_paginadas = ordenando_empresas[start:start + limit]

    return jsonify(empresas_paginadas), 200

if __name__=='__main__':
    app.run(debug=True)