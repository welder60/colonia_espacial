"""
Classe base abstrata para todas as entidades do jogo.
Demonstra: Abstração, Encapsulamento
"""
from abc import ABC, abstractmethod
import uuid


class Entidade(ABC):
    """
    Classe abstrata base para todas as entidades do jogo.
    Demonstra o conceito de abstração em POO.
    """
    
    def __init__(self, nome: str, descricao: str):
        """
        Inicializa uma entidade com atributos privados.
        Demonstra encapsulamento.
        
        Args:
            nome: Nome da entidade
            descricao: Descrição da entidade
        """
        self.__id = str(uuid.uuid4())  # Atributo privado
        self.__nome = nome
        self.__descricao = descricao
    
    # Getters (encapsulamento)
    @property
    def id(self) -> str:
        """Retorna o ID único da entidade."""
        return self.__id
    
    @property
    def nome(self) -> str:
        """Retorna o nome da entidade."""
        return self.__nome
    
    @property
    def descricao(self) -> str:
        """Retorna a descrição da entidade."""
        return self.__descricao
    
    # Setters (encapsulamento com validação)
    @nome.setter
    def nome(self, valor: str):
        """Define o nome da entidade com validação."""
        if not valor or len(valor.strip()) == 0:
            raise ValueError("Nome não pode ser vazio")
        self.__nome = valor.strip()
    
    @descricao.setter
    def descricao(self, valor: str):
        """Define a descrição da entidade."""
        self.__descricao = valor
    
    @abstractmethod
    def atualizar(self):
        """
        Método abstrato para atualizar o estado da entidade.
        Deve ser implementado pelas subclasses (polimorfismo).
        """
        pass
    
    def __str__(self) -> str:
        """Representação em string da entidade."""
        return f"{self.__class__.__name__}(nome='{self.__nome}')"
    
    def __repr__(self) -> str:
        """Representação técnica da entidade."""
        return f"{self.__class__.__name__}(id='{self.__id}', nome='{self.__nome}')"

