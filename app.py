from flask import render_template, Flask,request,jsonify
from db import Session, UserInfo
import user_agents
from pymongo import MongoClient

app = Flask(__name__,template_folder="templates")

# Підключення до MongoDB Atlas через URI
uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient(uri)

# Вибір бази даних
db = client["<dbname>"]
collection = db["your_collection"]

# Приклад: знайти всі документи в колекції
documents = collection.find({})
for doc in documents:
    print(doc)

@app.get("/")
def index():
    return render_template("index.html")

@app.get('/collect_info')
def collect_info():
    with Session.begin() as session:
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
         ip_address = request.remote_addr

        # Получаем User-Agent заголовок
        user_agent_str = request.headers.get('User-Agent')
        user_agent = user_agents.parse(user_agent_str)

        # Определяем тип устройства, ОС и браузер
        device_type = "Mobile" if user_agent.is_mobile else "Desktop" if user_agent.is_pc else "Tablet"
        os = user_agent.os.family
        browser = user_agent.browser.family

        # Создаем запись в базе данных
        new_user_info = UserInfo(
            ip_address=ip_address,
            user_agent=user_agent_str,
            device_type=device_type,
            os=os,
            browser=browser
        )

        session.add(new_user_info)
        session.commit()

        return jsonify({
            "message": "Information collected",
            "ip_address": ip_address,
            "device_type": device_type,
            "os": os,
            "browser": browser
        })
    return "Error"

if __name__ == "__main__":
    app.run()