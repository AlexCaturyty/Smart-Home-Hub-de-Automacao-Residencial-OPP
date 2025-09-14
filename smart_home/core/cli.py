# smart_home/core/cli.py
import argparse
from smart_home.core.hub import Hub
from smart_home.core.observers import ConsoleObserver, FileObserver
from smart_home.dispositivos.tomada import Smartplug
from smart_home.dispositivos.porta import Port
from smart_home.dispositivos.ar_condicionado import AirConditioner
from smart_home.dispositivos.geladeira import Freeze
from smart_home.dispositivos.luz import Ligth
from smart_home.dispositivos.umidificador import Humidifier
from smart_home.core.dispositivos import TipoDispositivo

# python -m smart_home.core.cli --config data/config.json


def menu(args):
    hub = Hub("Casa Exemplo")
    hub.registrar_observer(ConsoleObserver())
    hub.registrar_observer(FileObserver("data/eventos.txt"))

    # Se passar --config, carrega as configurações do JSON no Hub
    if args.config:
        hub.carregar_config(args.config)


    while True:
        print("""
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
""")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            hub.listar_dispositivos()

        elif opcao == "2":
            id_ = input("ID do dispositivo: ").strip()
            disp = hub.dispositivos.get(id_)
            if disp:
                print(disp.status())
            else:
                print(">> Dispositivo não encontrado.")

        elif opcao == "3":
            id_ = input("ID do dispositivo: ").strip()
            comando = input("Comando: ").strip()
            args_input = input("Argumentos (k=v separados por espaço ou apenas valor único) ou ENTER: ").strip()
            kwargs = {}
            args_list = []

            if args_input:
                for par in args_input.split():
                    if "=" in par:
                        k, v = par.split("=")
                        kwargs[k] = v
                    else:
                        args_list.append(par)  
            hub.executar_comando(id_, comando, *args_list, **kwargs)


        elif opcao == "4":
            id_ = input("ID do dispositivo: ").strip()
            atributo = input("Nome do atributo: ").strip()
            valor = input("Novo valor: ").strip()
            disp = hub.dispositivos.get(id_)
            if disp and hasattr(disp, atributo):
                try:
                    if valor.isdigit():
                        valor = int(valor)
                    setattr(disp, atributo, valor)
                    print(">> Atributo atualizado!")
                except Exception as e:
                    print("!! Erro:", e)
            else:
                print(">> Dispositivo ou atributo não encontrado.")

        elif opcao == "5":
            print("Rotinas disponíveis:", ", ".join(hub.rotinas.keys()))
            nome_rotina = input("Nome da rotina a executar: ").strip()
            hub.executar_rotina(nome_rotina)


        elif opcao == "6":
            print(">> Gerar relatório")
            tipo_str = input("Filtrar por tipo (Tomada, Luz, Porta, ArCondicionado, Freeze, Umidificador) ou ENTER para todos: ").strip()
            tipo_enum = None
            if tipo_str:
                try:
                    tipo_enum = TipoDispositivo[tipo_str.upper()]
                except KeyError:
                    print(">> Tipo inválido, gerando relatório para todos.")
                    tipo_enum = None
            arquivo = input("Nome do arquivo CSV (padrão: relatorio.csv): ").strip()
            if not arquivo:
                arquivo = "relatorio.csv"
            hub.gerar_relatorio(arquivo=arquivo, tipo=tipo_enum)

        elif opcao == "7":
            arquivo = input("Nome do arquivo para salvar (ex: config.json): ").strip()
            if not arquivo:
                arquivo = "config.json"
            hub.salvar_config(arquivo)


        elif opcao == "8":
            print(">> Adicionar dispositivo")
            tipo = input("Tipo (Tomada, Porta, Luz, Freeze, Umidificador, ArCondicionado): ").strip()
            id_ = input("ID do dispositivo: ").strip()
            nome = input("Nome do dispositivo: ").strip()

            dispositivo = None
            if tipo.lower() == "tomada":
                potencia = int(input("Potência (W): ").strip())
               
                dispositivo = Smartplug(id_, nome, potencia_w=potencia)
            elif tipo.lower() == "porta":
                
                dispositivo = Port(id_, nome)
            elif tipo.lower() == "luz":
                dispositivo = Ligth(id_, nome)
                brilho = int(input("Brilho inicial (0-100): ").strip())
                dispositivo.brightness = brilho
            elif tipo.lower() == "freeze":
                dispositivo = Freeze(id_, nome)
            elif tipo.lower() == "umidificador":
                dispositivo = Humidifier(id_, nome)
            elif tipo.lower() == "arcondicionado":
                dispositivo = AirConditioner(id_, nome)
            else:
                print(">> Tipo inválido.")
            
            if dispositivo:
                hub.adicionar_dispositivo(dispositivo)
                print(f">> Dispositivo '{nome}' adicionado com sucesso!")


        elif opcao == "9":
            id_ = input("ID do dispositivo: ").strip()
            if id_ in hub.dispositivos:
                hub.dispositivos.pop(id_)
                print(">> Dispositivo removido.")
            else:
                print(">> Dispositivo não encontrado.")

        elif opcao == "10":
            print("saindo...")
            break

        else:
            print(">> Opção inválida.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # Cria um parser para ler argumentos do terminal
    parser.add_argument("--config", help="Arquivo JSON de configuração", default=None) # Define o argumento opcional --config (ex: python app.py --config data/config.json)
    args = parser.parse_args() # Lê os argumentos passados no terminal (args.config acessa o valor)
    menu(args)  # Executa o programa principal, passando os argumentos lidos


