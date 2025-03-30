import requests
from PIL import Image
from io import BytesIO

api_url = "https://jx.iqfk.top/60s.php?key=54K55paw6Iqx6Zuo"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    data = response.json()
    if data.get('data', {}).get('image'):
        image_url = data['data']['image']
        img_response = requests.get(image_url, headers=headers)
        img_response.raise_for_status()

        image = Image.open(BytesIO(img_response.content))
        image.show()
    else:
        print("未找到图片链接")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP错误: {http_err}")
except Exception as e:
    print(f"发生错误: {e}")
