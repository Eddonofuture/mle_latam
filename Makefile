install:
	pip3 install --upgrade pip && pip3 install -r requirements.txt
lint:
	pylint --disable=R,C api/main.py
