# -*- coding: utf-8 -*-
"""
Sistema de logging para o jogo.
Registra todas as ações, erros e eventos importantes.
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class GameLogger:
    """
    Classe para gerenciar logs do jogo.
    Implementa singleton pattern para garantir única instância.
    """
    
    _instance = None
    
    def __new__(cls):
        """Implementa Singleton."""
        if cls._instance is None:
            cls._instance = super(GameLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa o logger se ainda não foi inicializado."""
        if self._initialized:
            return
        
        self._initialized = True
        
        # Cria diretório de logs se não existir
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configura logger principal
        self.logger = logging.getLogger('ColonyGame')
        self.logger.setLevel(logging.DEBUG)
        
        # Remove handlers existentes
        self.logger.handlers = []
        
        # Formato dos logs
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para arquivo (rotativo, máximo 5MB, 5 backups)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'colony_game.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para console (apenas INFO e acima)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler separado para erros críticos
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, 'errors.log'),
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
        
        self.info("Sistema de logging inicializado")
    
    def debug(self, message, usuario=None):
        """Log de debug."""
        msg = f"[{usuario}] {message}" if usuario else message
        self.logger.debug(msg)
    
    def info(self, message, usuario=None):
        """Log de informação."""
        msg = f"[{usuario}] {message}" if usuario else message
        self.logger.info(msg)
    
    def warning(self, message, usuario=None):
        """Log de aviso."""
        msg = f"[{usuario}] {message}" if usuario else message
        self.logger.warning(msg)
    
    def error(self, message, usuario=None, exception=None):
        """Log de erro."""
        msg = f"[{usuario}] {message}" if usuario else message
        if exception:
            msg += f" | Exception: {type(exception).__name__}: {str(exception)}"
        self.logger.error(msg, exc_info=exception is not None)
    
    def critical(self, message, usuario=None, exception=None):
        """Log crítico."""
        msg = f"[{usuario}] {message}" if usuario else message
        if exception:
            msg += f" | Exception: {type(exception).__name__}: {str(exception)}"
        self.logger.critical(msg, exc_info=exception is not None)
    
    def log_action(self, action, usuario=None, details=None):
        """
        Registra uma ação do usuário.
        
        Args:
            action: Nome da ação
            usuario: Usuário que executou
            details: Detalhes adicionais
        """
        msg = f"ACTION: {action}"
        if details:
            msg += f" | {details}"
        self.info(msg, usuario)
    
    def log_game_event(self, event_type, colonia_nome, details):
        """
        Registra um evento do jogo.
        
        Args:
            event_type: Tipo do evento
            colonia_nome: Nome da colônia
            details: Detalhes do evento
        """
        msg = f"GAME_EVENT: {event_type} | Colônia: {colonia_nome} | {details}"
        self.info(msg)
    
    def get_recent_logs(self, lines=50, level='INFO'):
        """
        Retorna os logs recentes.
        
        Args:
            lines: Número de linhas
            level: Nível mínimo (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Lista de strings com os logs
        """
        log_file = 'logs/colony_game.log'
        if not os.path.exists(log_file):
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            # Filtra por nível se especificado
            if level != 'DEBUG':
                levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
                min_index = levels.index(level)
                allowed_levels = levels[:min_index + 1]
                
                filtered_lines = []
                for line in all_lines:
                    if any(f'| {lvl}' in line for lvl in allowed_levels):
                        filtered_lines.append(line)
                all_lines = filtered_lines
            
            # Retorna últimas N linhas
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            self.error(f"Erro ao ler logs: {e}", exception=e)
            return []
    
    def get_error_logs(self, lines=20):
        """
        Retorna apenas logs de erro.
        
        Args:
            lines: Número de linhas
            
        Returns:
            Lista de strings com os erros
        """
        error_file = 'logs/errors.log'
        if not os.path.exists(error_file):
            return []
        
        try:
            with open(error_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            return [f"Erro ao ler arquivo de erros: {e}"]


# Instância global do logger
game_logger = GameLogger()

