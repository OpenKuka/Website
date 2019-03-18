# System Functions


## System.String

{% for f in functions %}

{% set name = '`' + functions[f]['name'] + '`' %}
{% set description = functions[f]['description'] %}
{% set params = functions[f]['parameters'] %}
{% set rtype = functions[f]['return-type'] %}
{% set rdesc = functions[f]['return-description'] %}
{% set comments = functions[f]['comments'] %}
{% set sample = functions[f]['code-sample'] %}

### **{{ functions[f]['name'] }}**
*{{description}}*

{% if params is defined %}
**Parameters**

<table>
    <thead>
        <tr>
        <th style="min-width:10em">Parameter</th>
        <th style="min-width:4em">Value/Ref</th>
        <th style="min-width:10em">Type</th>
        <th>Description</th>
        </tr>
    </thead>
    <tbody>
{% for p in params %}
{% set type = p['type'] %}
        <tr>
            <td><code>{{p['name']}}</code></td>
            <td><code>{{p['pass']}}</code></td>
            <td><code>
                {% if types[type] is defined %}
                    <a href="../types/#{{p['type']}}">{{p['type']}}</a>
                {% else %}
                    {{p['type']}}
                {% endif %}
            </code></td>
            <td>{{p['description']}}</td>
        </tr>
{% endfor %}
    </tbody>
</table>

{% endif %}
{% if rtype is defined %}
**Return**

| Type | Description |
|------|-------------|
|`{{rtype}}`|{{rdesc}}|
{% endif %}

{% if comments is defined %}
**Comments**

!!! note ""
{{comments|indent(4, true)}}
{% endif %}

{% if sample is defined %}
**Sample**

```pascal
{{sample|indent(0, true)}}
```
{% endif %}

***

{% endfor %}

