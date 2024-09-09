from flask import Flask, request, jsonify
from datetime import datetime
from datetime import date
import psycopg2

app = Flask(__name__)
    
def conectar(info):

    bd = psycopg2.connect(
        host = info['host'],
        database = info['database'],
        user = info['user'],
        password = info['password']
    )
    return bd
        

@app.route('/usuario', methods=['POST'])
def criar_usuario():
    dados = request.json

    host = dados.get('host')
    database = dados.get('database')
    user = dados.get('user')
    password = dados.get('password')

    cpf = dados.get('cpf')
    nome = dados.get('nome')
    data_nascimento = dados.get('data_nascimento')
    info_bd = {
        'host': host,
        'database': database,
        'user': user,
        'password': password
    }
    bd = conectar(info_bd)
    try:
        
        cursor = bd.cursor()
        
        cursor.execute(
            """
            INSERT INTO atv.usuario (cpf, nome, data_nascimento) VALUES (%s,%s,%s)
            """,
            (cpf,nome,data_nascimento)
        )
        bd.commit()
        
        return jsonify({"nice"})
    except Exception as e:
        bd.rollback()
        return jsonify({"erro": str(e)})
    


@app.route('/usuario', methods=['GET'])
def obter_usuario():
    dados = request.json
    host = dados.get('host')
    database = dados.get('database')
    user = dados.get('user')
    password = dados.get('password')
    cpf = dados.get('cpf')
    info_bd = {
        'host': host,
        'database': database,
        'user': user,
        'password': password
    }
    bd = conectar(info_bd)
    try:
        
        cursor = bd.cursor()
        cursor.execute(
            """
            SELECT cpf, nome, data_nascimento FROM atv.usuario WHERE cpf = %s
            """,
            (cpf,)
        )
        usuario = cursor.fetchone()

        return jsonify({"cpf": usuario[0],"nome": usuario[1], "data_nascimento": usuario[2]})
    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
