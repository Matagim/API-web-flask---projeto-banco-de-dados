from flask import Flask, request, jsonify

import psycopg2

app = Flask(__name__)

def conectar():
    bd = psycopg2.connect(
        host="database-1.cqryy0a1cnxv.us-east-1.rds.amazonaws.com",
        database="postgres",
        user="professor",
        password="professor"
    )
    return bd
        

@app.route('/usuario', methods=['POST'])
def criar_usuario():


    try:
        dados = request.json
        if not dados:
            return jsonify({"erro": "Corpo da requisição vazio"})
        
        cpf = dados.get('cpf')
        nome = dados.get('nome')
        data_nascimento = dados.get('data_nascimento')
        bd = conectar()
        cursor = bd.cursor()
        
        cursor.execute(
            """
            INSERT INTO atv.usuario (cpf, nome, data_nascimento) VALUES (%s, %s, %s)
            """,
            (cpf,nome,data_nascimento)
        )
        bd.commit()
        cursor.close()
        bd.close()
        return jsonify("Relaxa que tá criado!")
    except (psycopg2.Error, ConnectionError) as e:
        bd.rollback()
        return jsonify({"erro": str(e)})
        


@app.route('/usuario', methods=['GET'])
def obter_usuario():
    
    if request.content_type != 'application/json':
        return jsonify({"erro": "Content-Type deve ser application/json"})
    
    try:
        
        dados = request.json
        if not dados:
            return jsonify({"erro": "Corpo da requisição vazio"})

        cpf = dados.get('cpf')

        bd = conectar()
        cursor = bd.cursor()
  
        cursor.execute(
            """
            SELECT cpf, nome, data_nascimento FROM atv.usuario WHERE cpf = %s
            """,
            (cpf,)
        )
        usuario = cursor.fetchone()
        cursor.close()
        bd.close()
        if usuario:
            return jsonify({"cpf": usuario[0], "nome": usuario[1], "data_nascimento": usuario[2]})
        else:
            return jsonify({"erro": "Usuário não encontrado"})

    except (psycopg2.Error, ConnectionError) as e:
        return jsonify({"erro": str(e)})   

if __name__ == '__main__':
    app.run(debug=True)
