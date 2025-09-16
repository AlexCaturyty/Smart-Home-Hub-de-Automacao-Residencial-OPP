import argparse  
from smart_home.core.hub import Hub  
from smart_home.core.observers import ConsoleObserver, FileObserver  
from smart_home.dispositivos.tomada import Smartplug  
from smart_home.dispositivos.porta import Port 
from smart_home.dispositivos.ar_condicionado import AirConditioner  
from smart_home.dispositivos.geladeira import Freeze  
from smart_home.dispositivos.luz import Ligth  
from smart_home.dispositivos.umidificador import Humidifier 

from smart_home.core.erros import TransicaoInvalida




def main(args):
    hub = Hub("Casa Exemplo")
    # Adiciona observadores para registrar eventos no console e em arquivo
    hub.registrar_observer(ConsoleObserver())
    hub.registrar_observer(FileObserver("data/eventos.txt"))

    # Se o usuário passar --config, carrega as configurações do arquivo JSON
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

        # Opção 1: lista todos os dispositivos cadastrados
        if opcao == "1":
            hub.listar_dispositivos()

        # Opção 2: mostra o status de um dispositivo específico
        elif opcao == "2":
            id_ = input("ID do dispositivo: ").strip()
            disp = hub.dispositivos.get(id_)
            if disp:
                print(disp.status())
            else:
                print(">> Dispositivo não encontrado.")

        # Opção 3: executa um comando em um dispositivo
        elif opcao == "3":
            id_ = input("ID do dispositivo: ").strip()
            disp = hub.dispositivos.get(id_)
            if not disp:
                print(">> Dispositivo não encontrado.")
                continue

            # Mostra comandos disponíveis se tiver máquina de estados
            if hasattr(disp, "machine"):
                comandos = sorted(disp.machine.events.keys())
                print(f"Comandos disponíveis para {disp.nome} ({disp.tipo.value}): {', '.join(comandos)}")

            comando = input("Comando: ").strip()

            # Dicionário de sugestões de argumento por dispositivo e trigger
            dicas = {
                AirConditioner: {
                    "ajustar_temperatura": "16-30",
                    "mudar_modo": "FRIO ou QUENTE"
                },
                Freeze: {
                    "ajustar_temperatura": "0-10",
                    "mudar_modo": "ECO ou TURBO"
                },
                Ligth: {
                    "definir_brilho": "0-100",
                    "definir_cor": "QUENTE, FRIA ou NEUTRA"
                },
                Smartplug: {
                    "ligar": "nenhum argumento necessário",
                    "desligar": "nenhum argumento necessário"
                },
                Port: {
                    "abrir": "nenhum argumento necessário",
                    "fechar": "nenhum argumento necessário",
                    "trancar": "nenhum argumento necessário",
                    "destrancar": "nenhum argumento necessário"
                },
                Humidifier: {
                    "ajustar_intensidade": "0-100",
                    "reabastecer": "0-100"
                }
            }

            # Mostra dica se existir
            for cls, triggers in dicas.items():
                if isinstance(disp, cls) and comando in triggers:
                    print(f">> Sugestão de argumento para '{comando}': {triggers[comando]}")
                    break

            args_input = input("Argumentos (apenas valor único) ou ENTER: ").strip()
            kwargs = {}
            args_list = []

            if args_input:
                for par in args_input.split():
                    if "=" in par:
                        k, v = par.split("=")
                        kwargs[k] = v
                    else:
                        args_list.append(par)

            try:
                hub.executar_comando(id_, comando, *args_list, **kwargs)
            except TransicaoInvalida as e:
                print(f">> Atenção: {e}")
            except Exception as e:
                print(f">> Erro inesperado: {e}")


        # Opção 4: altera o valor de um atributo de um dispositivo
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

        # Opção 5: executa uma rotina pré-definida
        elif opcao == "5":
            print("Rotinas disponíveis:", ", ".join(hub.rotinas.keys()))
            nome_rotina = input("Nome da rotina a executar: ").strip()
            hub.executar_rotina(nome_rotina)

        # Opção 6: gera relatório dos dispositivos
        elif opcao == "6":
            print(">> Gerar relatório")
            print("Tipos disponíveis: consumo, comandos, ar_semana, tempo_luz, mais_usados")
            tipo = input("Tipo: ").strip().lower()
            arquivo = input("Nome do arquivo CSV (padrão: relatorio.csv): ").strip()
            if not arquivo:
                arquivo = "relatorio.csv"
            if not arquivo.startswith("data/"):
                arquivo = "data/" + arquivo
            hub.gerar_relatorio(arquivo=arquivo, tipo=tipo)

        # Opção 7: salva a configuração atual em arquivo JSON
        elif opcao == "7":
            arquivo = input("Nome do arquivo para salvar (ex: config.json): ").strip()
            if not arquivo:
                arquivo = "config.json"
            hub.salvar_config(arquivo)

        # Opção 8: adiciona um novo dispositivo ao Hub
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

        # Opção 9: remove um dispositivo do Hub
        elif opcao == "9":
            id_ = input("ID do dispositivo: ").strip()
            if id_ in hub.dispositivos:
                hub.dispositivos.pop(id_)
                print(">> Dispositivo removido.")
            else:
                print(">> Dispositivo não encontrado.")

        # Opção 10: encerra o programa
        elif opcao == "10":
            print(">> Atenção: você precisa salvar antes de sair para não perder as alterações!")
            salvar = input("Deseja salvar agora? (s/n): ").strip().lower()

            if salvar == "s":
                arquivo_padrao = "config.json"
                while True:
                    arquivo = input(f"Nome do arquivo para salvar (pressione ENTER para '{arquivo_padrao}'): ").strip()
                    if not arquivo:
                        arquivo = arquivo_padrao
                    if arquivo.endswith(".json"):
                        hub.salvar_config(arquivo)
                        break
                    else:
                        print(">> Nome inválido! O arquivo precisa terminar com '.json'.")

            print(">> Saindo...")
            break

        # Opção inválida: qualquer outra entrada
        else:
            print(">> Opção inválida.")

# Ponto de entrada do programa
if __name__ == "__main__":
     # Lê os argumentos passados no terminal (args.config acessa o valor)
    main()  # Executa o programa principal, passando os argumentos lidos


