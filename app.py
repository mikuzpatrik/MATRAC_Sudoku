from dash import Dash, dash_table, dcc, html, Input, Output, callback
import igra as Igra 

app = Dash(__name__)

grid, game = Igra.get_game(9, 40)

app.layout = html.Div([
    dash_table.DataTable(
        id='table-editing-simple',
        data=[
            grid
        ],
        editable=True
    ),
])

if __name__ == '__main__':
    app.run(debug=True)