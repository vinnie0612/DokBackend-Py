setup:
	pip install -r requirements.txt --break-system-packages
	cp -i sample.config.py config.py
	echo "Run with make dev"

dev:
	python app.py