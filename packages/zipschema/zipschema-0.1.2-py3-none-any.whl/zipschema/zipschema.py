import os
import click
import yaml
import json
import zipfile
import pathlib
import jsonschema
from jinja2 import Template


# Helper function to load YAML file
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Helper function to load JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Resolve schema references ($ref) for jsonschema and zipschema
def resolve_reference(file_item, base_path):
    schema_path = file_item.get('schema')
    if schema_path:
        if schema_path.endswith(('.json', '.jsonschema')):
            schema_file = os.path.join(base_path, schema_path)
            schema = load_json(schema_file)
            return schema, 'jsonschema'
        elif schema_path.endswith(('.yaml', '.yml', '.zipschema')):
            schema_file = os.path.join(base_path, schema_path)
            schema = load_yaml(schema_file)
            return schema, 'zipschema'
        elif schema_path in ['.', 'self', 'this']:
            return None, 'self'
    return None, None


# Validate a zipschema YAML structure
def validate_zipschema(schema):
    required_keys = ['name', 'description', 'version', 'elements']
    for key in required_keys:
        if key not in schema:
            raise ValueError(f"Missing required key: {key}")
    print("Schema is valid.")


# Validate files within a zip file against the schema
def validate_zip_file(schema, zip_path, base_path):
    if not zipfile.is_zipfile(zip_path):
        raise ValueError(f"{zip_path} is not a valid zip file.")

    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_contents = zip_file.namelist()
        elements = schema.get('elements', [])

        for element in elements:
            for condition, files in element.items():
                if condition in ["allOf", "anyOf", "oneOf", "noneOf", "allowed"]:
                    validate_condition(condition, files, zip_contents, base_path)
                else:
                    print(f"Unknown condition: {condition}")

        print(f"Validation of {zip_path} completed.")


# Function to handle different conditionals: allOf, anyOf, oneOf, noneOf, and allowed
def validate_condition(condition, files, zip_contents, base_path):
    matched_files = []
    for file_item in files:
        pattern = file_item if isinstance(file_item, str) else file_item.get('path', '')

        matching_files = [file for file in zip_contents if pathlib.PurePath(file).match(pattern)]
        matched_files.extend(matching_files)

        if isinstance(file_item, dict) and 'schema' in file_item:
            resolved_schema, schema_type = resolve_reference(file_item, base_path)
            if schema_type == 'jsonschema':
                validate_jsonschema_file(file_item, matching_files, zip_contents)
            elif schema_type == 'zipschema':
                for matching_file in matching_files:
                    validate_zip_file(resolved_schema, matching_file, base_path)
            elif schema_type == 'self':
                validate_zip_file(load_yaml(base_path), matching_file, base_path)

    if condition == 'allOf' and len(matched_files) != len(files):
        raise ValueError(f"Not all required files found for 'allOf': {files}")
    elif condition == 'anyOf' and len(matched_files) == 0:
        raise ValueError(f"At least one file must match for 'anyOf': {files}")
    elif condition == 'oneOf' and len(matched_files) != 1:
        raise ValueError(f"Exactly one file must match for 'oneOf': {files}")
    elif condition == 'noneOf' and len(matched_files) > 0:
        raise ValueError(f"No files should match for 'noneOf': {files}")
    elif condition == 'allowed':
        for file in files:
            if file not in matched_files:
                print(f"Optional file missing: {file}")


# Validate a file using JSON Schema
def validate_jsonschema_file(file_item, matching_files, zip_contents):
    for file in matching_files:
        if file in zip_contents:
            with zipfile.ZipFile(zip_contents, 'r') as zip_file:
                with zip_file.open(file) as f:
                    try:
                        data = json.load(f)
                        schema = file_item.get('schema')
                        jsonschema.validate(instance=data, schema=schema)
                        print(f"File {file} passed JSON schema validation.")
                    except jsonschema.ValidationError as e:
                        print(f"JSON schema validation error in file {file}: {e}")
        else:
            print(f"File {file} not found in zip.")


# Generate documentation from the zipschema in Markdown or AsciiDoc
def generate_documentation(schema, output_format):
    doc_template = """
    # {{ schema.name }} (Version: {{ schema.version }})

    {{ schema.description }}

    ## File Overview:

    | File Path | Description | Conditional |
    |-----------|-------------|-------------|
    {% for element in schema.elements %}
      {% for file in element[element | first] %}
    | {{ file.link if file.link else file.path }} | {{ file.description if file.description else 'No Description' }} | {{ element | first }} |
      {% endfor %}
    {% endfor %}

    ## Detailed Elements:

    {% for element in schema.elements %}
    ### {{ element.section_title }} ({{ element | first }})

    {{ element.section_description }}

    | File Path | Description | Schema Reference |
    |-----------|-------------|------------------|
    {% for file in element[element | first] %}
    | {{ '[{}]({})'.format(file.path, file.link) if file.link else file.path }} | {{ file.description if file.description else 'No Description' }} | {{ file.schema if file.schema else 'None' }} |
    {% endfor %}
    {% endfor %}
    """

    template = Template(doc_template)
    documentation = template.render(schema=schema)

    if output_format == 'markdown':
        output_file = 'schema_documentation.md'
    else:
        output_file = 'schema_documentation.adoc'

    with open(output_file, 'w') as file:
        file.write(documentation)

    print(f"Documentation generated: {output_file}")


@click.group()
def cli():
    """Zipschema Validator and Documentation Generator CLI"""
    pass


@cli.command()
@click.argument('schema_path')
def validate_schema(schema_path):
    """Validate a zipschema YAML file."""
    try:
        schema = load_yaml(schema_path)
        validate_zipschema(schema)
        print(f"Schema {schema_path} is valid.")
    except Exception as e:
        print(f"Error: {e}")


@cli.command()
@click.argument('schema_path')
@click.argument('zip_path')
def validate_zip(schema_path, zip_path):
    """Validate a zip file against a zipschema."""
    try:
        schema = load_yaml(schema_path)
        validate_zipschema(schema)
        base_path = os.path.dirname(schema_path)
        validate_zip_file(schema, zip_path, base_path)
    except Exception as e:
        print(f"Error: {e}")


@cli.command()
@click.argument('schema_path')
@click.option('--format', type=click.Choice(['markdown', 'asciidoc']), default='markdown')
def generate_docs(schema_path, format):
    """Generate documentation from a zipschema."""
    try:
        schema = load_yaml(schema_path)
        validate_zipschema(schema)  # Validate the schema before generating docs
        generate_documentation(schema, format)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    cli()
