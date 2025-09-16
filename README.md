# Smart Home Hub (Hub de Automação Residencial)

Este projeto é um sistema de automação residencial em Python chamado **Smart Home Hub**. Ele gerencia dispositivos inteligentes (luzes, portas, tomadas, alarmes, TVs, ar-condicionado, etc.) via **CLI** e aplica conceitos de POO, padrões de projeto, FSM (`transitions`), descritores, exceções, I/O (JSON/CSV) e programação funcional.

---

## 📋 Funcionalidades

* **Gerenciamento de dispositivos**: adicionar, remover, listar, consultar status.
* **FSM** (`transitions==0.9.1`): cada dispositivo tem sua máquina de estados.
* **Consumo elétrico realista** em tomada (`Wh`), acumulado enquanto está ligada.
* **Rotinas automáticas**: execução de comandos encadeados (ex.: "modo_frio").
* **Relatórios automáticos** em CSV:
  - Consumo por tomada.
  - Quantidade de comandos por tipo.
  - Quantidade de vezes que o ar-condicionado foi ligado na semana.
  - Quantos tempo a luz permaneceu ligada após desligar.
  - Quais dispositivos foram os mais usados
* **Persistência**:
  - Configuração em JSON.
  - Logs de eventos em CSV.
* **Padrões aplicados**:
  - `Observer`: hub notifica logger/console.
  - `Singleton`: logger CSV único.
  - `Descritores/propriedades`: validações (brilho 0–100, potência ≥ 0).
  - `ABC` e herança para dispositivos.

## 📂 Estrutura do Projeto

---

## Estrutura do projeto

```
smart_home/
├── data/
│   ├── configuracao.json
│   └── eventos.csv
├── smart_home/
│   ├── __init__.py
│   ├── core/
│   │   ├── cli.py
│   │   ├── hub.py
│   │   ├── dispositivos.py
│   │   ├── persistencia.py
│   │   ├── logger.py
│   │   ├── observers.py
│   │   ├── relatorios.py
│   │   └── erros.py
│   ├── dispositivos/
│   │   ├── luz.py
│   │   ├── porta.py
│   │   ├── tomada.py
│   │   ├── geladeira.py
│   │   └── ...
│   └── main.py
├── README.md
└── requirements.txt
```


---

## 🛠️ Conceitos e tecnologias aplicadas
- **OOP:** classes abstratas (`Dispositivo`), herança, polimorfismo e encapsulamento.  
- **Descritores/propriedades:** validações (ex.: `brilho` 0–100, `potencia_w` ≥ 0).  
- **FSM:** `transitions` para garantir transições válidas.  
- **Padrões:** `Singleton` (logger CSV), `Observer` (console e arquivo).  
- **I/O:** JSON para configuração/estado; CSV para logs e relatórios.  
- **Programação funcional:** `map`, `filter`, `reduce`, comprehensions para relatórios.  

---

## 🔧 Instalação

Requisitos: **Python 3.10+**

1. Clone o repositório:
```bash
git clone https://github.com/AlexCaturyty/Smart-Home-Hub-de-Automacao-Residencial-OPP.git
cd Smart-Home-Hub-de-Automacao-Residencial-OPP
```
---

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Como executar

Executar o ponto de entrada (CLI):

```bash
python -m smart_home.main
```

Você pode passar um arquivo de configuração customizado:

```bash
python -m smart_home.main --config data/configuracao.json
```

Ao iniciar, o Hub carrega a `configuracao.json` (se existir) e o `eventos.csv` é usado como log (ou criado quando houver o primeiro evento). Ao sair, a configuração atual é salva.

---

## Guia rápido da CLI

Menu principal (sem acentos para facilitar):
```
=== SMART HOME HUB ===
1. Listar dispositivos
2. Mostrar dispositivo
3. Executar comando em dispositivo
4. Alterar atributo de dispositivo
5. Executar rotina
6. Gerar relatorio
7. Salvar configuracao
8. Adicionar dispositivo
9. Remover dispositivo
10. Sair
```

Fluxos típicos:

