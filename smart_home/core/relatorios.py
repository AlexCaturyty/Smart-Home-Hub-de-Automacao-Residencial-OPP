import csv
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from functools import reduce

class Relatorios:
    def __init__(self, arquivo="data/eventos.csv"):
        self.arquivo = arquivo

    def _ler_eventos(self):
        with open(self.arquivo, newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    # ---------------- Relatórios ----------------
    # 1. Consumo por tomada inteligente
    def consumo_por_tomada(self, arquivo_saida="relatorio_consumo.csv"):
        eventos = self._ler_eventos()
        tomadas = [e for e in eventos if e["tipo_dispositivo"].lower() == "tomada"]

        # Usa reduce para somar o consumo de cada dispositivo
        def soma_consumo(acumulador, evento):
            id_ = evento["id_dispositivo"]
            wh = float(evento.get("consumo_wh", 0) or 0)
            acumulador[id_] = acumulador.get(id_, 0) + wh
            return acumulador

        consumo_por_disp = reduce(soma_consumo, tomadas, {}) # < ------------

        with open(arquivo_saida, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_dispositivo", "nome_dispositivo", "total_wh"])
            for id_, total in consumo_por_disp.items():
                nome = next((t["nome_dispositivo"] for t in tomadas if t["id_dispositivo"] == id_), "")
                writer.writerow([id_, nome, round(total, 2)])

        print(f">> Relatório de consumo por tomada salvo em {arquivo_saida}")


    # 2. Tempo total em que cada luz permaneceu ligada
    def tempo_luz_ligada(self, arquivo_saida="relatorio_tempo_luz.csv"):
        eventos = self._ler_eventos()
        luzes = set(e["id_dispositivo"] for e in eventos if e["tipo_dispositivo"].lower() == "luz")

        resultado = {}
        for luz in luzes:
            eventos_luz = [e for e in eventos if e["id_dispositivo"] == luz]
            eventos_luz.sort(key=lambda x: x["timestamp"])
            tempo_total = 0
            ultimo_ligar = None

            for e in eventos_luz:
                if e["evento"] == "ligar":
                    ultimo_ligar = datetime.fromisoformat(e["timestamp"])
                elif e["evento"] == "desligar" and ultimo_ligar:
                    ts = datetime.fromisoformat(e["timestamp"])
                    tempo_total += (ts - ultimo_ligar).total_seconds() / 60  
                    ultimo_ligar = None

            resultado[luz] = round(tempo_total, 2)

        with open(arquivo_saida, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_dispositivo", "nome_dispositivo", "tempo_ligado_min"])
            for id_, tempo in resultado.items():
                nome = next((e["nome_dispositivo"] for e in eventos if e["id_dispositivo"] == id_), "")
                writer.writerow([id_, nome, tempo])

        print(f">> Relatório de tempo de luz ligada salvo em {arquivo_saida}")

    # 3. Ar-condicionado ligado na semana
    def ar_condicionado_ligado_semana(self, arquivo_saida="relatorio_ar_semana.csv"):
        eventos = self._ler_eventos()
        hoje = datetime.now()
        sete_dias = hoje - timedelta(days=7)

        ar_eventos = filter(lambda e: "ar" in e["id_dispositivo"].lower() and e["evento"] == "ligar", eventos) # < --------------
        contagem = {}
        for e in ar_eventos:
            ts = datetime.fromisoformat(e["timestamp"])
            if ts >= sete_dias:
                contagem[e["id_dispositivo"]] = contagem.get(e["id_dispositivo"], 0) + 1

        with open(arquivo_saida, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_dispositivo", "vezes_ligado_na_semana"])
            for id_, qtd in contagem.items():
                writer.writerow([id_, qtd])

        print(f">> Relatório de ar-condicionado ligado na semana salvo em {arquivo_saida}")


    # 4. Dispositivos mais usados
    def dispositivos_mais_usados(self, arquivo_saida="relatorio_mais_usados.csv"):
        eventos = self._ler_eventos()
        contagem = Counter(map(lambda e: e["id_dispositivo"], eventos)) # < --------------
        mais_usados = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

        with open(arquivo_saida, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id_dispositivo", "quantidade_eventos"])
            for id_, qtd in mais_usados:
                writer.writerow([id_, qtd])

        print(f">> Relatório de dispositivos mais usados salvo em {arquivo_saida}")


    def comandos_por_tipo(self, arquivo_saida="relatorio_comandos.csv"):
        eventos = self._ler_eventos()
        contagem = Counter([e["evento"] for e in eventos])

        with open(arquivo_saida, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["evento", "quantidade"])
            for ev, qtd in contagem.items():
                writer.writerow([ev, qtd])

        print(f">> Relatório de comandos salvo em {arquivo_saida}")

    