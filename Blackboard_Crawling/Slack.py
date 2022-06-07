import requests

token = "[사용자토큰]"
channel = "#chatbot"
text = "HI, you did it!"

requests.post("https://slack.com/api/chat.postMessage",
    headers={"Authorization": "Bearer "+token},
    data={"channel": channel,"text": text})

