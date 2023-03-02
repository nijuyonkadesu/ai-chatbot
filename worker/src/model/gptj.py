import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()


class GPT:
    def __init__(self):
        self.url = os.environ.get('MODEL_URL')
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('HUGGINFACE_INFERENCE_TOKEN')}"
            }
        # Empty Payload
        self.payload = {
            "inputs": "",
            "parameters": {
                "return_full_text": False,
                "use_cache": True,
                "max_new_tokens": 25
            }

        }

    def query(self, input: str) -> list:
        # Populating payload
        self.payload["inputs"] = f"Human: {input} Bot:"

        # Payload to JSON
        data = json.dumps(self.payload)

        response = requests.request(
            "POST", self.url, headers=self.headers, data=data)

        data = json.loads(response.content.decode("utf-8"))
        text = data[0]['generated_text']
        res = str(text.split("Human:")[0]).strip("\n").strip()
        return res


if __name__ == "__main__":
    print(GPT().query("How's your cousing bingGPT?"))
    # TODO: Try some other interesting model
