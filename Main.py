import requests
from PIL import Image
from io import BytesIO

api_url = "https://jx.iqfk.top/60s.php?key=54K55paw6Iqx6Zuo"  #API可以直接拿去用，毕竟密钥是公开的(

response = requests.get(api_url) #记得使用GET请求，别整错了

if response.status_code == 200:
    try:
        data = response.json()
        if 'data' in data:
            if 'image' in data['data']:
                image_url = data['data']['image']
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image = Image.open(BytesIO(image_response.content))
                    image.show()
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"The response was: {response.text}")
