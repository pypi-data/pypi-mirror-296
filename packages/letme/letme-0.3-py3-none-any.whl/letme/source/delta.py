def read_delta(app, params):
    query = params.get('query')

    if not query:
        print('''Delta object needs the following parameters:
        - query
        ''')
        return
    return app.sql(query)