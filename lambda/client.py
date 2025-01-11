import requests


class Client:
    def __init__(self, url: str, api_key: str, model: str):
        self.url = url
        self.api_key = api_key
        self.model = model

    def api_request(self, prompt: str, question: str) -> dict:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": prompt}],
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": question}],
                },
            ],
        }

        response = requests.post(
            url=self.url,
            headers=self._headers(),
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    def webhook_request(self, question: str, context: dict) -> dict:
        local_payload = {
            "token": self.api_key,
            "question": question,
        }

        payload = {**context, **local_payload}
        response = requests.post(self.url, json=payload)
        response.raise_for_status()

        return response.json()

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP_Referer": "wordpress.jpt.land/ai",
            "X-Title": "jpt.land AI",
        }
