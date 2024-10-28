# Run backend

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 5000

# Run frontend

npm install
npm start

