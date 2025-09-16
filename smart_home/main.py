import argparse
from smart_home.core.cli import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # Cria um parser para ler argumentos do terminal
    parser.add_argument("--config", help="Arquivo JSON de configuração", default=None) # Define o argumento opcional --config (ex: python app.py --config data/config.json)
    args = parser.parse_args()
    main(args)  # Executa o programa principal, passando os argumentos lidos
