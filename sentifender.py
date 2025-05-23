import streamlit as st
import json

from lib.markdown import Markdown

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
			tmp = {}

			for field in schema["fields"]:
				tmp[field["name"]] = field

			keys = list(tmp.keys())
			keys.sort()
			schema["fields"] = []

			for key in keys:
				schema["fields"].append(tmp[key])

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
	pivots = {}

	for schema in schemas:
		schema_fields = []

		if schema["name"] != selected_table:
			for field in schema["fields"]:
				if field["name"] != "Timestamp":
					schema_fields.append(field["name"])

			via = list(set(source_fields).intersection(schema_fields))

			if len(via) > 0:
				pivots[schema["name"]] = {
					"from": selected_table,
					"to": schema["name"],
					"via": via 
				}

	tmp = []
	keys = list(pivots.keys())
	keys.sort()

	for key in keys:
		tmp.append(pivots[key])

	return tmp

st.title("Sentifender Lexica Detectica")

tab1, tab2, tab3 = st.tabs(["Home", "XDR Tables", "Contact"])

with tab1:
	col1, col2 = st.columns(2)

	with col1:
		st.write("## Welcome")
		st.write("""
**Sentifender Lexica Detectica** is a searchable reference for Microsoft Defender XDR tables and schemas, designed specifically for threat hunters. Developed by **Roger Johnsen**, the founder of the [**Predefender Initiative on Threat Hunting**](https://www.predefender.com/), it provides a structured overview of available data sources, making it easier to understand pivoting possibilities during investigations. This resource also serves as a companion guide to [Predefender Threat Hunt Book](https://huntbook.predefender.com/), enhancing structured threat hunting workflows.  
""")
	with col2:
		st.image("images/t2.webp", width=1024)
with tab2:
	col1, col2 = st.columns(2)

	table_names = get_table_names()

	with col1:
		st.metric("Tables available", len(table_names), "")

	with col2:
		selected_table = st.selectbox(
			"Select table",
			table_names
		)

	st.write("---")

	schema_data = get_table_definition(selected_table)

	if schema_data is not False:
		st.write(f"## {selected_table}")
		st.write("### Schema")

		st.write(Markdown.renderTable(schema_data["fields"]))

		st.write(f"### Pivot points")
		pivots = get_pivots(selected_table)

		for pivot in pivots:
			st.markdown(f"#### {pivot['to']}")

			col1, col2 = st.columns(2)

			pivot["via"].sort()
			col1.write("##### Fields")
			col1.write(Markdown.renderList(pivot["via"]))

			col2.markdown("##### Kusto example")
			col2.write("> The following Kusto query is machine generated and serves as a skeleton for further refinement by the analyst.")
			variable_name = f"{pivot['via'][0].lower()}Var"

			code_example = f'''
	let {variable_name}="";
	{selected_table}
	| where {pivot["via"][0]} == {variable_name}
	| join kind=inner {pivot["to"]} on $left.{pivot["via"][0]} == $right.{pivot["via"][0]}'''
			col2.code(code_example, language="powershell")

			st.write("---")
	else:
		st.write(f"Oh ... {selected_table} can't be found.")
with tab3:
	st.image("images/whatsapp-qr.png")

	
