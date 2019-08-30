function.zip: requirements.zip build_status.py
	cp requirements.zip function.zip
	zip -g function.zip build_status.py

requirements.zip: requirements.txt
	rm -rf build
	python3 -m venv build
	. build/bin/activate ; \
	pip3 install -r requirements.txt ; \
	cd build/lib/python*/site-packages ; \
	zip -g -r ../../../../requirements.zip . -x "*__pycache__*"

upload: function.zip
	aws lambda update-function-code --function-name TrafficLightMLInfra --zip-file fileb://function.zip

.PHONY: upload
