# System Variables

## System.String

{% for var in variables %}

{% set name = '`' + variables[var]['name'] + '`' %}
{% set description = variables[var]['description'] %}

### **{{ variables[var]['name'] }}**
*{{description}}*

<!-- STRUC -->
{% if 'STRUC' in variables[var]['data-type'] %}
{% set type = '`STRUC`: [' + variables[var]['type'] + '](../types/#' + variables[var]['type'] + ')' %}

| Name         | Type     |
|--------------|----------|
| {{name}}   | {{type}} |

| Field    | Description | Type     | Unit     | Constraint     |
|----------|-------------|----------|----------|----------------|
{% for field in variables[var]['fields']%}{{name}}.**`{{field['name']}}`** | {{field['description']}} | `{{field['data-type']}}` | {{field['unit']}} | {{field['constraint']}} |
{% endfor %}

<!-- ENUM -->
{% elif 'ENUM' in variables[var]['data-type'] %}
{% set type = '`ENUM`: [' + variables[var]['type'] + '](../types/#' + variables[var]['type'] + ')' %}

| Name         | Type     | Values |
|--------------|----------| -------|
| {{name}}     | {{type}} | <small>{{types[variables[var]['type']]['valueList']|join(', ')}}</small> |

<!-- CHAR -->
{% elif 'CHAR' in variables[var]['data-type'] %}
{% set type = variables[var]['data-type'] %}

| Name         | Type     |
|--------------|----------|
| {{name}}     | {{type}} |

<!-- BOOL -->
{% elif 'BOOL' in variables[var]['data-type'] %}
{% set type = variables[var]['data-type'] %}

| Name         | Type     |
|--------------|----------|
| {{name}}     | {{type}} |

| Value     | Description |
|-----------|-------------|
| `true` | {{variables[var]['description-true']}} |
| `false` | {{variables[var]['description-false']}} |


<!-- BOOL, INT, REAL, CHAR, STRING -->
{% else %}

{% set type = '`' + variables[var]['data-type'] + '`' %}
{% set unit = variables[var]['unit'] %}
{% set constraint = variables[var]['constraint'] %}


| Name     | Type     | Unit     | Constraint     |
|-----------------|----------|----------|----------------|
| {{name}} | {{type}} | {{unit}} | {{constraint}} |


{% endif %}


<!-- COMMENT -->


{% if variables[var]['comments'] is defined and variables[var]['comments']|length %}
??? info "Info"
{{variables[var]['comments']|indent(4, true)}}
<!-- ??? info "Info"
{{variables[var]['comments']|indent(4, true)}} -->
{% endif %}

***
{% endfor %}

