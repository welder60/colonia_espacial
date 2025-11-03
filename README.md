# 🚀 Jogo de Gerenciamento de Colônia Espacial

**Projeto de Orientação a Objetos - Universidade de Brasília (UnB)**

## 📋 Descrição

Jogo web de gerenciamento de colônia espacial desenvolvido em Python, demonstrando todos os conceitos fundamentais de Programação Orientada a Objetos (POO), implementando o padrão arquitetural MVC (Model-View-Controller) e utilizando persistência de dados com Pickle.

## 🎯 Objetivos do Projeto

Este projeto foi desenvolvido para demonstrar de forma prática e completa os seguintes conceitos:

### Conceitos de POO Implementados

1. **Encapsulamento**
   - Atributos privados (prefixo `__`)
   - Properties (getters/setters)
   - Validação de dados nos setters
   - Exemplo: Classes `Recurso`, `Colono`, `Edificio`

2. **Herança**
   - Classe base abstrata `Entidade`
   - Subclasses: `Colono`, `Edificio`
   - Classe base `Edificio` com subclasses específicas: `Fazenda`, `Purificador`, `GeradorEnergia`, `Mina`, `Habitacao`, `Hospital`

3. **Polimorfismo**
   - Método abstrato `atualizar()` implementado diferentemente em cada subclasse
   - Método `produzir()` com comportamentos específicos para cada tipo de edifício
   - Sobrescrita de métodos `__str__()` e `__repr__()`

4. **Abstração**
   - Uso de classes abstratas (`ABC` do módulo `abc`)
   - Métodos abstratos (`@abstractmethod`)
   - Interface comum para diferentes tipos de entidades

5. **Composição**
   - Classe `Colonia` contém objetos de `Colono`, `Edificio`, `Recurso`
   - Relacionamento forte entre objetos
   - Ciclo de vida gerenciado pela classe container

6. **Agregação e Associação**
   - Relacionamentos entre classes
   - Dependências entre objetos
   - Eventos que afetam a colônia

## 🏗️ Arquitetura MVC

### Model (Modelo)
Localização: `/models/`

- **`entidade.py`**: Classe abstrata base para todas as entidades
- **`recurso.py`**: Gerenciamento de recursos (comida, água, energia, metal)
- **`colono.py`**: Representa os habitantes da colônia
- **`edificio.py`**: Classes de edifícios e suas especializações
- **`evento.py`**: Eventos aleatórios que afetam o jogo
- **`colonia.py`**: Classe principal que orquestra todo o jogo

### View (Visão)
Localização: `/views/`

- **`index.html`**: Página inicial com menu
- **`jogo.html`**: Interface principal do jogo
- **`/static/style.css`**: Estilização da interface

### Controller (Controlador)
Localização: `app.py`

- Rotas HTTP usando Bottle
- Processamento de requisições
- Integração entre Model e View
- Lógica de controle de fluxo

## 💾 Persistência com Pickle

- **Arquivo**: `saves/colonia_save.pkl`
- **Funcionalidade**: Serialização completa do objeto `Colonia`
- **Salvamento**: Automático a cada turno
- **Carregamento**: Ao iniciar o jogo

## 🎮 Mecânicas do Jogo

### Recursos
- **🌾 Comida**: Consumida pelos colonos (5 por colono/turno)
- **💧 Água**: Consumida pelos colonos (3 por colono/turno)
- **⚡ Energia**: Necessária para funcionamento dos edifícios
- **🔩 Metal**: Usado para construção de edifícios

### Edifícios
- **Fazenda**: Produz comida
- **Purificador de Água**: Produz água
- **Gerador de Energia**: Produz energia
- **Mina**: Extrai metal
- **Habitação**: Abriga colonos e aumenta felicidade
- **Hospital**: Cuida da saúde dos colonos

### Colonos
- **Profissões**: Agricultor, Engenheiro, Cientista, Minerador, Médico
- **Atributos**: Saúde, Felicidade, Produtividade
- **Mecânicas**: Trabalho, descanso, consumo de recursos

### Eventos Aleatórios
- Tempestade Solar
- Descoberta de Recursos
- Colheita Abundante
- Contaminação de Água
- Moral Alta
- Epidemia
- Novo Colono
- Avanço Tecnológico

### Condições de Vitória/Derrota
- **Vitória**: 20+ colonos com felicidade média > 70%
- **Derrota**: Todos os colonos morrem

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- Bottle framework

### Instalação

```bash
# Clone ou extraia o projeto
cd colony_game

# Instale as dependências
pip3 install bottle

# Execute o servidor
python3 app.py
```

### Acesso
Abra o navegador em: `http://localhost:8080`

## 📁 Estrutura de Diretórios

```
colony_game/
├── app.py                 # Controlador principal (MVC)
├── models/                # Modelos (MVC)
│   ├── __init__.py
│   ├── entidade.py       # Classe abstrata base
│   ├── colono.py         # Classe Colono
│   ├── edificio.py       # Classes de edifícios
│   ├── recurso.py        # Classe Recurso
│   ├── evento.py         # Classe EventoAleatorio
│   └── colonia.py        # Classe principal Colonia
├── views/                 # Views (MVC)
│   ├── index.html        # Página inicial
│   └── jogo.html         # Interface do jogo
├── static/                # Arquivos estáticos
│   └── style.css         # Estilos CSS
├── saves/                 # Salvamentos (Pickle)
│   └── colonia_save.pkl  # Arquivo de save
└── README.md             # Este arquivo
```

## 🎓 Conceitos Acadêmicos Demonstrados

### Classes e Objetos
- Definição de classes com atributos e métodos
- Instanciação de objetos
- Construtores (`__init__`)

### Modificadores de Acesso
- Atributos privados (`__atributo`)
- Atributos protegidos (`_atributo`)
- Atributos públicos

### Properties
- Decoradores `@property`
- Getters e setters
- Validação de dados

### Métodos Especiais
- `__str__()`: Representação em string
- `__repr__()`: Representação técnica
- `__init__()`: Construtor

### Herança Múltipla de Conceitos
- Herança simples
- Método `super()`
- Sobrescrita de métodos

### Classes Abstratas
- Módulo `abc`
- Decorador `@abstractmethod`
- Imposição de implementação

### Composição vs Herança
- "Tem-um" vs "É-um"
- Agregação de objetos
- Ciclo de vida de objetos

## 🔧 Tecnologias Utilizadas

- **Linguagem**: Python 3.11
- **Framework Web**: Bottle 0.13
- **Persistência**: Pickle (módulo padrão)
- **Frontend**: HTML5, CSS3
- **Paradigma**: Orientação a Objetos
- **Padrão**: MVC (Model-View-Controller)

## 📊 Diagramas

- Diagrama UML de classes incluído no projeto
- Apresentação de slides explicativa

## 👨‍💻 Desenvolvimento

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de Orientação a Objetos da Universidade de Brasília (UnB), demonstrando de forma prática e completa todos os conceitos fundamentais de POO.

## 📝 Licença

Projeto acadêmico - UnB

---

**Universidade de Brasília (UnB)**  
**Disciplina**: Orientação a Objetos  
**Ano**: 2025

