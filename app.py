# -*- coding: utf-8 -*-
"""
Controlador principal da aplicação web usando Bottle.
Implementa o padrão MVC - este é o Controller.
"""
from bottle import Bottle, route, run, template, static_file, request, redirect, response, HTTPResponse
import json
import os
import sys
import traceback

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Colonia, TIPOS_EDIFICIOS
from logger import game_logger

# Inicializa aplicação Bottle
app = Bottle()

# Variáveis globais para sessão (em produção, usar sessões reais)
usuario_logado = None
colonia_atual = None


def carregar_usuarios():
    """Carrega usuários do arquivo JSON."""
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            game_logger.debug(f"Carregados {len(data['usuarios'])} usuários")
            return data['usuarios']
    except Exception as e:
        game_logger.error(f"Erro ao carregar usuários: {e}", exception=e)
        return []


def autenticar(username, password):
    """
    Autentica usuário.
    
    Args:
        username: Nome de usuário
        password: Senha
        
    Returns:
        Dicionário do usuário se autenticado, None caso contrário
    """
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['username'] == username and usuario['password'] == password:
            game_logger.info(f"Login bem-sucedido: {username}")
            return usuario
    game_logger.warning(f"Falha no login: {username}")
    return None


@app.route('/')
def index():
    """
    Rota principal - redireciona para login.
    """
    game_logger.debug("Acesso à rota raiz, redirecionando para login")
    redirect('/login')


@app.route('/login')
def login_page():
    """
    Página de login.
    """
    response.content_type = 'text/html; charset=utf-8'
    game_logger.debug("Exibindo página de login")
    return template('views/login.html')


@app.route('/login', method='POST')
def login_submit():
    """
    Processa login do usuário.
    """
    global usuario_logado, colonia_atual
    
    username = request.forms.get('username', '').strip()
    password = request.forms.get('password', '').strip()
    
    game_logger.info(f"Tentativa de login: {username}")
    usuario = autenticar(username, password)
    
    if usuario is None:
        game_logger.warning(f"Login rejeitado para: {username}")
        response.content_type = 'text/html; charset=utf-8'
        return template('views/login.html', erro="Usuário ou senha inválidos!")
    
    # Usuário autenticado
    usuario_logado = usuario
    game_logger.log_action("LOGIN", usuario=username)
    
    # Tenta carregar colônia do usuário
    save_file = usuario['save_file']
    if os.path.exists(save_file):
        try:
            game_logger.info(f"Carregando colônia salva: {save_file}", usuario=username)
            colonia_atual = Colonia.carregar(save_file)
            if colonia_atual:
                game_logger.info(f"Colônia carregada: {colonia_atual.nome}", usuario=username)
            else:
                game_logger.warning(f"Arquivo existe mas colônia é None: {save_file}", usuario=username)
        except Exception as e:
            game_logger.error(f"ERRO ao carregar colônia de {save_file}: {e}", usuario=username, exception=e)
            colonia_atual = None
    else:
        game_logger.info(f"Nenhum save encontrado para {username}", usuario=username)
        colonia_atual = None
    
    redirect('/menu')


@app.route('/logout')
def logout():
    """
    Faz logout do usuário.
    """
    global usuario_logado, colonia_atual
    
    username = usuario_logado['username'] if usuario_logado else 'desconhecido'
    
    # Salva colônia antes de sair
    if colonia_atual is not None and usuario_logado is not None:
        try:
            save_file = usuario_logado['save_file']
            colonia_atual.salvar(save_file)
            game_logger.info(f"Colônia salva antes do logout: {save_file}", usuario=username)
        except Exception as e:
            game_logger.error(f"Erro ao salvar colônia no logout: {e}", usuario=username, exception=e)
    
    game_logger.log_action("LOGOUT", usuario=username)
    usuario_logado = None
    colonia_atual = None
    
    redirect('/login')


@app.route('/menu')
def menu():
    """
    Menu principal após login.
    """
    global usuario_logado, colonia_atual
    
    if usuario_logado is None:
        game_logger.warning("Acesso ao menu sem autenticação")
        redirect('/login')
        return
    
    response.content_type = 'text/html; charset=utf-8'
    
    # Verifica se usuário tem jogo salvo
    tem_save = colonia_atual is not None
    
    username = usuario_logado['username']
    game_logger.debug(f"Exibindo menu para {username} | Tem save: {tem_save}")
    
    return template('views/index.html', 
                   usuario=usuario_logado,
                   tem_save=tem_save)


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
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        game_logger.warning("Tentativa de criar jogo sem autenticação")
        redirect('/login')
        return
    
    username = usuario_logado['username']
    nome_colonia = request.forms.get('nome_colonia', 'Nova Colônia')
    
    try:
        game_logger.log_action("NOVO_JOGO", usuario=username, details=f"Nome: {nome_colonia}")
        
        # Cria nova colônia (Model)
        colonia_atual = Colonia(nome_colonia)
        colonia_atual.salvar(usuario_logado['save_file'])
        
        game_logger.info(f"Nova colônia criada e salva: {nome_colonia}", usuario=username)
        game_logger.log_game_event("COLONIA_CRIADA", nome_colonia, f"Usuário: {username}")
    except Exception as e:
        game_logger.error(f"Erro ao criar nova colônia: {e}", usuario=username, exception=e)
    
    redirect('/jogo')


