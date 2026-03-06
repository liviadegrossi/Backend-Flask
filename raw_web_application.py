from wsgiref.simple_server import make_server

def application(environ, start_server):

    products = [
        {'name': 'Notebook', 'price': 7499.99},
        {'name': 'Mouse', 'price': 125.99},
        {'name': 'Keyboard', 'price': 450.99},
        {'name': 'Monitor', 'price': 2100.99}
    ]

    html_list = ''
    for product in products:
        html_list += f'<li>{product['name']} | R$ {product['price']} </li>'

    start_server('200 Ok', [('Content-type', 'text/html;charset=utf-8')])
    with open('index.html', 'r', encoding='utf-8') as file:
        html = file.read()
    
    final_html = html.replace('{{products}}', html_list)

    return [final_html.encode('utf-8')]

make_server('', 5000, application).serve_forever()