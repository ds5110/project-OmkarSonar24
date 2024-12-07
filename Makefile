eda :
	python src/eda.py

tables :	
	python src/create_base_tables.py

demographics : tables
	python src/demographics.py

discharges : tables
	python src/discharges.py

procedure_buckets : tables
	python src/procedure_buckets.py

procedures_distinct_patients : tables
	python src/procedures_distinct_patients.py
