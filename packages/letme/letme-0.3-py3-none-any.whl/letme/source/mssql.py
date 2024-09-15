def read_mssql(app, params):
    query = params.get('query')
    server = params.get('server')
    database = params.get('database')
    username = params.get('username')
    password = params.get('password')
    port = params.get('port')

    if not query or not server or not database or not username or not password:
        print('''MSSQL object needs the following parameters:
        - query
        - server
        - database
        - username
        - password
        - port (optional, default to 1433)
        ''')
        return
    
    if not port:
        port = '1433'
    else:
        port = port

    sqlsUrl = f'jdbc:sqlserver://{server}:{port};database={database};trustServerCertificate=true'
    jdbc_options = {
            "url": sqlsUrl,
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "user": username,
            "password": password
    }
    qryStr = f'({query}) t'
    return app.spark.read.format('jdbc').option('dbtable', qryStr ).options(**jdbc_options).load()