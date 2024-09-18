import time
from playwright.sync_api import sync_playwright

from .datas_user import load_data_session


def fetch_artist(artist, file_session, target_videos_count=10):
    """Busca pela quantidade de views em determinado perfil(`artist`), com `target_videos_count` sendo seu limite de videos procurados

    Args:
        artist (str): @nome_do_perfil para encontra-lo no tiktok
        file_session (str): path do arquivo de sessão salvo
        target_videos_count (int, optional): quantidade de videos alvos para procurar no perfil. Default 10.

    Returns:
        views (list): lista com a quantidade de views
    """
    with sync_playwright() as p:
        # estancia do navegador
        browser = p.chromium.launch(headless=False)

        # passando uma nova pagina com contexto
        contexto = browser.new_context()

        # Carrega os dados da sessão
        load_data_session(contexto, file_session)

        # Abre uma nova página com os dados da sessão carregados
        pg = contexto.new_page()

        # vai para o site do tiktok no pefil do artista
        pg.goto(f"https://www.tiktok.com/{artist}")

        # seletor do video da pagina do tiktok
        video_seletor = ".css-1uqux2o-DivItemContainerV2.e19c29qe8"

        time.sleep(3)
        # pega a quantidade de tags encontrada para iterar
        lista_de_videos = pg.query_selector_all(video_seletor)

        print("videos encontrados:", len(lista_de_videos))

        # verifica se tem videos na lista
        if len(lista_de_videos) > 0:

            # lista de armazenamento de views
            views = []

            # itera sobre os videos
            for i, video in enumerate(lista_de_videos):

                # seletor da quantidade de views
                x = f"#main-content-others_homepage > div > div.css-833rgq-DivShareLayoutMain.ee7zj8d4 > div.css-1qb12g8-DivThreeColumnContainer.eegew6e2 > div > div:nth-child({i+1}) > div > div > div > a > div > div.css-11u47i-DivCardFooter.e148ts220 > strong"

                # localiza o elemento de texto das views
                text = pg.locator(
                    x,
                ).inner_text()

                # acrecenta na lista de views
                views.append(text)

                # para caso tenha chegado ao limite de videos alvos
                if i >= target_videos_count:
                    break

            return views

        return None
