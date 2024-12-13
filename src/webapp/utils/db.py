def groupby_query_rows(groupby_column_n : int, query: list) -> dict:
    """
    Groups query rows by value in column, passed in `groupby_column_n`.

    Parameters
    ----------
    groupby_column_n : int
        Number of columns whose values are used for groupby.

    query: list
        Query to calculate groupby for.

    Returns
    ----------
    groupby_dict : dict
        Dict with results with following structure: 
        column value as key and list with rows as value.
    """
    groupby_dict = {}

    if groupby_column_n > len(query[0]) - 1:
        raise ValueError("Column number for groupby is bigger than biggest available column number!"
                         f"{groupby_column_n} > {len(query[0]) - 1}")
    
    for row in query:
        key = row[groupby_column_n]
        if key not in groupby_dict:
            groupby_dict[key] = [row] 
        groupby_dict[key].append(row)

    return groupby_dict