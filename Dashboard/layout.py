from dash import dcc, html


def create_layout(years_options):
    layout = html.Div([
        html.H1("Climatic Dashboard", style={'textAlign': 'center'}),
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=years_options,
                placeholder="Select Year"
            ),
            # Other components can be added here
        ], style={'width': '8%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        # Other layout components can be added here
    ])
    return layout
