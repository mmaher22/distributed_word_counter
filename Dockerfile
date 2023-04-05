FROM python:3.9-slim-buster

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "if [ $NODE_TYPE = 'remote' ]; then python remote_node.py; else python central_node.py; fi"]
