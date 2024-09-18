import json
import time
from playwright.sync_api import sync_playwright


def save_data_session(context, file):
    """Salva os dados de sessão para logar no browser

    Args:
        context (BrowserContext): context page do playwright
        file (str): path ou name do arquivo que deseja salvar os dados
    """
    # Salva cookies
    cookies = context.cookies()
    # Salva local storage
    local_storage = []
    for pagina in context.pages:
        storage = pagina.evaluate("() => JSON.stringify(localStorage)")
        local_storage.append({"url": pagina.url, "storage": storage})

    # Salva cookies e local storage em um arquivo
    with open(file, "w") as f:
        json.dump({"cookies": cookies, "local_storage": local_storage}, f)


def load_data_session(context, file):
    """Carrega os dados de sessão salvos para abrir um navegador

    Args:
        context (BrowserContext): context page do playwright
        file (str): nome do arquivo onde contem os dados de sessão
    """
    # Carrega cookies e local storage de um arquivo
    with open(file, "r") as f:
        dados = json.load(f)

        # Define os cookies no contexto
        context.add_cookies(dados["cookies"])

        # Define o local storage em cada página
        for pagina in context.pages:
            for item in dados["local_storage"]:
                if pagina.url.startswith(item["url"]):
                    pagina.evaluate(
                        f"() => {{ const data = JSON.parse('{item['storage']}'); for (const key in data) {{ localStorage.setItem(key, data[key]); }} }}"
                    )
