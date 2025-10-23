"""
Classe Colono - representa um habitante da colônia.
Demonstra: Herança, Polimorfismo, Encapsulamento
"""
from models.entidade import Entidade
import random


class Colono(Entidade):
    """
    Representa um colono da colônia.
    Demonstra herança da classe Entidade e polimorfismo.
    """
    
    # Constantes de classe
    PROFISSOES = ['Agricultor', 'Engenheiro', 'Cientista', 'Minerador', 'Médico']
    CONSUMO_COMIDA = 5
    CONSUMO_AGUA = 3
    
    def __init__(self, nome: str, profissao: str = None):
        """
        Inicializa um colono.
        
        Args:
            nome: Nome do colono
            profissao: Profissão do colono (aleatória se não especificada)
        """
        super().__init__(nome, f"Colono trabalhando como {profissao or 'indefinido'}")
        
        # Atributos privados específicos do colono
        self.__saude = 100
        self.__felicidade = 80
        self.__profissao = profissao or random.choice(self.PROFISSOES)
        self.__produtividade = 1.0
        self.__dias_trabalhados = 0
    
    # Getters
    @property
    def saude(self) -> int:
        """Retorna a saúde do colono (0-100)."""
        return self.__saude
    
    @property
    def felicidade(self) -> int:
        """Retorna a felicidade do colono (0-100)."""
        return self.__felicidade
    
    @property
    def profissao(self) -> str:
        """Retorna a profissão do colono."""
        return self.__profissao
    
    @property
    def produtividade(self) -> float:
        """Retorna a produtividade do colono."""
        return self.__produtividade
    
    @property
    def dias_trabalhados(self) -> int:
        """Retorna quantos dias o colono trabalhou."""
        return self.__dias_trabalhados
    
    @property
    def esta_vivo(self) -> bool:
        """Verifica se o colono está vivo."""
        return self.__saude > 0
    
    # Setters com validação
    @saude.setter
    def saude(self, valor: int):
        """Define a saúde do colono (0-100)."""
        self.__saude = max(0, min(100, valor))
    
    @felicidade.setter
    def felicidade(self, valor: int):
        """Define a felicidade do colono (0-100)."""
        self.__felicidade = max(0, min(100, valor))
    
    @profissao.setter
    def profissao(self, valor: str):
        """Define a profissão do colono."""
        if valor not in self.PROFISSOES:
            raise ValueError(f"Profissão inválida. Escolha entre: {', '.join(self.PROFISSOES)}")
        self.__profissao = valor
        self.descricao = f"Colono trabalhando como {valor}"
    
    def trabalhar(self) -> float:
        """
        Colono trabalha e retorna sua produtividade.
        Demonstra polimorfismo - comportamento específico da subclasse.
        
        Returns:
            Valor de produtividade do trabalho
        """
        if not self.esta_vivo:
            return 0
        
        self.__dias_trabalhados += 1
        
        # Produtividade baseada em saúde e felicidade
        self.__produtividade = (self.__saude / 100) * (self.__felicidade / 100) * 1.5
        
        # Bonus por profissão
        bonus_profissao = {
            'Agricultor': 1.2,
            'Engenheiro': 1.3,
            'Cientista': 1.1,
            'Minerador': 1.25,
            'Médico': 1.15
        }
        self.__produtividade *= bonus_profissao.get(self.__profissao, 1.0)
        
        # Trabalho causa pequeno desgaste
        self.__saude -= random.randint(1, 3)
        self.__felicidade -= random.randint(1, 2)
        
        return self.__produtividade
    
    def descansar(self):
        """
        Colono descansa e recupera saúde e felicidade.
        """
        if not self.esta_vivo:
            return
        
        self.__saude = min(100, self.__saude + random.randint(5, 10))
        self.__felicidade = min(100, self.__felicidade + random.randint(3, 7))
    
    def consumir_recursos(self, comida_disponivel: float, agua_disponivel: float) -> tuple:
        """
        Colono consome recursos necessários.
        
        Args:
            comida_disponivel: Quantidade de comida disponível
            agua_disponivel: Quantidade de água disponível
            
        Returns:
            Tupla (comida_consumida, agua_consumida)
        """
        if not self.esta_vivo:
            return (0, 0)
        
        comida_consumida = min(self.CONSUMO_COMIDA, comida_disponivel)
        agua_consumida = min(self.CONSUMO_AGUA, agua_disponivel)
        
        # Penalidades por falta de recursos
        if comida_consumida < self.CONSUMO_COMIDA:
            self.__saude -= 10
            self.__felicidade -= 15
        
        if agua_consumida < self.CONSUMO_AGUA:
            self.__saude -= 15
            self.__felicidade -= 10
        
        return (comida_consumida, agua_consumida)
    
    def receber_cuidados_medicos(self):
        """Colono recebe cuidados médicos e recupera saúde."""
        if self.esta_vivo:
            self.__saude = min(100, self.__saude + 20)
            self.__felicidade = min(100, self.__felicidade + 5)
    
    def atualizar(self):
        """
        Implementação do método abstrato da classe base.
        Demonstra polimorfismo.
        """
        if not self.esta_vivo:
            return
        
        # Degradação natural leve
        if random.random() < 0.1:  # 10% de chance
            self.__felicidade = max(0, self.__felicidade - 1)
    
    def to_dict(self) -> dict:
        """Converte o colono para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'profissao': self.__profissao,
            'saude': self.__saude,
            'felicidade': self.__felicidade,
            'produtividade': round(self.__produtividade, 2),
            'dias_trabalhados': self.__dias_trabalhados,
            'esta_vivo': self.esta_vivo
        }
    
    def __str__(self) -> str:
        """Representação em string do colono."""
        status = "Vivo" if self.esta_vivo else "Morto"
        return f"{self.nome} ({self.__profissao}) - Saúde: {self.__saude}, Felicidade: {self.__felicidade} - {status}"

