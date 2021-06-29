import configparser

from sqlalchemy import create_engine

cfg_parser = configparser.ConfigParser()
cfg_parser.read(r'assets/settings.rkz', encoding="utf-8")

db_username = cfg_parser['connect']['username']
db_password = cfg_parser['connect']['password']
db_name = cfg_parser['connect']['db']
db_host = cfg_parser['connect']['host']
db_port = cfg_parser['connect']['port']
db_dialect = cfg_parser['connect']['dialect']

table_name = cfg_parser['table_names']['db_table']

conn_string = create_engine(f'{db_dialect}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

tasks_closed_wo_3l = cfg_parser['SLA_params']['tasks_closed_wo_3l']
tasks_closed_wo_3l_name = cfg_parser['names_scatters']['tasks_closed_wo_3l_name']
tasks_closed_wo_3l_title = cfg_parser['titles']['tasks_closed_wo_3l_title']

tasks_wo_sla_violation = cfg_parser['SLA_params']['tasks_wo_sla_violation']
tasks_wo_sla_violation_name = cfg_parser['names_scatters']['tasks_wo_sla_violation_name']
tasks_wo_sla_violation_title = cfg_parser['titles']['tasks_wo_sla_violation_title']

tasks_back_work = cfg_parser['SLA_params']['tasks_back_work']
tasks_back_work_name = cfg_parser['names_scatters']['tasks_back_work_name']
tasks_back_work_title = cfg_parser['titles']['tasks_back_work_title']

mean_time_solve_wo_waiting = cfg_parser['SLA_params']['mean_time_solve_wo_waiting']
mean_time_solve_wo_waiting_name = cfg_parser['names_scatters']['mean_time_solve_wo_waiting_name']
mean_time_solve_wo_waiting_title = cfg_parser['titles']['mean_time_solve_wo_waiting_title']


mean_count_tasks_per_empl_per_day = cfg_parser['SLA_params']['mean_count_tasks_per_empl_per_day']
mean_count_tasks_per_empl_per_day_name = cfg_parser['names_scatters']['mean_count_tasks_per_empl_per_day_name']
mean_count_tasks_per_empl_per_day_title = cfg_parser['titles']['mean_count_tasks_per_empl_per_day_title']
mean_count_tasks_per_day_title = cfg_parser['titles']['mean_count_tasks_per_day']

color_schemes = dict(color0=['#007b00', '#24e0b8', '#ffcc51', '#ff8b76', '#ff3031', '#024f94'],
                     color1=['#ffd507', '#8da751', '#b2ceff', '#00a3e1', '#eccee2', '#f7528e'],
                     color2=['#ff070e', '#ec8a38', '#ffc785', '#e7e6eb', '#3baf1d', '#024f94'],
                     color3=['#ff6a00', '#ffb62a', '#65b016', '#9bd8da', '#9cb7bb', '#fa0088'],
                     color4=['#ffd901', '#ffbeae', '#ffade2', '#ff5682', '#f42439', '#28398d'],
                     color5=['#d3e9f0', '#76bcf5', '#5889b2', '#69d6cc', '#bad996', '#fed21f'],
                     color6=['#490009', '#ac0e28', '#bc4558', '#013766', '#012e67', '#f8a73f'],
                     color7=['#274b69', '#85a1c1', '#c6ccd8', '#3f4d63', '#012e67', '#f8a73f'],
                     color8=['#012e67', '#323e53', '#408fb4', '#bddfef', '#64566e', 'tomato'],
                     )
