staff_style = [
    {'if': {'filter_query': f'{{3}} >= -30 && {{3}} <= 30', 'column_id': 2}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{3}} < -30', 'column_id': 2}, 'backgroundColor': '#add2f8'},
    {'if': {'filter_query': f'{{3}} > 30', 'column_id': 2}, 'backgroundColor': '#d5adfb'},
    {'if': {'filter_query': f'{{3}} >= -30 && {{3}} <= 30', 'column_id': 3}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{3}} < -30', 'column_id': 3}, 'backgroundColor': '#add2f8'},
    {'if': {'filter_query': f'{{3}} > 30', 'column_id': 3}, 'backgroundColor': '#d5adfb'},
    {'if': {'filter_query': f'{{6}} >= 60 && {{6}} < 70', 'column_id': 6}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{6}} < 60', 'column_id': 6}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{6}} >= 70', 'column_id': 6}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{7}} >= 75 && {{7}} < 85', 'column_id': 7}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{7}} < 75', 'column_id': 7}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{7}} >= 85', 'column_id': 7}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{8}} > 10 && {{8}} <= 15', 'column_id': 8}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': f'{{8}} > 15', 'column_id': 8}, 'backgroundColor': 'tomato', 'color': 'white'},
    {'if': {'filter_query': f'{{8}} <= 10', 'column_id': 8}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': f'{{9}} <= "30:" && {{9}} >"24:"', 'column_id': 9}, 'backgroundColor': '#fcb500'},
    {'if': {'filter_query': '{9} <= "24:"', 'column_id': 9}, 'backgroundColor': '#c4fbdb'},
    {'if': {'filter_query': '{9} > "30"', 'column_id': 9}, 'backgroundColor': 'tomato', 'color': 'white'},
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
}