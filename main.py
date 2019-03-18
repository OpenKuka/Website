import yaml

def declare_variables(variables, macro):
    """
    This is the hook for the functions

    - variables: the dictionary that contains the variables
    - macro: a decorator function, to declare a macro.
    """

    variables['baz'] = "John Doe"
    variables['peoples'] = [{"Name" : "Lionel", "Age" : 33}, {"Name" : "Blandine", "Age" : 31}]
    variables['peoples2'] = {"Lionel" : {"Name" : "Lionel", "Age" : 33}, "Blandine" : {"Name" : "Blandine", "Age" : 31}}
    # variables['variables'] = ["Lionel", "Blandine"]

    # Load System.Variables 
    stream = open("variables.yml", 'r')
    tmpdic = {}
    count = 1
    for doc in yaml.load_all(stream):
        tmpdic[doc['name']] = doc
    variables['variables'] = tmpdic

    # Load System.Types
    stream = open("types.yml", 'r')
    tmpdic = {}
    count = 1
    for doc in yaml.load_all(stream):
        if doc['data-type'] == 'ENUM':
            doc['valueList'] = []
            for value in doc['values']:
                doc['valueList'].append("#" + value['name'])
        tmpdic[doc['name']] = doc
    variables['types'] = tmpdic

     # Load System.Functions
    stream = open("functions.yml", 'r')
    tmpdic = {}
    count = 1
    for doc in yaml.load_all(stream):
        tmpdic[doc['name']] = doc
    variables['functions'] = tmpdic

    @macro
    def bar(x):
        return (2.3 * x) + 7

    def PrintVariable(x):
        document = """
        name: $OV_PRO1
        type: INT
        description: override program
        """
        documents = """
        ---
        name: $OV_PRO
        type: INT
        description: override program
        ---
        name: $OV_PRO2
        type: INT
        description: override program
        """
        stream = open("variables.yml", 'r')
        docs = yaml.load_all(stream)

        output = []
        for doc in docs:
            output.append("\n## %s \n **type:** %s" %(doc['name'], doc['data-type']))
            

        # with  as stream:
        #     try:
        #         for d in :
        #             return d
        #     except yaml.YAMLError as exc:
        #         print(exc)


        return '\n'.join(output)
    


    # Give a name to each python function
    macro(PrintVariable, 'PrintVariable')