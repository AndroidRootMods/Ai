import os
import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# تحميل مفتاح الخدمة الخاص بـ Google Cloud
key_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
credentials = service_account.Credentials.from_service_account_file(key_path)

# تهيئة المتغيرات اللازمة للاتصال بـ Dialogflow
project_id = os.environ['DIALOGFLOW_PROJECT_ID']
language_code = 'en'
session_client = dialogflow.SessionsClient(credentials=credentials)

def detect_intent(text, session_id):
    """التحقق من النص المرسل وارجاع الإجابة المناسبة"""
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

# تعريف API Flask لتمكين استدعاء الدالة `detect_intent`
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    """التحقق من النص المرسل عبر API وإرجاع الإجابة المناسبة"""
    request_data = request.get_json()
    text = request_data['text']
    session_id = request_data['session_id']
    response_text = detect_intent(text, session_id)
    return jsonify({'text': response_text})
