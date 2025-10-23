"""
Classes de Edifícios da colônia.
Demonstra: Herança, Polimorfismo, Encapsulamento
"""
from models.entidade import Entidade
from abc import abstractmethod
import random


class Edificio(Entidade):
    """
    Classe base abstrata para todos os edifícios.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self, nome: str, descricao: str, custo_construcao: dict):
        """
        Inicializa um edifício.
        
        Args:
            nome: Nome do edifício
            descricao: Descrição do edifício
            custo_construcao: Dicionário com custos de recursos
        """
        super().__init__(nome, descricao)
        self.__nivel = 1
        self.__custo_construcao = custo_construcao
        self.__capacidade = 10
        self.__status = 'ativo'
        self.__producao_total = 0
    
    @property
    def nivel(self) -> int:
        """Retorna o nível do edifício."""
        return self.__nivel
    
    @property
    def custo_construcao(self) -> dict:
        """Retorna o custo de construção."""
        return self.__custo_construcao.copy()
    
    @property
    def capacidade(self) -> int:
        """Retorna a capacidade do edifício."""
        return self.__capacidade
    
    @property
    def status(self) -> str:
        """Retorna o status do edifício."""
        return self.__status
    
    @property
    def producao_total(self) -> float:
        """Retorna a produção total acumulada."""
        return self.__producao_total
    
    @status.setter
    def status(self, valor: str):
        """Define o status do edifício."""
        if valor not in ['ativo', 'inativo', 'manutencao']:
            raise ValueError("Status inválido")
        self.__status = valor
    
    def melhorar(self) -> dict:
        """
        Melhora o edifício para o próximo nível.
        
        Returns:
            Dicionário com o custo da melhoria
        """
        custo_melhoria = {
            recurso: valor * self.__nivel * 1.5
            for recurso, valor in self.__custo_construcao.items()
        }
        self.__nivel += 1
        self.__capacidade = int(self.__capacidade * 1.3)
        return custo_melhoria
    
    @abstractmethod
    def produzir(self, energia_disponivel: float) -> dict:
        """
        Método abstrato para produção de recursos.
        Deve ser implementado pelas subclasses.
        
        Args:
            energia_disponivel: Quantidade de energia disponível
            
        Returns:
            Dicionário com recursos produzidos
        """
        pass
    
    def atualizar(self):
        """Implementação do método abstrato da classe base."""
        if self.__status == 'manutencao':
            # Chance de voltar a funcionar
            if random.random() < 0.3:
                self.__status = 'ativo'
    
    def _calcular_producao_base(self, base: float, energia_disponivel: float, 
                                 consumo_energia: float) -> float:
        """
        Método protegido para calcular produção base.
        
        Args:
            base: Produção base
            energia_disponivel: Energia disponível
            consumo_energia: Energia necessária
            
        Returns:
            Produção calculada
        """
        if self.__status != 'ativo':
            return 0
        
        if energia_disponivel < consumo_energia:
            # Produção reduzida se não houver energia suficiente
            return base * self.__nivel * (energia_disponivel / consumo_energia) * 0.5
        
        producao = base * self.__nivel
        self.__producao_total += producao
        return producao
    
    def to_dict(self) -> dict:
        """Converte o edifício para dicionário."""
        return {
            'id': self.id,
            'tipo': self.__class__.__name__,
            'nome': self.nome,
            'nivel': self.__nivel,
            'capacidade': self.__capacidade,
            'status': self.__status,
            'producao_total': round(self.__producao_total, 2)
        }


class Fazenda(Edificio):
    """
    Fazenda - produz comida.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self):
        super().__init__(
            "Fazenda",
            "Produz comida para os colonos",
            {'metal': 20, 'energia': 10}
        )
    
    def produzir(self, energia_disponivel: float) -> dict:
        """
        Produz comida.
        Implementação polimórfica do método abstrato.
        """
        producao = self._calcular_producao_base(15, energia_disponivel, 5)
        return {
            'comida': producao,
            'energia_consumida': 5 if energia_disponivel >= 5 else energia_disponivel
        }


class Purificador(Edificio):
    """
    Purificador de Água - produz água potável.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self):
        super().__init__(
            "Purificador de Água",
            "Purifica e produz água potável",
            {'metal': 25, 'energia': 15}
        )
    
    def produzir(self, energia_disponivel: float) -> dict:
        """Produz água."""
        producao = self._calcular_producao_base(12, energia_disponivel, 8)
        return {
            'agua': producao,
            'energia_consumida': 8 if energia_disponivel >= 8 else energia_disponivel
        }


class GeradorEnergia(Edificio):
    """
    Gerador de Energia - produz energia.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self):
        super().__init__(
            "Gerador de Energia",
            "Gera energia para a colônia",
            {'metal': 40}
        )
    
    def produzir(self, energia_disponivel: float = 0) -> dict:
        """
        Produz energia (não consome energia).
        Implementação polimórfica.
        """
        if self.status != 'ativo':
            return {'energia': 0, 'energia_consumida': 0}
        
        producao = 30 * self.nivel
        return {
            'energia': producao,
            'energia_consumida': 0
        }


class Mina(Edificio):
    """
    Mina - extrai metal.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self):
        super().__init__(
            "Mina",
            "Extrai metal do solo",
            {'metal': 15, 'energia': 5}
        )
    
    def produzir(self, energia_disponivel: float) -> dict:
        """Produz metal."""
        producao = self._calcular_producao_base(8, energia_disponivel, 6)
        return {
            'metal': producao,
            'energia_consumida': 6 if energia_disponivel >= 6 else energia_disponivel
        }


class Habitacao(Edificio):
    """
    Habitação - abriga colonos.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self):
        super().__init__(
            "Habitação",
            "Fornece moradia para os colonos",
            {'metal': 30, 'energia': 5}
        )
        # Sobrescreve capacidade para representar número de colonos
        self._Edificio__capacidade = 5
    
    def produzir(self, energia_disponivel: float) -> dict:
        """
        Habitação não produz recursos, mas melhora felicidade.
        Implementação polimórfica.
        """
        if self.status == 'ativo' and energia_disponivel >= 3:
            return {
                'bonus_felicidade': 2 * self.nivel,
                'energia_consumida': 3
            }
        return {'bonus_felicidade': 0, 'energia_consumida': 0}


class Hospital(Edificio):
    """
    Hospital - cuida da saúde dos colonos.
    Demonstra herança e polimorfismo.
    """
    
    def __init__(self):
        super().__init__(
            "Hospital",
            "Cuida da saúde dos colonos",
            {'metal': 35, 'energia': 10}
        )
    
    def produzir(self, energia_disponivel: float) -> dict:
        """Hospital melhora a saúde dos colonos."""
        if self.status == 'ativo' and energia_disponivel >= 5:
            return {
                'bonus_saude': 3 * self.nivel,
                'energia_consumida': 5
            }
        return {'bonus_saude': 0, 'energia_consumida': 0}


# Dicionário para facilitar a criação de edifícios
TIPOS_EDIFICIOS = {
    'fazenda': Fazenda,
    'purificador': Purificador,
    'gerador': GeradorEnergia,
    'mina': Mina,
    'habitacao': Habitacao,
    'hospital': Hospital
}

