all: install run
	@echo 'Building venv enviroment'

install: venv
	. venv/bin/activate && pip install -r requirements.txt

venv:
	test -d venv || python3 -m venv venv

run:
	. venv/bin/activate && pip -V
	. venv/bin/activate && (\
      python3 -c 'import sys; print(sys.prefix)'; \
      pip3 -V \
    )

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
