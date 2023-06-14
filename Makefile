dev:
	pip install -r requirements.txt --break-system-packages
	cp -i sample.config.py config.py
	python app.py