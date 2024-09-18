from ..exeptions import MSpeechPyExeptions, NetworkError
import os
import json
from datetime import datetime, timezone, timedelta
from azure.identity import DeviceCodeCredential
from ..CONSTANTS import CONFIG_FILE


class AuthMicrosoft:
    """Classe para autenticação com a Microsoft Azure cognitiveservices"""

    TOKEN_REFRESH_THRESHOLD = 300  # Tempo limite (em segundos) para renovar o token

    def __init__(self):
        self.__token = None
        self.__timestamp = None
        self.__load_config()

    def __load_config(self):
        """Carrega o token e a data de expiração do arquivo de configuração, se existir."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as file:
                    config = json.load(file)
                    self.__token = config.get('token')
                    self.__timestamp = config.get('timestamp', 0)
            except (IOError, json.JSONDecodeError) as e:
                raise MSpeechPyExeptions(f"Erro ao carregar o arquivo de configuração: {e}")

    def __save_config(self):
        """Salva o token e a data de expiração no arquivo de configuração."""
        try:
            with open(CONFIG_FILE, 'w') as file:
                json.dump({
                    'token': self.__token,
                    'timestamp': self.__timestamp
                }, file)
        except IOError as e:
            raise MSpeechPyExeptions(f"Erro ao salvar o arquivo de configuração: {e}")

    def get_token_expiry_details(self):
        """
        Obtém o tempo restante até a expiração do token em minutos e segundos.

        Returns:
            dict: Um dicionário com o tempo restante em minutos e segundos.
        """
        if self.__timestamp is None:
            return {
                'valid': False,
                'minutes': 0,
                'seconds': 0
            }

        current_time = datetime.now(timezone.utc).timestamp()
        time_remaining = self.__timestamp - current_time

        if time_remaining < 0:
            return {
                'valid': False,
                'minutes': 0,
                'seconds': 0
            }

        minutes, seconds = divmod(time_remaining, 60)
        return {
            'valid': True,
            'minutes': int(minutes),
            'seconds': int(seconds)
        }

    def check_login(self):
        """
        Verifica se o usuário está logado, se o token é válido e se está prestes a expirar.
        Retorna True se o token estiver presente e for válido.
        """
        if self.__token is None:
            return False

        expiry_details = self.get_token_expiry_details()
        if not expiry_details['valid']:
            return False

        # Verificar se o token expira nos próximos 5 minutos (300 segundos)
        current_time = datetime.now(timezone.utc).timestamp()
        if (self.__timestamp - current_time) < self.TOKEN_REFRESH_THRESHOLD:
            # ("Token está próximo de expirar, renovando...")
            self.login()
            return True
        return True

    def login(self):
        """
        Realiza o login do usuário e salva o token e sua data de expiração se necessário.
        Também atualiza o token se ele estiver prestes a expirar.
        """
        if self.check_login():
            return self.__token
        try:
            credential = DeviceCodeCredential()
            aadToken = credential.get_token("https://cognitiveservices.azure.com/.default")

            self.__token = aadToken.token
            self.__timestamp = aadToken.expires_on
            self.__save_config()
        except Exception as e:
            raise NetworkError(f"Erro durante o login: {e}")
        return self.__token

    def load_section(self):
        """Retorna a seção do usuário com seu token."""
        while not self.check_login():
            self.login()
        return self.__token

