"""
Classe para gerenciar recursos da colônia.
Demonstra: Encapsulamento, Validação de Dados
"""


class Recurso:
    """
    Representa um recurso da colônia (comida, água, energia, metal).
    Demonstra encapsulamento com validação de dados.
    """
    
    def __init__(self, tipo: str, quantidade: float = 0, capacidade_maxima: float = 1000):
        """
        Inicializa um recurso.
        
        Args:
            tipo: Tipo do recurso (comida, agua, energia, metal)
            quantidade: Quantidade inicial
            capacidade_maxima: Capacidade máxima de armazenamento
        """
        self.__tipo = tipo
        self.__quantidade = max(0, quantidade)
        self.__capacidade_maxima = max(1, capacidade_maxima)
        
        # Garante que quantidade não exceda capacidade
        if self.__quantidade > self.__capacidade_maxima:
            self.__quantidade = self.__capacidade_maxima
    
    @property
    def tipo(self) -> str:
        """Retorna o tipo do recurso."""
        return self.__tipo
    
    @property
    def quantidade(self) -> float:
        """Retorna a quantidade atual do recurso."""
        return self.__quantidade
    
    @property
    def capacidade_maxima(self) -> float:
        """Retorna a capacidade máxima de armazenamento."""
        return self.__capacidade_maxima
    
    @capacidade_maxima.setter
    def capacidade_maxima(self, valor: float):
        """Define a capacidade máxima com validação."""
        if valor < 1:
            raise ValueError("Capacidade máxima deve ser maior que 0")
        self.__capacidade_maxima = valor
        # Ajusta quantidade se exceder nova capacidade
        if self.__quantidade > self.__capacidade_maxima:
            self.__quantidade = self.__capacidade_maxima
    
    def adicionar(self, valor: float) -> float:
        """
        Adiciona recurso respeitando a capacidade máxima.
        
        Args:
            valor: Quantidade a adicionar
            
        Returns:
            Quantidade realmente adicionada
        """
        if valor <= 0:
            return 0
        
        quantidade_anterior = self.__quantidade
        self.__quantidade = min(self.__quantidade + valor, self.__capacidade_maxima)
        return self.__quantidade - quantidade_anterior
    
    def remover(self, valor: float) -> bool:
        """
        Remove recurso se houver quantidade suficiente.
        
        Args:
            valor: Quantidade a remover
            
        Returns:
            True se conseguiu remover, False caso contrário
        """
        if valor <= 0:
            return True
        
        if self.__quantidade >= valor:
            self.__quantidade -= valor
            return True
        return False
    
    def esta_disponivel(self, valor: float) -> bool:
        """
        Verifica se há quantidade suficiente disponível.
        
        Args:
            valor: Quantidade a verificar
            
        Returns:
            True se há quantidade suficiente, False caso contrário
        """
        return self.__quantidade >= valor
    
    def percentual(self) -> float:
        """
        Retorna o percentual de preenchimento do recurso.
        
        Returns:
            Percentual de 0 a 100
        """
        return (self.__quantidade / self.__capacidade_maxima) * 100
    
    def to_dict(self) -> dict:
        """Converte o recurso para dicionário."""
        return {
            'tipo': self.__tipo,
            'quantidade': round(self.__quantidade, 2),
            'capacidade_maxima': self.__capacidade_maxima,
            'percentual': round(self.percentual(), 1)
        }
    
    def __str__(self) -> str:
        """Representação em string do recurso."""
        return f"{self.__tipo.capitalize()}: {self.__quantidade:.1f}/{self.__capacidade_maxima}"
    
    def __repr__(self) -> str:
        """Representação técnica do recurso."""
        return f"Recurso(tipo='{self.__tipo}', quantidade={self.__quantidade}, capacidade={self.__capacidade_maxima})"

