import aiohttp
import requests
from rich.console import Console

from worker_automate_hub.api.helpers.api_helpers import handle_api_response
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import get_new_task_info, get_system_info

console = Console()


async def get_new_task():
    env_config, _ = load_env_config()
    try: 
        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}
        data = await get_new_task_info()

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(
                f"{env_config["API_BASE_URL"]}/robo/new-job",
                data=data,
                headers=headers_basic,
            ) as response:
                return await handle_api_response(response)

    except Exception as e:
        err_msg = f"Erro ao obter nova tarefa: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None

async def burnQueue(id_fila: str):
    env_config, _ = load_env_config()
    try:       

        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}
        

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.delete(
                f"{env_config["API_BASE_URL"]}/fila/burn-queue/{id_fila}",
                headers=headers_basic,
            ) as response:
                if response.status == 200:
                    logger.info("Fila excluida com sucesso.")
                    console.print("\nFila excluida com sucesso.\n", style="bold green")    
                else:
                    logger.error(f"Erro ao excluir a fila: {response.content}") 
                    console.print(f"Erro ao excluir a fila: {response.content}", style="bold red")          

    except Exception as e:
        err_msg = f"Erro remover registro da fila: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None
    
async def notify_is_alive():
    env_config, _ = load_env_config()
    try:       

        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}
        data = await get_system_info()

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.put(
                f"{env_config["API_BASE_URL"]}/robo/last-alive",
                data=data,
                headers=headers_basic,
            ) as response:
                return await handle_api_response(response, last_alive=True)

    except Exception as e:
        err_msg = f"Erro ao informar is alive: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None
    
async def get_processo(uuidProcesso: str):
    env_config, _ = load_env_config()
    try:      
        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}       
        

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                f"{env_config["API_BASE_URL"]}/processo/{uuidProcesso}",                
                headers=headers_basic,
            ) as response:
                return await response.json()

    except Exception as e:
        err_msg = f"Erro ao obter o processo: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None


async def get_workers():
    env_config, _ = load_env_config()
    try:
        

        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                f"{env_config["API_BASE_URL"]}/robo/workers",
                headers=headers_basic,
            ) as response:
                return await response.json()

    except Exception as e:
        err_msg = f"Erro ao obter a lista de workers: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None

async def get_config_by_name(name: str):
    env_config, _ = load_env_config()
    try:        

        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                f"{env_config["API_BASE_URL"]}/configuracao/{name}",
                headers=headers_basic,
            ) as response:
                return await response.json()

    except Exception as e:
        err_msg = f"Erro ao obter a configuração: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None
    
def sync_get_config_by_name(name: str):
    env_config, _ = load_env_config()
    
    try:
        headers_basic = {"Authorization": f"Basic {env_config['API_AUTHORIZATION']}"}

        response = requests.get(
            f"{env_config['API_BASE_URL']}/configuracao/{name}",
            headers=headers_basic,
            verify=False  # Desativa a verificação SSL
        )

        response.raise_for_status()
        
        return response.json()

    except requests.RequestException as e:
        err_msg = f"Erro ao obter a configuração: {e}"
        logger.error(err_msg)
        console.print(err_msg, style="red")
        return None
    
async def send_gchat_message(message: str):
    env_config, _ = load_env_config()
    try:       

        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}        

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.post(
                f"{env_config["API_BASE_URL"]}/google-chat",
                data={"message": message},
                headers=headers_basic,
            ) as response:
                data = await response.text()
                console.print(f"Retorno de enviar msg no chat: {data}")
                # return await response.json()

    except Exception as e:
        err_msg = f"Erro ao enviar mensagem ao Google Chat: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None
    
async def unlock_queue(id: str):
    env_config, _ = load_env_config()
    try:      
        headers_basic = {"Authorization": f"Basic {env_config["API_AUTHORIZATION"]}"}       
        

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                f"{env_config["API_BASE_URL"]}/fila/unlock-queue/{id}",                
                headers=headers_basic,
            ) as response:
                return await response.text()

    except Exception as e:
        err_msg = f"Erro ao desbloquear a fila: {e}"
        logger.error(err_msg)
        console.print(
            f"{err_msg}\n",
            style="bold red",
        )
        return None


def read_secret(path: str, vault_token: str):
    

    url = f"https://aspirina.simtech.solutions/{path}"
    headers = {"X-Vault-Token": vault_token, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["data"]["data"]
    elif response.status_code == 403:
        err_msg = "403 - Token inválido!"
        logger.error(err_msg)
        console.print(f"\n{err_msg}\n", style="bold red")
    else:
        response.raise_for_status()


def load_environments(env: str, vault_token: str):

    environments = {}   
    credentials = {}

    environments[env] = read_secret(path=f"v1/{env}-sim/data/worker-automate-hub/env", vault_token=vault_token)
    credentials[env] = read_secret(path=f"v1/{env}-sim/data/worker-automate-hub/credentials.json", vault_token=vault_token)

    return environments[env], credentials[env]
