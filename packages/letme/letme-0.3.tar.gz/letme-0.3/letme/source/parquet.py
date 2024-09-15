def read_parquet(app, params):
    file_path = params.get('file_path')

    if not file_path:
        print('''Parquet object needs the following parameters:
        - file_path
        ''')
        return
    return app.spark.read.parquet(file_path)