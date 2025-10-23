"""
Controlador principal da aplicação web usando Bottle.
Implementa o padrão MVC - este é o Controller.
"""
from bottle import Bottle, route, run, template, static_file, request, redirect
import json
import os
import sys

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Colonia, TIPOS_EDIFICIOS

# Inicializa aplicação Bottle
app = Bottle()

# Variável global para armazenar a colônia atual (em produção, usar sessões)
colonia_atual = None


@app.route('/')
def index():
    """
    Rota principal - página inicial.
    Controller que renderiza a View inicial.
    """
    return template('views/index.html')


@app.route('/static/<filepath:path>')
def server_static(filepath):
    """Serve arquivos estáticos (CSS, JS)."""
    return static_file(filepath, root='./static')


@app.route('/novo_jogo', method='POST')
def novo_jogo():
    """
    Cria uma nova colônia.
    Controller que manipula o Model.
    """
    global colonia_atual
    
    nome_colonia = request.forms.get('nome_colonia', 'Nova Colônia')
    
    # Cria nova colônia (Model)
    colonia_atual = Colonia(nome_colonia)
    colonia_atual.salvar()
    
    redirect('/jogo')


@app.route('/carregar_jogo', method='POST')
def carregar_jogo():
    """
    Carrega um jogo salvo.
    Controller que carrega o Model persistido.
    """
    global colonia_atual
    
    # Carrega colônia do arquivo pickle
    colonia_atual = Colonia.carregar()
    
    if colonia_atual is None:
        return template('views/index.html', erro="Nenhum jogo salvo encontrado!")
    
    redirect('/jogo')


@app.route('/jogo')
def jogo():
    """
    Página principal do jogo.
    Controller que passa dados do Model para a View.
    """
    global colonia_atual
    
    if colonia_atual is None:
        redirect('/')
        return
    
    # Obtém dados do Model
    stats = colonia_atual.obter_estatisticas()
    condicoes = colonia_atual.verificar_condicoes()
    
    # Renderiza View com dados do Model
    return template('views/jogo.html', 
                   stats=stats, 
                   condicoes=condicoes,
                   tipos_edificios=TIPOS_EDIFICIOS)


@app.route('/proximo_turno', method='POST')
def proximo_turno():
    """
    Processa o próximo turno.
    Controller que executa lógica do Model.
    """
    global colonia_atual
    
    if colonia_atual is None:
        redirect('/')
        return
    
    # Processa turno no Model
    relatorio = colonia_atual.processar_turno()
    
    redirect('/jogo')


@app.route('/construir/<tipo>', method='POST')
def construir(tipo):
    """
    Constrói um edifício.
    Controller que manipula o Model.
    
    Args:
        tipo: Tipo do edifício a construir
    """
    global colonia_atual
    
    if colonia_atual is None:
        redirect('/')
        return
    
    # Executa ação no Model
    sucesso, mensagem = colonia_atual.construir_edificio(tipo)
    
    redirect('/jogo')


@app.route('/contratar_colono', method='POST')
def contratar_colono():
    """
    Adiciona um novo colono.
    Controller que manipula o Model.
    """
    global colonia_atual
    
    if colonia_atual is None:
        redirect('/')
        return
    
    # Executa ação no Model
    sucesso, mensagem = colonia_atual.adicionar_colono()
    
    redirect('/jogo')


@app.route('/api/status')
def api_status():
    """
    API REST que retorna o status da colônia em JSON.
    Controller que expõe dados do Model via API.
    """
    global colonia_atual
    
    if colonia_atual is None:
        return json.dumps({'erro': 'Nenhuma colônia ativa'})
    
    # Retorna dados do Model em formato JSON
    stats = colonia_atual.obter_estatisticas()
    return json.dumps(stats, ensure_ascii=False, indent=2)


@app.route('/reiniciar', method='POST')
def reiniciar():
    """
    Reinicia o jogo.
    Controller que reseta o Model.
    """
    global colonia_atual
    colonia_atual = None
    
    # Remove arquivo de save
    caminho_save = '/home/ubuntu/colony_game/saves/colonia_save.pkl'
    if os.path.exists(caminho_save):
        os.remove(caminho_save)
    
    redirect('/')


if __name__ == '__main__':
    """
    Ponto de entrada da aplicação.
    Inicia o servidor web Bottle.
    """
    print("=" * 60)
    print("🚀 JOGO DE GERENCIAMENTO DE COLÔNIA")
    print("=" * 60)
    print("Projeto de Orientação a Objetos - UnB")
    print("Demonstra: POO, MVC, Persistência com Pickle")
    print("=" * 60)
    print("\n🌐 Servidor iniciando em http://localhost:8080")
    print("📝 Pressione Ctrl+C para encerrar\n")
    
    # Inicia servidor Bottle
    run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)

