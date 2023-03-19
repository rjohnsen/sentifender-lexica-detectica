import streamlit as st
import json

st. set_page_config(layout="wide")

def load_schemas():
	with open("datacollectors/output/schemas.json", "r") as schemas_file:
		return json.load(schemas_file)

def get_table_names():
	schemas = load_schemas()

	names = []
	for schema in schemas:
		names.append(schema["name"])

	names.sort()

	return names

def get_table_definition(tablename):
	schemas = load_schemas()
	for schema in schemas:
		if schema["name"] == tablename.strip():
			return schema
	
	return False

def get_pivots(selected_table):
	# Get selected table
	source_data = get_table_definition(selected_table)

	source_fields = []

	# Prepare source fields for later comparison
	for field in source_data["fields"]:
		if field["name"] is not None:
			if field["name"] != "Timestamp":
				source_fields.append(field["name"])

	# Compare selected table with the others to find pivot points
	schemas = load_schemas()
	pivots = []

	for schema in schemas:
		schema_fields = []

		if schema["name"] != selected_table:
			for field in schema["fields"]:
				if field["name"] != "Timestamp":
					schema_fields.append(field["name"])

			via = list(set(source_fields).intersection(schema_fields))

			if len(via) > 0:
				pivots.append({
					"from": selected_table,
					"to": schema["name"],
					"via": via 
				})

	return pivots

with st.sidebar:
	st.image("images/kusto-alt-icon-original.svg")

	st.title("Sentifender Lexica Detectica")
	table_names = get_table_names()

	selected_table = st.selectbox(
		"Select table",
		table_names
	)

schema_data = get_table_definition(selected_table)

if schema_data is not False:
	st.header(f"{selected_table} (table)")
	st.subheader("Schema")
	st.table(schema_data["fields"])

	st.subheader(f"From {selected_table} you can pivot to ...")
	pivots = get_pivots(selected_table)

	for pivot in pivots:
		st.markdown(f"#### {pivot['to']}")
		st.table(pivot)

		st.write("The following Kusto query is machine generated and serves as a skeleton for further refinement by the analyst.")
		variable_name = f"{pivot['via'][0].lower()}Var"
		code_example = f'''
let {variable_name}="";
{selected_table}
| where {pivot["via"][0]} == {variable_name}
| join type=inner {pivot["to"]} on $left.{pivot["via"][0]} == $right.{pivot["via"][0]}'''
		st.code(code_example, language="powershell")
else:
	st.write(f"Oh ... {selected_table} can't be found.")


