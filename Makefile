eda :
	python -B src/eda.py

tables :	
	python -B src/create_base_tables.py

demographics : tables
	python -B src/demographics.py

discharges : tables
	python -B src/discharges.py

treatment_buckets : tables
	python -B src/treatment_buckets.py

treatments : tables
	python -B src/treatments.py
