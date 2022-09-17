def get_active_table_name():
    with open('database/db_properties.txt', 'r', encoding='utf-8') as properties:
        content = properties.read().split('\n')
    for line in content:
        if line.startswith('active_table'):
            return line.split(':')[1].strip()