import sys, os, glob
import markdown
import yaml
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
from collections import OrderedDict

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

        path = './docs/krl-ref/ref/'
        namespaces = {}

        for filepath in glob.glob(os.path.join(path, '*.yml')):
            namespace = GetNameSpace(filepath)
            stream = open(filepath, 'r')
            dic = yaml.load(stream)

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
                if namespaces[namespace][k] != None:
                    variables[k1].extend(namespaces[namespace][k])

        # create type index
        variables["alltypes"] = {}
        for k in keys[0:2]:
            for namespace in namespaces:
                if namespaces[namespace][k] != None:
                    for i in range(len(namespaces[namespace][k])):
                        t = namespaces[namespace][k][i]
                        variables["alltypes"][t['name']] = t 

        
    md = markdown.Markdown(extensions=['pymdownx.caret'])
    

    Load()

    def split(txt, seps):
        default_sep = seps[0]

        # we skip seps[0] because that's the default seperator
        for sep in seps[1:]:
            txt = txt.replace(sep, default_sep)
        return [i.strip() for i in txt.split(default_sep)]

    def InlineMdFilter(text):
        html = md.convert(text)
        # strip the enclosing <p></p> tags of the converted text
        html = html.strip()
        n = len(html)
        if html[0:3] == '<p>':
            html = html[3:]
        n = len(html)
        if html[n-4:n] == '</p>':
            html = html[0:n-4]
        return html

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
        j2_env = Environment(loader=FileSystemLoader('./theme/'), trim_blocks=True)
        j2_env.filters['markdown'] = lambda text: InlineMdFilter(text)
        j2_env.filters['arraydim'] = lambda text: ArrayDimFilter(text)
        j2_env.filters['arraytype'] = lambda text: ArrayTypeFilter(text)
        j2_env.filters['enumlist'] = lambda values: EnumListFilter(values)
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