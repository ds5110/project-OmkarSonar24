eda :
	python -B src/eda.py

tables :	
	python -B src/create_base_tables.py

demographics : tables
	python -B src/demographics.py

discharges : tables
	python -B src/discharges.py

procedure_buckets : tables
	python -B src/procedure_buckets.py

procedures_distinct_patients : tables
	python -B src/procedures_distinct_patients.py
