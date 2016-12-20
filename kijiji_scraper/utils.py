from itertools import chain


def parse_table(table):
    data = []
    rows = table.find_all('tr')
    for row in rows:
        header_cols = [ele.text.strip() for ele in row.find_all('th')]

        cols = [ele.text.strip() for ele in row.find_all('td')]
        data.append([ele for ele in chain(header_cols, cols) if ele])
    return data
