# System Types

{% for t in types %}

{% set name = '`' + types[t]['name'] + '`' %}
{% set type = '`' + types[t]['data-type'] + '`' %}
{% set description = types[t]['description'] %}
{% set comments = types[t]['comments'] %}

## **{{ types[t]['name'] }}**
*{{description}}*

<!-- STRUC -->
{% if 'STRUC' in types[t]['data-type'] %}

| Name         | Data Type     |
|--------------|---------------|
| {{name}}     | {{type}}     |


<table>
    <thead>
        <tr>
        <th style="min-width:10em">Field</th>
        <th style="min-width:14em">Type</th>
        <th>Description</th>
        </tr>
    </thead>
    <tbody>
{% for field in types[t]['fields']%}
{% set dtype = field['data-type'] %}
        <tr>
            <td><code>{{field['name']}}</code></td>
            <td>
                {% if types[dtype] is defined %}
                    <code><a href="../types/#{{dtype}}">{{dtype}}</a><code>
                {% else %}
                    <code>{{dtype}}</code>
                {% endif %}
            </td>
            <td>{{field['description']}}</td>
        </tr>
{% endfor %}
    </tbody>
</table>

<!-- ENUM -->
{% elif 'ENUM' in types[t]['data-type']%}

| Name         | Data Type     |
|--------------|---------------|
| {{name}}     | {{type}}      |


| Value    | Description |
|----------|-------------|
{% for value in types[t]['values'] %}**`#{{value['name']}}`** | {{value['description']}} |
{% endfor %}

{% endif %}

{% if types[t]['comments'] is defined and types[t]['comments']|length %}
??? info "Info"
{{types[t]['comments']|indent(4, true)}}
{% endif %}

***
{% endfor %}

