class TransicaoInvalida(Exception):
    """Exceção lançada quando um comando não pode ser executado no estado atual do dispositivo."""
    def __init__(self, dispositivo_id, comando, estado):
        self.dispositivo_id = dispositivo_id
        self.comando = comando
        self.estado = estado
        super().__init__(f"Comando '{comando}' inválido para o dispositivo '{dispositivo_id}' no estado '{estado}'.")


class ConfigInvalida(Exception):
    """Exceção lançada quando o arquivo de configuração JSON é inválido ou está corrompido."""
    def __init__(self, arquivo, mensagem="Configuração inválida ou corrompida"):
        self.arquivo = arquivo
        self.mensagem = mensagem
        super().__init__(f"{mensagem}: {arquivo}")


class ValidacaoAtributo(Exception):
    """Exceção lançada quando um valor de atributo não é válido."""
    def __init__(self, dispositivo_id, atributo, valor, mensagem="Valor inválido para o atributo"):
        self.dispositivo_id = dispositivo_id
        self.atributo = atributo
        self.valor = valor
        self.mensagem = mensagem
        super().__init__(f"{mensagem} '{atributo}' do dispositivo '{dispositivo_id}': {valor}")
