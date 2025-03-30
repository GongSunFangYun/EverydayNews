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

api_url = "https://jx.iqfk.top/60s.php?key=54K55paw6Iqx6Zuo"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    logger.info("开始请求API: %s", api_url)
    response = requests.get(api_url, headers=headers)
    logger.debug("收到API响应，状态码: %d", response.status_code)
    response.raise_for_status()

    try:
        logger.info("尝试解析JSON响应...")
        data = response.json()
        logger.debug("JSON解析结果: %s", data)

        if data.get('data', {}).get('image'):
            image_url = data['data']['image']
            logger.info("从JSON中获取图片URL: %s", image_url)

            logger.info("开始下载图片...")
            img_response = requests.get(image_url, headers=headers)
            logger.debug("图片下载响应状态码: %d", img_response.status_code)
            img_response.raise_for_status()

            logger.info("尝试打开图片...")
            image = Image.open(BytesIO(img_response.content))
            logger.info("成功打开图片，准备显示...")
            image.show()
            logger.info("图片已显示...")
        else:
            error_msg = "JSON中未找到image链接！"
            logger.warning(error_msg)
            raise ValueError(error_msg)

    except ValueError as ve:
        logger.error("JSON解析失败: %s", ve)
        logger.info("尝试直接解析响应内容为图片...")

        try:
            image = Image.open(BytesIO(response.content))
            logger.info("成功直接打开图片，准备显示...")
            image.show()
            logger.info("图片已显示...")
        except Exception as img_err:
            logger.error("无法识别图片文件: %s", img_err)

except requests.exceptions.HTTPError as http_err:
    logger.error("HTTP请求错误: %s", http_err)
except Exception as e:
    logger.error("发生未预期错误: %s", e)
finally:
    logger.info("程序执行结束！")
