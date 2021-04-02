# main target
naeb.sqlite3: schema.ddl insert.py $(wildcard data/normalized/*.csv)
	rm -f naeb.sqlite3
	sqlite3 naeb.sqlite3 < schema.ddl
	. venv/bin/activate; python3 insert.py; deactivate

.PHONY : clean 

.extracted: extract.py .unzipped #$(wildcard data/raw/**/*.html)
	python3 extract.py

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

