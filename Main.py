import requests
from PIL import Image
from io import BytesIO
import logging
from colorama import Fore, Style, init

init()


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        super().format(record)

        date_part = f"{Fore.GREEN}{record.asctime.split()[0]}{Style.RESET_ALL}"
        time_part = f"{Fore.CYAN}{record.asctime.split()[1]}{Style.RESET_ALL}"
        level_color = {
            'INFO': Fore.GREEN,
            'DEBUG': Fore.BLUE,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Fore.RED + Style.BRIGHT
        }.get(record.levelname, Fore.WHITE)
        level_part = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        message_part = f"{Fore.WHITE}{record.getMessage()}{Style.RESET_ALL}"
        return f"{date_part} {time_part} | {level_part} | {message_part}"


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = ColoredFormatter(
    fmt='%(asctime)s',
    datefmt='%y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

logger.handlers = [console_handler]


class DailyNewsFetcher:
    def __init__(self, apikey):
        self.api_url = "https://jx.iqfk.top/api/new"
        self.apikey = apikey
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_news(self, response_type='img'):
        params = {
            'apikey': self.apikey,
            'type': response_type
        }

        try:
            logger.info(f"开始请求API，类型: {response_type}")
            response = requests.get(self.api_url, params=params, headers=self.headers)
            logger.debug(f"收到API响应，状态码: {response.status_code}")
            response.raise_for_status()

            if response_type == 'json':
                data = response.json()
                logger.info("成功获取JSON格式新闻数据")
                return data
            elif response_type == 'text':
                text = response.text
                logger.info("成功获取文本格式新闻")
                return text
            elif response_type == 'img':
                image = Image.open(BytesIO(response.content))
                logger.info("成功获取图片格式新闻，准备显示...")
                image.show()
                return image
            elif response_type == 'web':
                html = response.text
                logger.info("成功获取网页格式新闻")
                return html
            else:
                raise ValueError(f"不支持的响应类型: {response_type}")

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP请求错误: {http_err}")
            raise
        except Exception as error:
            logger.error(f"发生未预期错误: {str(error)}")
            raise


if __name__ == "__main__":
    API_KEY = "********-****-****-****-******************"

    try:
        fetcher = DailyNewsFetcher(API_KEY)
        fetcher.fetch_news('img')

    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        logger.info("程序执行结束！")
