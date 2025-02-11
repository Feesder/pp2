import json

with open('sample-data.json', 'r') as json_file:
    data = json.load(json_file)
    print('Interface Status')
    print('================================================================================')
    print('DN                                                 Description           Speed    MTU')
    print('-------------------------------------------------- --------------------  ------  ------')
    for i in data['imdata']:
        print(f'{i['l1PhysIf']['attributes']['dn']}                              {i['l1PhysIf']['attributes']['speed']}   {i['l1PhysIf']['attributes']['mtu']}')
