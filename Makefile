# main target
naeb.sqlite3: schema.ddl insert.py normalize # $(wildcard data/normalized/*.csv)
	# rm -f naeb.sqlite3
	# create naeb.sqlite3 from schema
	# activate venv (if necessary)
	# run insert.py with normalized_csvs

.PHONY : clean normalize

normalize: normalize.py $(wildcard data/extracted/*.csv)
	# activate venv (if necessary)
	# run normalize.py on unnormalized_data

extract: extract.py .unzipped #$(wildcard data/raw/**/*.html)
	. venv/bin/activate
	python3 extract.py
	. deactivate

.unzipped: data/raw.tar.gz
	# -m for new modification time
	tar -xzf $< -C data/
	touch .unzipped

clean:
	# remove intermediate files
	rm .unzipped
	rm -rf data/raw/
	rm -rf data/extracted/
	rm -rf data/normalized/
	rm -f naeb.sqlite3
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

