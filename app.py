from flasgger import Swagger
from flasgger import swag_from

from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'


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
]

# Validação do formato do CNPJ
def is_valid_cnpj(cnpj):
    # Remover caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verificar se o CNPJ tem 14 digitos
    if len(cnpj) != 14:
        return False
    
    # Verificar se todos os digitos são iguais (CNPJs inválidos)
    if cnpj == cnpj[0] * 14:
        return False

    # Cálculo do primeiro digito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1
    primeiro_digito = 11 - (soma % 11) if soma % 11 > 1 else 0

    # Cálculo do segundo digito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso = 9 if peso == 2 else peso - 1 
    segundo_digito = 11 - (soma % 11) if soma % 11 > 1 else 0

    # Verificar se os digitos verificadores calculados batema com o fornecidos
    if int(cnpj[12]) != primeiro_digito or int(cnpj[13]) != segundo_digito:
        return False
    
    return True

#Endpoint para cadastrar uma nova empresa
@app.route('/empresas/', methods=['POST'])

@swag_from({
    'summary': 'Cadastrar uma nova empresa',
    'tags': ['Empresas'],
    'parameters': [
        {
            'name': 'empreasa',
            'description': 'Dados da nova empresa',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'cnpj': {'type': 'string'},
                    'nome_razao': {'type':'string'},
                    'nome_fantasia':{'type':'string'},
                    'cnae':{'type':'string'}
                }
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Empresa cadastrada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'mensagem': {'type':'string'}
                }
            }
        },
        '400': {
            'description': 'Requisição inválida',
            'schema': {
                'type': 'object',
                'properties': {
                    'erro': {'type': 'string'}
                }
            }
        }
    }
})

def cadastrar_empresa():
    nova_empresa = request.get_json()
    if "cnpj" not in nova_empresa or "nome_razao" not in nova_empresa or "nome_fantasia" not in nova_empresa or "cnae" not in nova_empresa:
        return jsonify({"erro": "Os campos CNPJ, Nome Razão, Nome Fantasia e CNAE são obrigatórios"}), 400
    
    # Validar o formato do CNPJ antes de salvar a empresa
    if not is_valid_cnpj(nova_empresa['cnpj']):
        return jsonify({"erro": "CNPJ inválido"}), 400

    empresas.append(nova_empresa)
    return jsonify({"mensagem": "Empresa cadastrada com sucesso"}), 201


#Endpoint para editar uma empresa existente
@app.route('/empresas/<string:cnpj>/', methods=['PUT'])

@swag_from({
    'summary': 'Editar uma empresa exitente',
    'tags': ['Empresa'],
    'parameters': [
        {
            'name':'cnpj',
            'description': 'CNPJ da empresa a ser editada',
            'in': 'patg',
            'type': 'string',
            'required': True
        },
        {
            'name': 'empresa',
            'description': 'Dados da empresa a serem atualizados',
            'in': 'body',
            'required': True,
            'schema': {
                'type':'object',
                'properties': {
                    'nome_fantasia': {'type':'string'},
                    'cnae': {'type':'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Empresa editada com sucesso',
            'schema': {
                'type':'object',
                'properties': {
                    'mensagem': {'type':'string'}
                }
            }
        },
        '404': {
            'description':'Empresa não encontrada',
            'schema': {
                'type':'object',
                'properties': {
                    'erro': {'type':'string'}
                }
            }
        }
    }
})

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

@swag_from({
    'summary': 'Remover uma empresa existente',
    'tags': ['Empresas'],
    'parameters': [
        {
            'name': 'cnpj',
            'description': 'CNPJ da empresa a ser removida',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description':'Empresas removida com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'mensagem':{'type':'string'}
                }
            }
        },
        '404': {
            'description': 'Empresa não encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'erro': {'type':'string'}
                }
            }
        }
    }  
})

def remover_empresa(cnpj):
    for empresa in empresas:
        if empresa['cnpj'] == cnpj:
            empresas.remove(empresa)
            return jsonify({'mensagem': 'Empresa removida com sucesso'}), 200
    return jsonify({'erro': 'Empresa não encontrada'}), 404


#Endpoint de listagem e empresas para paginação, ordenação e limite
@app.route('/empresas/', methods=['GET'])

@swag_from({
    'summary': 'Listar empresas',
    'tags': ['Empresas'],
    'parameters':[
        {
            'name': 'start',
            'description': 'Indice de início para a paginação',
            'in': 'query',
            'type': 'integer',
            'default': 0
        },
        {
            'name': 'limit',
            'description': 'Número máximo de registros por página',
            'in': 'query',
            'type': 'integer',
            'default': 10
        },
        {
            'name': 'sort',
            'description': 'Campo para ordenação (cnpj, nome_razao, nome_fantasia, cnae)',
            'in':'query',
            'type': 'string',
            'default': 'cnpj'
        },
        {
            'name': 'dir',
            'description': 'Direção da ordenação (asc ou desc)',
            'in': 'query',
            'type':'string',
            'default': 'asc'
        }
    ],
    'responses': {
        '200':{
            'description':'Lista de empresas',
            'schema': {
                'type': 'array',
                'items': {
                    'type':' object',
                    'properties': {
                        'cnpj': {'type': 'string'},
                        'nome_razao': {'type':'string'},
                        'nome_fantasia': {'type':'string'},
                        'cnae': {'type':'string'}
                    }
                }
            }
        }
    }
})



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