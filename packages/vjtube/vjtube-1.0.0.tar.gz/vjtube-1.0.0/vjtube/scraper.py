from datetime import datetime
import os
from playwright.sync_api import sync_playwright
from .utils import sanitize_filename

TIPOS_VIDEOS = ['CD Melhores', 'Coletânea', 'Compilado']
FILTROS = {
    'relevancia': 'CAASAhAB',
    'data_de_envio': 'CAI%253D'
}

class YouTubeScraper:
    def __init__(self, termo_pesquisa: str):
        self.termo_pesquisa = termo_pesquisa
        self.base_path = "screenshots"

    def buscar_videos(self) -> list:
        """
        Faz a busca por vídeos no YouTube, salva dados e screenshots para o termo de pesquisa,
        e retorna uma lista com as informações dos vídeos encontrados.

        :return: Lista de dicionários com informações dos vídeos.
        """
        todos_videos = []  # Lista para armazenar todos os vídeos encontrados.

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(no_viewport=True)
            page = context.new_page()

            for tipo_video in TIPOS_VIDEOS:
                for filtro_nome, filtro_valor in FILTROS.items():
                    # Gera a URL de busca
                    url = f"https://www.youtube.com/results?search_query={self.termo_pesquisa.replace(' ', '+')}+{tipo_video.replace(' ', '+')}&sp={filtro_valor}"
                    print(f"Navegando para: {url}")
                    page.goto(url)

                    page.wait_for_selector("ytd-video-renderer")

                    total_videos = self._carregar_todos_videos(page, limite_videos=200)
                    print(f"Total de vídeos encontrados: {total_videos}")

                    dados_videos = self._extrair_dados_videos(page)
                    self._salvar_dados_e_screenshots(dados_videos, tipo_video, filtro_nome)

                    # Adiciona os vídeos encontrados à lista total
                    todos_videos.extend(dados_videos)

            browser.close()

        # Retorna a lista com todas as informações dos vídeos
        return todos_videos

    def _carregar_todos_videos(self, page, limite_videos: int = 200, max_tentativas: int = 50) -> int:
        """
        Scrolla a página até carregar o número desejado de vídeos.
        """
        total_videos = 0
        tentativas = 0

        while total_videos < limite_videos and tentativas < max_tentativas:
            videos = page.query_selector_all("ytd-video-renderer")
            novos_videos = len(videos)

            if novos_videos > total_videos:
                total_videos = novos_videos
                print(f"Vídeos carregados: {total_videos}")
                ultimo_video = videos[-1]
                ultimo_video.scroll_into_view_if_needed()
                page.wait_for_timeout(2000)
            else:
                print(f"Tentativa {tentativas + 1}: Sem novos vídeos carregados.")
            
            tentativas += 1

        return total_videos

    def _extrair_dados_videos(self, page) -> list:
        """
        Extrai informações de vídeos da página.

        :return: Lista de dicionários contendo as informações de cada vídeo.
        """
        videos = page.query_selector_all("ytd-video-renderer")
        dados_videos = []

        for video in videos:
            titulo_elem = video.query_selector("#video-title")
            metadata_elem = video.query_selector_all("#metadata-line span")
            link_elem = video.query_selector("#video-title")
            canal_elem = video.query_selector("ytd-channel-name yt-formatted-string")

            if titulo_elem and metadata_elem and link_elem and canal_elem:
                titulo = titulo_elem.text_content().strip()
                views = metadata_elem[0].text_content().strip() if len(metadata_elem) > 0 else "N/A"
                publicado_em = metadata_elem[1].text_content().strip() if len(metadata_elem) > 1 else "N/A"
                canal = canal_elem.text_content().strip()
                link = f"https://www.youtube.com{link_elem.get_attribute('href')}"
                
                dados_videos.append({
                    "titulo": titulo,
                    "views": views,
                    "publicado_em": publicado_em,
                    "canal": canal,
                    "link": link,
                    "elemento": video  # Mantemos o elemento para salvar screenshots.
                })
        
        return dados_videos

    def _salvar_dados_e_screenshots(self, dados_videos: list, tipo_video: str, filtro_nome: str) -> None:
        """
        Salva screenshots e dados dos vídeos, organizados em pastas por cantor, tipo de vídeo e filtro.
        """
        # Adiciona um diretório separado pelo nome do cantor
        pasta_cantor = os.path.join(self.base_path, sanitize_filename(self.termo_pesquisa))
        pasta_filtro = os.path.join(pasta_cantor, sanitize_filename(tipo_video), sanitize_filename(filtro_nome))
        os.makedirs(pasta_filtro, exist_ok=True)

        for video in dados_videos:
            titulo = sanitize_filename(video['titulo'])
            data = sanitize_filename(video['publicado_em'])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{titulo}_{data}_{timestamp}.png"
            
            print(f"Salvando screenshot para: {video['titulo']}")
            video['elemento'].screenshot(path=os.path.join(pasta_filtro, nome_arquivo))

            print(f"Título: {video['titulo']}\nViews: {video['views']}\nData: {video['publicado_em']}\nCanal: {video['canal']}\nLink: {video['link']}\n")