* **Adicionar dispositivo (8):**

  * Informe tipo (`PORTA`, `LUZ`, `TOMADA`, `FREEZER`, `UMIDIFICADOR`, etc.), id, nome e atributos (ex.: brilho, cor, potencia\_w).
  * Evento de `DispositivoAdicionado` é emitido.

* **Executar comando (3):**

  * Informe `id` do dispositivo e o `comando` (ex.: `ligar`, `desligar`, `reabastecer`, `definir_brilho`).

* **Executar rotina (5):**

  * Escolha uma rotina configurada no JSON (`modo_frio`, `acordar`, ...).
  * O Hub aplica cada ação na sequência e registra eventos.

* **Gerar relatório (6):**

  * Escolha tipo de relatório (ex.: consumo por tomada, tempo que cada luz ficou ligada, dispositivos mais usados).
  * Opções adicionais podem pedir período (data inicial/final).

  

---

## Formato dos arquivos

### `configuracao.json` (exemplo)

```json
{
  "hub": {
    "nome": "Minha Casa",
    "versao": "1.0"
  },
  "dispositivos": [
    {
      "id": "ar_quarto_id",
      "tipo": "ARCONDICIONADO",
      "nome": "condicionado",
      "estado": "OFF",
      "atributos": {
        "_temperature": 20,
        "temperature": 20
      }
    },
    {
      "id": "porta_id",
      "tipo": "PORTA",
      "nome": "porta_entrada",
      "estado": "LOCKED",
      "atributos": {
        "_invalid_attempts": 2,
        "invalid_attempts": 0
      }
    },
    {
      "id": "geladeira_id",
      "tipo": "GELADEIRA",
      "nome": "freze",
      "estado": "OFF",
      "atributos": {
        "_temperature": 6
      }
    },
    {
      "id": "umidicador_id",
      "tipo": "UMIDIFICADOR",
      "nome": "umidifi",
      "estado": "OFF",
      "atributos": {
        "_intensity": 5,
        "_water_level": 100
      }
    },
    {
      "id": "tomada_id",
      "tipo": "TOMADA",
      "nome": "toma",
      "estado": "OFF",
      "atributos": {
        "_potencia_w": 400,
        "_consumption_wh": 15.140979388888889
      }
    },
    {
      "id": "luz_id",
      "tipo": "LUZ",
      "nome": "luiz",
      "estado": "OFF",
      "atributos": {
        "_brightness": 100,
        "_pending_brightness": null,
        "_pending_color": null
      }
    }
  ],
  "rotinas": {
    "modo_frio": [
      {
        "id": "umidicador_id",
        "comando": "ligar"
      },
      {
        "id": "ar_quarto_id",
        "comando": "ligar",
        "argumentos": {
          "temperatura": 16
        }
      },
      {
        "id": "luz_id",
        "comando": "desligar"
      }
    ],
    "acordar": [
      {
        "id": "luz_sala",
        "comando": "ligar"
      },
      {
        "id": "umidificador",
        "comando": "ligar"
      },
      {
        "id": "ar_quarto",
        "comando": "desligar"
      }
    ]
  }
}
```

### `eventos.csv` (exemplo)

Cabeçalho:

```
timestamp,id_dispositivo,nome_dispositivo,tipo_dispositivo,evento,estado,potencia_w,consumo_wh
```

Exemplo de linhas:

```
2025-09-15T20:02:41.093681,luz_id,luiz,LUZ,ligar,luz_id | luz | Luz | Estado: ON | Brilho: 100% | Cor: neutra,,0
2025-09-15T20:06:09.505690,umidificador_id,umidifi,UMIDIFICADOR,ligar,umidificador_id | umidifi | Umidificador | Estado: ON | �gua: 50% | Intensidade: 5%,,0
2025-09-15T20:06:18.616623,umidificador_id,umidifi,UMIDIFICADOR,reabastecer,umidificador_id | umidifi | Umidificador | Estado: ON | �gua: 100% | Intensidade: 5%,,0
```

### Relatórios CSV

Formato depende do relatório; ex. consumo por tomada:

```
id_dispositivo,total_wh,inicio_periodo,fim_periodo
tomada_tv,240,2025-09-01T00:00:00,2025-09-01T23:59:59
```

---

## Autor

Alex Cavalcanti

---