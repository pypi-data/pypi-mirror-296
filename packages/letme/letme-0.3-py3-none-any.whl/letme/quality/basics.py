from time import time
from datetime import datetime

def check_condition(source, condition: str):
    t1 = time()
    source.data.createOrReplaceTempView('tmp')
    total = source.app.spark.sql('select * from tmp') 
    failed = source.app.spark.sql(f'select * from tmp where not ({condition})')
    total_count = total.count()
    failed_count = failed.count()
    t2 = time()
    summary = {
            'execution_time': t2 - t1,
            'date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'source_name': source.source_name,
            'source_type': source.source_type,
            'user': source.app.username,
            'check_type': 'check_condition',
            'total_count': total_count,
            'failed_count': failed_count,
            'success_percentage': ( (total_count-failed_count) / total_count) * 100,
            'source_params': source.params
    }
    return [summary, failed]