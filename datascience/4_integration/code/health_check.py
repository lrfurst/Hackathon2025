import requests

def check_service():
    try:
        # Tenta acessar o health check do FastAPI
        res = requests.get("http://localhost:8000/health")
        if res.status_code == 200:
            print("🟢 API Python está respondendo corretamente.")
        else:
            print("🔴 API Python com problemas.")
    except:
        print("⚪ API Python está offline.")

if __name__ == "__main__":
    check_service()
