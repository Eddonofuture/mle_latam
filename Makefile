install:
	pip3 install --upgrade pip && pip3 install -r api/requirements.txt
lint:
	pylint --disable=R,C api/api.py
