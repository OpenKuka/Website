import sys, os, glob
import markdown
import yaml
from yaml.loader import SafeLoader
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
from collections import OrderedDict
import re

# https://stackoverflow.com/a/53647080/7060811
class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['line-start'] = node.start_mark.line + 1
        mapping['line-end'] = node.end_mark.line
        return mapping

def declare_variables(variables, macro):
    """
    This is the hook for the functions

    - variables: the dictionary that contains the variables
    - macro: a decorator function, to declare a macro.
    """

    keys = ['enums', 'strucs', 'variables', 'functions']

    
    def GetNameSpace(filepath):
        base = os.path.basename(filepath)
        filename = os.path.splitext(base)[0]
        tokens = filename.split('.')
        namespace = '.'.join(token.title() for token in tokens)
        return namespace

    def Load():

        path = './docs/krl/reference/yaml/'
        namespaces = {}

        

        for filepath in glob.glob(os.path.join(path, '*.yml')):
            namespace = GetNameSpace(filepath)
            stream = open(filepath, 'r')
            dic = yaml.load(stream, Loader=SafeLineLoader)

            # add namespace to each element
            for k in keys:
                if k in dic and dic[k] != None:
                    for i in range(len(dic[k])):
                        dic[k][i]['namespace'] = namespace

            namespaces[namespace] = dic
        
        
        variables['allnamespaces'] = namespaces

        # add entries by type for cross ref
        for k in keys:
            k1 = "all" + k
            variables[k1] = []
            for namespace in namespaces:
                if k in namespaces[namespace]:
                    if namespaces[namespace][k] != None:
                        variables[k1].extend(namespaces[namespace][k])

        # create type index
        variables["alltypes"] = {}
        for k in keys[0:2]:
            for namespace in namespaces:
                if k in namespaces[namespace]:
                    if namespaces[namespace][k] != None:
                        for i in range(len(namespaces[namespace][k])):
                            t = namespaces[namespace][k][i]
                            variables["alltypes"][t['name']] = t 

        # crossref index name = {value, path, line}
        variables["xref"] = {}
        for namespace in namespaces:
            for k in keys:
                if k in namespaces[namespace] and namespaces[namespace][k] != None :
                    for i in range(len(namespaces[namespace][k])):
                        node_value =  namespaces[namespace][k][i]
                        node_name = node_value['name']
                        node_path = namespace
                        node_type = k
                        variables["xref"][node_name] = {'value': node_value, 'type': node_type, 'path': node_path, 'line-start': node_value['line-start'], 'line-end': node_value['line-end']}

        
    md = markdown.Markdown(extensions=['pymdownx.caret'])
    

    Load()

    def split(txt, seps):
        default_sep = seps[0]

        # we skip seps[0] because that's the default seperator
        for sep in seps[1:]:
            txt = txt.replace(sep, default_sep)
        return [i.strip() for i in txt.split(default_sep)]

    def InlineMdFilter(text):
        if text != None:
            html = md.convert(text)
            # strip the enclosing <p></p> tags of the converted text
            html = html.strip()
            n = len(html)
            if html[0:3] == '<p>':
                html = html[3:]
            n = len(html)
            if html[n-4:n] == '</p>':
                html = html[0:n-4]
            
            # replace xref lables in the html
            return XRefFilter(html)
        else:
            return text

    def XRefFilter(html):
        regex = r'&lt;xref:([\$\w]+)&gt;' # match <xref:NAME>
        # regex = r'<xref:([\$\w]+)>' # match <xref:NAME>

        def repl(match):
            key = match.group(1)
            if key in variables["xref"]:
                node = variables["xref"][key]
                path = "../" + node['path'] + "/#" + key.lower().strip('$')
                return '<a href="' + path + '" class="krl tippy" title="' + node['value']['description'] +'">' + str(key) + '</a>'
            else:
                return key
        
        # return "bob"
        return re.sub(regex, repl, html, re.MULTILINE, re.IGNORECASE)


    def ArrayDimFilter(text):
        res = split(text, ('[', ']'))
        if len(res) > 1:
            return res[1]
        return ''

    def ArrayTypeFilter(text):
        res = split(text, ('[', ']'))
        if len(res) > 1:
            return res[0]
        return ''

    def EnumListFilter(values):
        html = []
        for value in values:
            html.append("<span title='Mytitle'><code>" + "#" + str(value['name']) + "</code></span>")
        return ', '.join(html)

    @macro
    def NamespaceToMarkdown(namespace):
        
        variables['namespace_filter'] = namespace
        j2_env = Environment(loader=FileSystemLoader('./theme/templates/'), trim_blocks=True)
        j2_env.filters['markdown'] = lambda text: InlineMdFilter(text)
        j2_env.filters['arraydim'] = lambda text: ArrayDimFilter(text)
        j2_env.filters['arraytype'] = lambda text: ArrayTypeFilter(text)
        j2_env.filters['enumlist'] = lambda values: EnumListFilter(values)
        # j2_env.filters['xref'] = lambda text: XRefFilter(text)
        j2_env.filters['enum'] = lambda text: "`#" + str(text) + "`" 
        j2_tpl = j2_env.get_template('namespace.j2')
        return j2_tpl.render(variables)

    @macro
    def GetTypePath(typename):
        if typename in variables["alltypes"]:
            t = variables["alltypes"][typename]
            return './' + t['namespace'].lower() + '/#' + typename
        else:
            return ''

    @macro
    def ListNamespaces():
        path = './docs/krl-ref/ref/'
        namespaces = []
        for filepath in glob.glob(os.path.join(path, '*.yml')):
            namespace = GetNameSpace(filepath)
            namespaces.append(namespace)
        return ', '.join(namespaces)


    # Give a name to each python function
    # macro(ListNamespaces, 'ListNamespaces')
    # macro(GetTypePath, 'GetTypePath')