# include/soda/check_function.py
def check(scan_name, data_source, checks_subpath=None, duckdb_conn=None, project_root='include'):
    from soda.scan import Scan

    print('Running Soda Scan ...')
    config_file = f'{project_root}/soda/configuration.yml'
    checks_path = f'{project_root}/soda/checks'

    if checks_subpath:
        checks_path += f'/{checks_subpath}'

    scan = Scan()
    scan.set_verbose()
    if duckdb_conn != None:
        scan.add_duckdb_connection(duckdb_conn)
    #scan.add_configuration_yaml_file(config_file) this is not working with DuckDB
    scan.set_data_source_name(data_source)
    scan.add_sodacl_yaml_files(checks_path)
    scan.set_scan_definition_name(scan_name)
    result = scan.execute()
    print(scan.get_logs_text())

    if result != 0:
        raise ValueError('Soda Scan failed')

    return result