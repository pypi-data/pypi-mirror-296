import requests

class art:
    BASE_URL = 'https://api.aspirart.com'

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
    
    def get_account_details(self):
        response = requests.get(f'{self.BASE_URL}/account/details', headers=self.headers)
        return response.json()
    
    def check_auth(self):
        response = requests.get(f'{self.BASE_URL}/account/check', headers=self.headers)
        return response.json()
    
    def generate_image(self, model, prompt, negative_prompt="", steps=10, cfg=7.5, seed=None, batch_size=1):
        payload = {
            'model': model,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'steps': steps,
            'cfg': cfg,
            'seed': seed,
            'batch_size': batch_size
        }
        response = requests.post(f'{self.BASE_URL}/txt2img', json=payload, headers=self.headers)
        return response.json()
