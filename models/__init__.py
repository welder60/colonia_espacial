"""
Pacote models - contém todas as classes do modelo do jogo.
Demonstra organização modular e encapsulamento de código.
"""
from models.entidade import Entidade
from models.recurso import Recurso
from models.colono import Colono
from models.edificio import (
    Edificio, Fazenda, Purificador, GeradorEnergia, 
    Mina, Habitacao, Hospital, TIPOS_EDIFICIOS
)
from models.evento import EventoAleatorio
from models.colonia import Colonia

__all__ = [
    'Entidade',
    'Recurso',
    'Colono',
    'Edificio',
    'Fazenda',
    'Purificador',
    'GeradorEnergia',
    'Mina',
    'Habitacao',
    'Hospital',
    'TIPOS_EDIFICIOS',
    'EventoAleatorio',
    'Colonia'
]

