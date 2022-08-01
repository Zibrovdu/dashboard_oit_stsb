staff_style = [
    {'if': {'filter_query': f'{{4}} >= 0 && {{4}} <= 30', 'column_id': 3}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{4}} < 0', 'column_id': 3}, 'backgroundColor': '#add2f8'},
    {'if': {'filter_query': f'{{4}} > 30', 'column_id': 3}, 'backgroundColor': '#d5adfb'},
    {'if': {'filter_query': f'{{4}} >= 0 && {{4}} <= 30', 'column_id': 4}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{4}} < 0', 'column_id': 4}, 'backgroundColor': '#add2f8'},
    {'if': {'filter_query': f'{{4}} > 30', 'column_id': 4}, 'backgroundColor': '#d5adfb'},
    {'if': {'filter_query': f'{{7}} >= 60 && {{7}} < 70', 'column_id': 7}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{7}} < 60', 'column_id': 7}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{7}} >= 70', 'column_id': 7}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{8}} >= 75 && {{7}} < 85', 'column_id': 8}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{8}} < 75', 'column_id': 8}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{8}} >= 85', 'column_id': 8}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{9}} > 10 && {{9}} <= 15', 'column_id': 9}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{9}} > 15', 'column_id': 9}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{9}} <= 10', 'column_id': 9}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{10}} <= "30:" && {{10}} >"24:"', 'column_id': 10}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': '{10} <= "24:"', 'column_id': 10}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': '{10} > "30"', 'column_id': 10}, 'backgroundColor': 'tomato', 'color': 'white'},
]

region_style = [
    {'if': {'filter_query': f'{{4}} > 60 && {{4}} < 70', 'column_id': 4}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{4}} < 60', 'column_id': 4}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{4}} >= 70', 'column_id': 4}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{6}} > 75 && {{6}} < 85', 'column_id': 6}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{6}} < 75', 'column_id': 6}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{6}} >= 85', 'column_id': 6}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{8}} > 10 && {{8}} < 15', 'column_id': 8}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{8}} > 15', 'column_id': 8}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{8}} <= 10', 'column_id': 8}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{9}} < "30:" && {{9}} > "24:"', 'column_id': 9}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': '{9} <= "24:"', 'column_id': 9}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': '{9} > "30"', 'column_id': 9}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{12}} >= 6', 'column_id': 12}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{12}} < 6 && {{12}} > 4', 'column_id': 12}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{12}} < 4', 'column_id': 12}, 'backgroundColor': 'tomato', 'color': 'white'}
]

picture_day_table_style = [{'if': {'column_id': i}, 'backgroundColor': '#D6ECFF'} for i in range(4, 13)]

kpi_style = {
    'if': {
        'column_id': 0
    },
    'textAlign': 'left'
}

kpi_style_big = {
    'if': {
        'column_id': 1
    },
    'textAlign': 'left'
}

tooltips = {
    '2_column':
        """
Количество обращений закрытых сотрудником за выбранный период
    """,
    '3_column':
        """
__Алгоритм расчета среднего значения:__

- Рассчитали квартили, и определили 
межквартильный размах
- Убрали слишком большие и слишком малые 
значения (выбросы)
- Рассчитали среднее на очищенных от 
выбросов данных
    """,
    '4_column':
        """
Количество открытых обращений закрытых сотрудником за выбранный период
    """,
    'pd_2_column':
        """
    
    """
}
