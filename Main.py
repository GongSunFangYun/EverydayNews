import requests
from PIL import Image
from io import BytesIO

api_url = "https://jx.iqfk.top/60s.php?key=54K55paw6Iqx6Zuo"

response = requests.get(api_url)

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
                    print(f"The response was: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"The response was: {response.text}")