welcome_msg = """
Welcome!

This script will generate sql for creating a database, user,
and giving the user full permissions on the specified host like this:

********************************************
CREATE DATABASE <dbname>;
CREATE USER '<usr>'@'<host>' IDENTIFIED BY '<pw>';
GRANT ALL PRIVILEGES ON <dbname>.* TO '<usr>'@'<host>';
********************************************
"""

params = {
    "host" : 'localhost',
    "db" : '',
    "usr" : '',
    "pw" : '',
}

def update_params():
    global params
    for k, v in params.items():
        new_val = input(f'Enter value for {k} (default: {v}): ')
        if new_val:
            params[k] = new_val

def create_sql():
    sql = {
    "db_sql" : f"CREATE DATABASE {params['db']};",
    "usr_sql" : f"CREATE USER '{params['usr']}'@'{params['host']}' IDENTIFIED BY '{params['pw']}';",
    "perm_sql" : f"GRANT ALL PRIVILEGES ON {params['db']}.* TO '{params['usr']}'@'{params['host']}';",
    }
    return sql

def print_sql(sql):
    print('********************************************\n')
    for s in sql:
        print(sql[s])
    print('\n********************************************')
    
def main():
    print(welcome_msg)
    update_params()
    print_sql(create_sql())


if __name__ == '__main__':
    main()