@app.route('/carregar_jogo', method='POST')
def carregar_jogo():
    """
    Carrega um jogo salvo do usuário.
    Controller que carrega o Model persistido.
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        game_logger.warning("Tentativa de carregar jogo sem autenticação")
        redirect('/login')
        return
    
    username = usuario_logado['username']
    save_file = usuario_logado['save_file']
    
    game_logger.log_action("CARREGAR_JOGO", usuario=username, details=f"Arquivo: {save_file}")
    
    if not os.path.exists(save_file):
        game_logger.warning(f"Arquivo de save não encontrado: {save_file}", usuario=username)
        response.content_type = 'text/html; charset=utf-8'
        return template('views/index.html', 
                       usuario=usuario_logado,
                       tem_save=False,
                       erro="Nenhum jogo salvo encontrado!")
    
    try:
        game_logger.info(f"Carregando jogo de: {save_file}", usuario=username)
        colonia_atual = Colonia.carregar(save_file)
        
        if colonia_atual is None:
            game_logger.error(f"Colonia.carregar() retornou None para: {save_file}", usuario=username)
            raise Exception("Arquivo corrompido ou incompatível")
        
        game_logger.info(f"Jogo carregado com sucesso: {colonia_atual.nome} (Dia {colonia_atual.dia})", usuario=username)
        redirect('/jogo')
    except HTTPResponse:
        # Redirecionamento do Bottle - não é erro, é comportamento normal
        raise
    except Exception as e:
        game_logger.error(f"ERRO CRÍTICO ao carregar jogo: {e}", usuario=username, exception=e)
        game_logger.error(f"Traceback completo: {traceback.format_exc()}", usuario=username)
        
        response.content_type = 'text/html; charset=utf-8'
        return template('views/index.html', 
                       usuario=usuario_logado,
                       tem_save=False,
                       erro=f"Erro ao carregar jogo: {str(e)}")


@app.route('/jogo')
def jogo():
    """
    Página principal do jogo.
    Controller que passa dados do Model para a View.
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        game_logger.warning("Acesso ao jogo sem autenticação")
        redirect('/login')
        return
    
    if colonia_atual is None:
        username = usuario_logado['username']
        game_logger.warning(f"Acesso ao jogo sem colônia ativa", usuario=username)
        redirect('/menu')
        return
    
    try:
        # Obtém dados do Model
        stats = colonia_atual.obter_estatisticas()
        condicoes = colonia_atual.verificar_condicoes()
        
        # Renderiza View com dados do Model
        response.content_type = 'text/html; charset=utf-8'
        return template('views/jogo.html', 
                       stats=stats, 
                       condicoes=condicoes,
                       tipos_edificios=TIPOS_EDIFICIOS,
                       usuario=usuario_logado)
    except HTTPResponse:
        raise
    except Exception as e:
        username = usuario_logado['username']
        game_logger.error(f"Erro ao renderizar página do jogo: {e}", usuario=username, exception=e)
        redirect('/menu')


@app.route('/proximo_turno', method='POST')
def proximo_turno():
    """
    Processa o próximo turno.
    Controller que executa lógica do Model.
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        redirect('/login')
        return
    
    if colonia_atual is None:
        redirect('/menu')
        return
    
    username = usuario_logado['username']
    
    try:
        dia_anterior = colonia_atual.dia
        
        # Processa turno no Model
        relatorio = colonia_atual.processar_turno()
        
        game_logger.log_action("PROXIMO_TURNO", usuario=username, 
                              details=f"Dia {dia_anterior} → {colonia_atual.dia}")
        game_logger.log_game_event("TURNO_PROCESSADO", colonia_atual.nome, 
                                   f"Dia {colonia_atual.dia}")
        
        # Salva automaticamente
        colonia_atual.salvar(usuario_logado['save_file'])
        game_logger.debug(f"Jogo salvo automaticamente", usuario=username)
    except Exception as e:
        game_logger.error(f"Erro ao processar turno: {e}", usuario=username, exception=e)
    
    redirect('/jogo')


@app.route('/construir/<tipo>', method='POST')
def construir(tipo):
    """
    Constrói um edifício.
    Controller que manipula o Model.
    
    Args:
        tipo: Tipo do edifício a construir
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        redirect('/login')
        return
    
    if colonia_atual is None:
        redirect('/menu')
        return
    
    username = usuario_logado['username']
    
    try:
        game_logger.log_action("CONSTRUIR", usuario=username, details=f"Tipo: {tipo}")
        
        # Executa ação no Model
        sucesso, mensagem = colonia_atual.construir_edificio(tipo)
        
        if sucesso:
            game_logger.info(f"Edifício construído: {tipo}", usuario=username)
            game_logger.log_game_event("EDIFICIO_CONSTRUIDO", colonia_atual.nome, 
                                       f"Tipo: {tipo}")
        else:
            game_logger.warning(f"Falha ao construir {tipo}: {mensagem}", usuario=username)
        
        # Salva automaticamente
        colonia_atual.salvar(usuario_logado['save_file'])
    except Exception as e:
        game_logger.error(f"Erro ao construir edifício {tipo}: {e}", usuario=username, exception=e)
    
    redirect('/jogo')


