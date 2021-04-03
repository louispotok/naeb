.PHONY : clean 
EXTRACTED=data/extracted/tribes.csv data/extracted/uses.csv data/extracted/species.csv

naeb.tar.gz: export.sh naeb.sqlite3
	# there must be a better way to do this
	bash export.sh naeb.sqlite3
	tar -czf naeb.tar.gz data/naeb_dump/*.csv

naeb.sqlite3: schema.ddl src/insert.py $(EXTRACTED)
	rm -f naeb.sqlite3
	sqlite3 naeb.sqlite3 < schema.ddl
	. venv/bin/activate; python3 src/insert.py; deactivate


$(EXTRACTED): src/extract.py .unzipped 
	. venv/bin/activate; python3 src/extract.py; deactivate

.unzipped: data/raw.tar.gz
	tar -xzf $< -C data/
	touch .unzipped

clean:
	# remove intermediate files
	rm -rf data/raw/
	rm -rf data/extracted/*
	rm -rf data/from_db/*.csv
	rm -rf data/normalized/
	rm -f .unzipped
	rm -f naeb.sqlite3
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

