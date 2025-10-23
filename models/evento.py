"""
Classe para eventos aleatórios que afetam a colônia.
Demonstra: Encapsulamento, Composição
"""
import random


class EventoAleatorio:
    """
    Representa um evento aleatório que pode ocorrer na colônia.
    Demonstra encapsulamento e composição.
    """
    
    # Tipos de eventos possíveis
    EVENTOS = [
        {
            'tipo': 'tempestade_solar',
            'nome': 'Tempestade Solar',
            'descricao': 'Uma tempestade solar danificou alguns geradores de energia!',
            'efeitos': {'energia': -20},
            'probabilidade': 0.15
        },
        {
            'tipo': 'descoberta_recursos',
            'nome': 'Descoberta de Recursos',
            'descricao': 'Os colonos descobriram um depósito de metal!',
            'efeitos': {'metal': 50},
            'probabilidade': 0.20
        },
        {
            'tipo': 'colheita_abundante',
            'nome': 'Colheita Abundante',
            'descricao': 'As fazendas produziram uma colheita excepcional!',
            'efeitos': {'comida': 30},
            'probabilidade': 0.18
        },
        {
            'tipo': 'contaminacao_agua',
            'nome': 'Contaminação de Água',
            'descricao': 'Parte do suprimento de água foi contaminado!',
            'efeitos': {'agua': -15},
            'probabilidade': 0.12
        },
        {
            'tipo': 'moral_alta',
            'nome': 'Moral Alta',
            'descricao': 'Os colonos estão animados e motivados!',
            'efeitos': {'felicidade_bonus': 10},
            'probabilidade': 0.25
        },
        {
            'tipo': 'epidemia',
            'nome': 'Epidemia',
            'descricao': 'Uma doença está se espalhando pela colônia!',
            'efeitos': {'saude_bonus': -15},
            'probabilidade': 0.10
        },
        {
            'tipo': 'novo_colono',
            'nome': 'Novo Colono',
            'descricao': 'Um viajante solitário pediu para se juntar à colônia!',
            'efeitos': {'novo_colono': True},
            'probabilidade': 0.15
        },
        {
            'tipo': 'avanco_tecnologico',
            'nome': 'Avanço Tecnológico',
            'descricao': 'Os cientistas fizeram uma descoberta que melhora a eficiência!',
            'efeitos': {'eficiencia_bonus': 1.2},
            'probabilidade': 0.08
        }
    ]
    
    def __init__(self, tipo: str = None, nome: str = None, descricao: str = None, efeitos: dict = None):
        """
        Inicializa um evento.
        
        Args:
            tipo: Tipo do evento
            nome: Nome do evento
            descricao: Descrição do evento
            efeitos: Dicionário com os efeitos do evento
        """
        self.__tipo = tipo or ''
        self.__nome = nome or ''
        self.__descricao = descricao or ''
        self.__efeitos = efeitos or {}
        self.__aplicado = False
    
    @property
    def tipo(self) -> str:
        """Retorna o tipo do evento."""
        return self.__tipo
    
    @property
    def nome(self) -> str:
        """Retorna o nome do evento."""
        return self.__nome
    
    @property
    def descricao(self) -> str:
        """Retorna a descrição do evento."""
        return self.__descricao
    
    @property
    def efeitos(self) -> dict:
        """Retorna os efeitos do evento."""
        return self.__efeitos.copy()
    
    @property
    def foi_aplicado(self) -> bool:
        """Verifica se o evento já foi aplicado."""
        return self.__aplicado
    
    @classmethod
    def gerar_evento_aleatorio(cls) -> 'EventoAleatorio':
        """
        Gera um evento aleatório baseado nas probabilidades.
        
        Returns:
            Instância de EventoAleatorio ou None
        """
        if random.random() > 0.3:  # 30% de chance de evento ocorrer
            return None
        
        # Seleciona evento baseado em probabilidades
        eventos_possiveis = []
        pesos = []
        
        for evento_data in cls.EVENTOS:
            eventos_possiveis.append(evento_data)
            pesos.append(evento_data['probabilidade'])
        
        evento_selecionado = random.choices(eventos_possiveis, weights=pesos, k=1)[0]
        
        return cls(
            tipo=evento_selecionado['tipo'],
            nome=evento_selecionado['nome'],
            descricao=evento_selecionado['descricao'],
            efeitos=evento_selecionado['efeitos'].copy()
        )
    
    def aplicar(self, colonia) -> str:
        """
        Aplica os efeitos do evento na colônia.
        Demonstra composição - evento interage com colônia.
        
        Args:
            colonia: Instância da colônia
            
        Returns:
            Mensagem descrevendo o que aconteceu
        """
        if self.__aplicado:
            return "Evento já foi aplicado"
        
        mensagens = [self.__descricao]
        
        # Aplica efeitos em recursos
        for recurso in ['comida', 'agua', 'energia', 'metal']:
            if recurso in self.__efeitos:
                valor = self.__efeitos[recurso]
                if valor > 0:
                    colonia.recursos[recurso].adicionar(valor)
                    mensagens.append(f"+{valor} {recurso}")
                else:
                    colonia.recursos[recurso].remover(abs(valor))
                    mensagens.append(f"{valor} {recurso}")
        
        # Aplica efeitos em colonos
        if 'felicidade_bonus' in self.__efeitos:
            bonus = self.__efeitos['felicidade_bonus']
            for colono in colonia.colonos:
                if colono.esta_vivo:
                    colono.felicidade = colono.felicidade + bonus
            mensagens.append(f"Felicidade dos colonos: {bonus:+d}")
        
        if 'saude_bonus' in self.__efeitos:
            bonus = self.__efeitos['saude_bonus']
            for colono in colonia.colonos:
                if colono.esta_vivo:
                    colono.saude = colono.saude + bonus
            mensagens.append(f"Saúde dos colonos: {bonus:+d}")
        
        # Adiciona novo colono
        if self.__efeitos.get('novo_colono', False):
            colonia.adicionar_colono()
            mensagens.append("Um novo colono se juntou à colônia!")
        
        # Bonus de eficiência (armazenado para uso posterior)
        if 'eficiencia_bonus' in self.__efeitos:
            colonia._bonus_eficiencia = self.__efeitos['eficiencia_bonus']
            mensagens.append(f"Eficiência aumentada em {(self.__efeitos['eficiencia_bonus']-1)*100:.0f}%!")
        
        self.__aplicado = True
        return " | ".join(mensagens)
    
    def to_dict(self) -> dict:
        """Converte o evento para dicionário."""
        return {
            'tipo': self.__tipo,
            'nome': self.__nome,
            'descricao': self.__descricao,
            'efeitos': self.__efeitos,
            'aplicado': self.__aplicado
        }
    
    def __str__(self) -> str:
        """Representação em string do evento."""
        return f"{self.__nome}: {self.__descricao}"