@app.route('/contratar_colono', method='POST')
def contratar_colono():
    """
    Adiciona um novo colono.
    Controller que manipula o Model.
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        redirect('/login')
        return
    
    if colonia_atual is None:
        redirect('/menu')
        return
    
    username = usuario_logado['username']
    
    try:
        game_logger.log_action("CONTRATAR_COLONO", usuario=username)
        
        # Executa ação no Model
        sucesso, mensagem = colonia_atual.adicionar_colono()
        
        if sucesso:
            game_logger.info(f"Colono contratado", usuario=username)
            game_logger.log_game_event("COLONO_CONTRATADO", colonia_atual.nome, 
                                       f"Total: {colonia_atual.total_colonos_vivos}")
        else:
            game_logger.warning(f"Falha ao contratar colono: {mensagem}", usuario=username)
        
        # Salva automaticamente
        colonia_atual.salvar(usuario_logado['save_file'])
    except Exception as e:
        game_logger.error(f"Erro ao contratar colono: {e}", usuario=username, exception=e)
    
    redirect('/jogo')


@app.route('/api/status')
def api_status():
    """
    API REST que retorna o status da colônia em JSON.
    Controller que expõe dados do Model via API.
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({'erro': 'Usuário não autenticado'}, ensure_ascii=False)
    
    if colonia_atual is None:
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({'erro': 'Nenhuma colônia ativa'}, ensure_ascii=False)
    
    try:
        # Retorna dados do Model em formato JSON
        stats = colonia_atual.obter_estatisticas()
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps(stats, ensure_ascii=False, indent=2)
    except Exception as e:
        username = usuario_logado['username']
        game_logger.error(f"Erro na API status: {e}", usuario=username, exception=e)
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({'erro': str(e)}, ensure_ascii=False)


@app.route('/reiniciar', method='POST')
def reiniciar():
    """
    Reinicia o jogo do usuário.
    Controller que reseta o Model.
    """
    global colonia_atual, usuario_logado
    
    if usuario_logado is None:
        redirect('/login')
        return
    
    username = usuario_logado['username']
    save_file = usuario_logado['save_file']
    
    try:
        game_logger.log_action("REINICIAR", usuario=username)
        
        colonia_atual = None
        
        # Remove arquivo de save do usuário
        if os.path.exists(save_file):
            os.remove(save_file)
            game_logger.info(f"Save removido: {save_file}", usuario=username)
    except Exception as e:
        game_logger.error(f"Erro ao reiniciar jogo: {e}", usuario=username, exception=e)
    
    redirect('/menu')


@app.route('/logs')
def view_logs():
    """
    Visualiza logs do sistema (apenas para admin).
    """
    global usuario_logado
    
    if usuario_logado is None or usuario_logado['username'] != 'admin':
        game_logger.warning(f"Tentativa de acesso aos logs sem permissão")
        redirect('/login')
        return
    
    try:
        logs_recentes = game_logger.get_recent_logs(lines=100, level='INFO')
        logs_erro = game_logger.get_error_logs(lines=50)
        
        response.content_type = 'text/html; charset=utf-8'
        return template('views/logs.html', 
                       logs=logs_recentes,
                       erros=logs_erro,
                       usuario=usuario_logado)
    except Exception as e:
        game_logger.error(f"Erro ao exibir logs: {e}", exception=e)
        return f"Erro ao carregar logs: {e}"


if __name__ == '__main__':
    """
    Ponto de entrada da aplicação.
    Inicia o servidor web Bottle.
    """
    game_logger.info("=" * 60)
    game_logger.info("🚀 JOGO DE GERENCIAMENTO DE COLÔNIA")
    game_logger.info("=" * 60)
    game_logger.info("Projeto de Orientação a Objetos - UnB")
    game_logger.info("Demonstra: POO, MVC, Persistência com Pickle")
    game_logger.info("=" * 60)
    game_logger.info("🌐 Servidor iniciando em http://localhost:8080")
    game_logger.info("📝 Pressione Ctrl+C para encerrar")
    game_logger.info("=" * 60)
    
    # Cria diretório de saves se não existir
    if not os.path.exists('saves'):
        os.makedirs('saves')
        game_logger.info("Diretório 'saves' criado")
    
    # Inicia servidor Bottle
    try:
        run(app, host='0.0.0.0', port=8080, debug=True, reloader=True)
    except KeyboardInterrupt:
        game_logger.info("Servidor encerrado pelo usuário")
    except Exception as e:
        game_logger.critical(f"Erro crítico no servidor: {e}", exception=e)

