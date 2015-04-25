sample-data:
	@mkdir -p sample-data

sample-data/backend-python-homework.tar.gz: sample-data
	@wget https://s3.amazonaws.com/olark_pub/backend-python-homework.tar.gz --output-document sample-data/backend-python-homework.tar.gz

sample-data/backend-python-homework/small_input: sample-data/backend-python-homework.tar.gz
	@tar zxvf sample-data/backend-python-homework.tar.gz --directory sample-data

get-sample-data: sample-data/backend-python-homework/small_input

prepare-venv:
	@virtualenv venv
	@./venv/bin/pip install -r requirements.txt

clean-venv:
	@rm -rf venv

test-small: 
	@./venv/bin/python zorin/report.py sample-data/backend-python-homework/small_input > /tmp/small_output
	@diff /tmp/small_output sample-data/backend-python-homework/small_output

test-big:
	@./venv/bin/python zorin/report.py sample-data/backend-python-homework/big_input > /tmp/big_output
	@diff /tmp/big_output sample-data/backend-python-homework/big_output
