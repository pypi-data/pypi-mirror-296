def read_csv(app, params):
    file_path = params.get('file_path')
    header = params.get('header')
    delimiter = params.get('delimiter')

    if not file_path:
        print('''CSV object needs the following parameters:
        - file_path
        - header (optional, default to True)
        - delimiter (optional, default to ',')
        ''')
        return
    if not header:
        header = True
    if not delimiter:
        delimiter = ','
    return app.spark.read.option('header', header).option('inferSchema', 'true').option("delimiter", delimiter).csv(file_path)