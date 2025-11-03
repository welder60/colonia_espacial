"""
Classe principal Colonia - gerencia todo o estado do jogo.
Demonstra: Composição, Agregação, Associação
"""
from models.colono import Colono
from models.edificio import TIPOS_EDIFICIOS
from models.recurso import Recurso
from models.evento import EventoAleatorio
import random
import pickle
import os


class Colonia:
    """
    Classe principal que gerencia toda a colônia.
    Demonstra composição (contém objetos de outras classes) e agregação.
    """
    
    def __init__(self, nome: str):
        """
        Inicializa uma nova colônia.
        
        Args:
            nome: Nome da colônia
        """
        self.__nome = nome
        self.__dia = 1
        self.__colonos = []  # Composição - colônia contém colonos
        self.__edificios = []  # Composição - colônia contém edifícios
        self.__eventos_historico = []  # Lista de eventos ocorridos
        self._bonus_eficiencia = 1.0  # Bonus temporário de eficiência
        
        # Inicializa recursos (Composição)
        self.__recursos = {
            'comida': Recurso('comida', 50, 1000),
            'agua': Recurso('agua', 50, 1000),
            'energia': Recurso('energia', 100, 1000),
            'metal': Recurso('metal', 100, 500)
        }
        
        # Estatísticas
        self.__total_colonos_mortos = 0
        self.__total_edificios_construidos = 0
        
        # Inicializa com recursos básicos
        self._inicializar_colonia()
    
    def _inicializar_colonia(self):
        """Inicializa a colônia com recursos básicos."""
        # Adiciona 3 colonos iniciais
        for i in range(3):
            self.adicionar_colono(f"Colono {i+1}")
        
        # Constrói edifícios iniciais
        self.construir_edificio('gerador')
        self.construir_edificio('fazenda')
        self.construir_edificio('purificador')
    
    # Getters (Encapsulamento)
    @property
    def nome(self) -> str:
        """Retorna o nome da colônia."""
        return self.__nome
    
    @property
    def dia(self) -> int:
        """Retorna o dia atual."""
        return self.__dia
    
    @property
    def colonos(self) -> list:
        """Retorna lista de colonos (cópia para evitar modificação direta)."""
        return self.__colonos.copy()
    
    @property
    def edificios(self) -> list:
        """Retorna lista de edifícios."""
        return self.__edificios.copy()
    
    @property
    def recursos(self) -> dict:
        """Retorna dicionário de recursos."""
        return self.__recursos
    
    @property
    def eventos_historico(self) -> list:
        """Retorna histórico de eventos."""
        return self.__eventos_historico.copy()
    
    @property
    def total_colonos_vivos(self) -> int:
        """Retorna número de colonos vivos."""
        return sum(1 for c in self.__colonos if c.esta_vivo)
    
    @property
    def total_colonos_mortos(self) -> int:
        """Retorna número total de colonos mortos."""
        return self.__total_colonos_mortos
    
    @property
    def capacidade_habitacao(self) -> int:
        """Retorna capacidade total de habitação."""
        return sum(e.capacidade for e in self.__edificios 
                  if e.__class__.__name__ == 'Habitacao' and e.status == 'ativo')
    
    def adicionar_colono(self, nome: str = None):
        """
        Adiciona um novo colono à colônia.
        Demonstra composição.
        
        Args:
            nome: Nome do colono (gerado automaticamente se não fornecido)
        """
        if nome is None:
            nome = f"Colono {len(self.__colonos) + 1}"
        
        # Verifica capacidade de habitação
        if self.total_colonos_vivos >= self.capacidade_habitacao and self.capacidade_habitacao > 0:
            return False, "Capacidade de habitação atingida! Construa mais habitações."
        
        novo_colono = Colono(nome)
        self.__colonos.append(novo_colono)
        return True, f"{nome} se juntou à colônia!"
    
    def construir_edificio(self, tipo: str) -> tuple:
        """
        Constrói um novo edifício.
        Demonstra composição e validação de recursos.
        
        Args:
            tipo: Tipo do edifício a construir
            
        Returns:
            Tupla (sucesso: bool, mensagem: str)
        """
        if tipo not in TIPOS_EDIFICIOS:
            return False, f"Tipo de edifício inválido: {tipo}"
        
        # Cria instância do edifício
        classe_edificio = TIPOS_EDIFICIOS[tipo]
        novo_edificio = classe_edificio()
        
        # Verifica se há recursos suficientes
        custos = novo_edificio.custo_construcao
        for recurso, quantidade in custos.items():
            if not self.__recursos[recurso].esta_disponivel(quantidade):
                return False, f"Recursos insuficientes! Necessário: {custos}"
        
        # Consome recursos
        for recurso, quantidade in custos.items():
            self.__recursos[recurso].remover(quantidade)
        
        # Adiciona edifício
        self.__edificios.append(novo_edificio)
        self.__total_edificios_construidos += 1
        
        return True, f"{novo_edificio.nome} construído com sucesso!"
    
    def processar_turno(self) -> dict:
        """
        Processa um turno completo do jogo.
        Demonstra orquestração de múltiplos objetos (composição).
        
        Returns:
            Dicionário com informações do turno
        """
        relatorio = {
            'dia': self.__dia,
            'producao': {},
            'consumo': {},
            'evento': None,
            'alertas': []
        }
        
        # 1. PRODUÇÃO DE ENERGIA (primeiro, pois outros precisam)
        energia_produzida = 0
        for edificio in self.__edificios:
            if edificio.__class__.__name__ == 'GeradorEnergia':
                resultado = edificio.produzir()
                energia_produzida += resultado.get('energia', 0)
        
        self.__recursos['energia'].adicionar(energia_produzida)
        relatorio['producao']['energia'] = energia_produzida
        
        # 2. PRODUÇÃO DE RECURSOS (usando energia disponível)
        energia_disponivel = self.__recursos['energia'].quantidade
        
        for edificio in self.__edificios:
            if edificio.__class__.__name__ == 'GeradorEnergia':
                continue  # Já processado
            
            resultado = edificio.produzir(energia_disponivel)
            energia_consumida = resultado.get('energia_consumida', 0)
            energia_disponivel -= energia_consumida
            
            # Adiciona recursos produzidos
            for recurso, quantidade in resultado.items():
                if recurso in self.__recursos and quantidade > 0:
                    quantidade_bonus = quantidade * self._bonus_eficiencia
                    self.__recursos[recurso].adicionar(quantidade_bonus)
                    relatorio['producao'][recurso] = relatorio['producao'].get(recurso, 0) + quantidade_bonus
        
        # Reset bonus de eficiência
        self._bonus_eficiencia = 1.0
        
        # 3. TRABALHO DOS COLONOS
        for colono in self.__colonos:
            if colono.esta_vivo:
                colono.trabalhar()
        
        # 4. CONSUMO DE RECURSOS PELOS COLONOS
        consumo_total = {'comida': 0, 'agua': 0}
        colonos_vivos = [c for c in self.__colonos if c.esta_vivo]
        
        for colono in colonos_vivos:
            comida_disp = self.__recursos['comida'].quantidade
            agua_disp = self.__recursos['agua'].quantidade
            
            comida_cons, agua_cons = colono.consumir_recursos(comida_disp, agua_disp)
            
            self.__recursos['comida'].remover(comida_cons)
            self.__recursos['agua'].remover(agua_cons)
            
            consumo_total['comida'] += comida_cons
            consumo_total['agua'] += agua_cons
        
        relatorio['consumo'] = consumo_total
        
        # 5. BENEFÍCIOS DE EDIFÍCIOS ESPECIAIS
        for edificio in self.__edificios:
            if edificio.__class__.__name__ == 'Hospital':
                resultado = edificio.produzir(energia_disponivel)
                bonus_saude = resultado.get('bonus_saude', 0)
                if bonus_saude > 0:
                    for colono in colonos_vivos[:3]:  # Trata até 3 colonos
                        colono.receber_cuidados_medicos()
            
            elif edificio.__class__.__name__ == 'Habitacao':
                resultado = edificio.produzir(energia_disponivel)
                bonus_felicidade = resultado.get('bonus_felicidade', 0)
                if bonus_felicidade > 0:
                    for colono in colonos_vivos:
                        colono.felicidade = colono.felicidade + bonus_felicidade
        
        # 6. ATUALIZAÇÃO DE ENTIDADES
        for colono in self.__colonos:
            colono.atualizar()
        
        for edificio in self.__edificios:
            edificio.atualizar()
        
        # 7. VERIFICA MORTES
        mortes = sum(1 for c in self.__colonos if not c.esta_vivo)
        if mortes > self.__total_colonos_mortos:
            novos_mortos = mortes - self.__total_colonos_mortos
            self.__total_colonos_mortos = mortes
            relatorio['alertas'].append(f"⚠️ {novos_mortos} colono(s) morreram!")
        
        # 8. EVENTO ALEATÓRIO
        evento = EventoAleatorio.gerar_evento_aleatorio()
        if evento:
            mensagem_evento = evento.aplicar(self)
            self.__eventos_historico.append(evento)
            relatorio['evento'] = {
                'nome': evento.nome,
                'descricao': mensagem_evento
            }
        
        # 9. ALERTAS DE RECURSOS
        for nome, recurso in self.__recursos.items():
            if recurso.percentual() < 20:
                relatorio['alertas'].append(f"⚠️ {nome.capitalize()} está baixo!")
        
        # 10. AVANÇA DIA
        self.__dia += 1
        
        # Salva automaticamente
        self.salvar()
        
        return relatorio
    
    def verificar_condicoes(self) -> dict:
        """
        Verifica condições de vitória e derrota.
        
        Returns:
            Dicionário com status do jogo
        """
        colonos_vivos = self.total_colonos_vivos
        
        # Derrota: todos os colonos morreram
        if colonos_vivos == 0:
            return {
                'status': 'derrota',
                'mensagem': 'Todos os colonos morreram. A colônia foi perdida!'
            }
        
        # Vitória: 20+ colonos com felicidade média > 70
        if colonos_vivos >= 20:
            felicidade_media = sum(c.felicidade for c in self.__colonos if c.esta_vivo) / colonos_vivos
            if felicidade_media > 70:
                return {
                    'status': 'vitoria',
                    'mensagem': f'Vitória! A colônia prospera com {colonos_vivos} colonos felizes!'
                }
        
        return {'status': 'jogando', 'mensagem': ''}
    
    def obter_estatisticas(self) -> dict:
        """
        Retorna estatísticas completas da colônia.
        
        Returns:
            Dicionário com todas as estatísticas
        """
        colonos_vivos = [c for c in self.__colonos if c.esta_vivo]
        
        if colonos_vivos:
            saude_media = sum(c.saude for c in colonos_vivos) / len(colonos_vivos)
            felicidade_media = sum(c.felicidade for c in colonos_vivos) / len(colonos_vivos)
        else:
            saude_media = 0
            felicidade_media = 0
        
        return {
            'nome': self.__nome,
            'dia': self.__dia,
            'colonos_vivos': len(colonos_vivos),
            'colonos_mortos': self.__total_colonos_mortos,
            'saude_media': round(saude_media, 1),
            'felicidade_media': round(felicidade_media, 1),
            'total_edificios': len(self.__edificios),
            'capacidade_habitacao': self.capacidade_habitacao,
            'recursos': {nome: rec.to_dict() for nome, rec in self.__recursos.items()},
            'edificios': [e.to_dict() for e in self.__edificios],
            'colonos': [c.to_dict() for c in colonos_vivos],
            'eventos_recentes': [e.to_dict() for e in self.__eventos_historico[-5:]]
        }
    
    def salvar(self, caminho: str = None):
        """
        Salva o estado atual da colônia em um arquivo pickle.
        Demonstra persistência de dados.
        
        Args:
            caminho: Caminho do arquivo (usa padrão se não fornecido)
        """
        if caminho is None:
            caminho = 'saves/colonia_save.pkl'
        
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        with open(caminho, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def carregar(caminho: str = None) -> 'Colonia':
        """
        Carrega o estado da colônia do arquivo pickle.
        Demonstra persistência de dados.
        
        Args:
            caminho: Caminho do arquivo (usa padrão se não fornecido)
            
        Returns:
            Instância de Colonia carregada
        """
        if caminho is None:
            caminho = 'saves/colonia_save.pkl'
        
        if not os.path.exists(caminho):
            return None
        
        with open(caminho, 'rb') as f:
            return pickle.load(f)
    
    def __str__(self) -> str:
        """Representação em string da colônia."""
        return f"Colônia {self.__nome} - Dia {self.__dia} - {self.total_colonos_vivos} colonos vivos"

