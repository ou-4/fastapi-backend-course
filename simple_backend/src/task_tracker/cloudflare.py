import requests
import os

class CloudflareAI:
    def __init__(self):
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')  
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')    
        self.model = '@cf/meta/llama-3-8b-instruct'
    
    def get_advice(self, task_text: str) -> str:
        if not self.account_id or not self.api_token:
            return "AI не настроен"
        
        try:
            api_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты - полезный ассистент. Отвечай ТОЛЬКО на русском языке. Давай четкие, структурированные ответы с нумерованными шагами. Используй Markdown-разметку для форматирования."
                    },
                    {
                        "role": "user", 
                        "content": f"Дай подробные шаги для решения этой задачи на русском языке: {task_text}"
                    }
                ]
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            print(f"Cloudflare Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                return result.get('result', {}).get('response', 'Ответ получен')
            else:
                return f"Ошибка API: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Ошибка: {str(e)}"