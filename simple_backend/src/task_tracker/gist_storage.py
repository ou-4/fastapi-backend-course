import json
import requests
import os

class GistStorage:
    def __init__(self, filename='tasks.json'):
        self.json_name = filename
        self.gist_id = os.getenv('GIST_ID')  
        self.github_token = os.getenv('GITHUB_TOKEN')  
    
    def load_tasks(self):
        if not self.gist_id or not self.github_token:
            return []
        
        try:
            headers = {"Authorization": f"token {self.github_token}"}
            response = requests.get(f"https://api.github.com/gists/{self.gist_id}", headers=headers)
            
            if response.status_code == 200:
                gist_data = response.json()
                tasks_content = gist_data['files'][self.json_name]['content']
                return json.loads(tasks_content)
            return []
        except:
            return []
    
    def save_tasks(self, task_list):
        if not self.gist_id or not self.github_token:
            return False
        
        try:
            gist_data = {
                "files": {
                    self.json_name: {
                        "content": json.dumps(task_list, indent=2, ensure_ascii=False)
                    }
                }
            }
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.patch(
                f"https://api.github.com/gists/{self.gist_id}",
                headers=headers,
                data=json.dumps(gist_data)
            )
            return response.status_code == 200
        except:
            return False