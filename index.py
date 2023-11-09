
# import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from dash import Dash, dcc, html, Input, Output, callback

df = pd.read_csv('file_csv/gara_all_clean.csv')
data = pd.read_csv('file_csv/data_car_all.csv')
showroom = pd.read_csv('file_csv/showroom_all_clean.csv')
thuexe = pd.read_csv('file_csv/thuexe_all.csv')

data_company = pd.read_csv('file_csv/data_oto_all.csv')

provinces = df['Province'].dropna().unique()

data = data.drop_duplicates()

# Thêm 'Toàn quốc' vào danh sách unique_provinces
provinces = list(provinces)
provinces.append('Toàn quốc')

service = pd.concat([data['Service'], data_company['Service']]).unique()

group = pd.read_csv('file_csv/group_oto_sg.csv')

brand_counts = df.groupby(['Province', 'Brand']).size().reset_index(name='Count')
df['Brand'] = df['Brand'].replace(['Huyndai', 'Huynhdai'], 'Multibrand')
df1 = df.drop_duplicates(subset=['Company']).drop_duplicates(['Name Gara']).drop_duplicates(subset=['Address'])

brand = pd.concat([df['Brand'], showroom['Brand']]).dropna()

showroom['Province'] = showroom['Province'].replace({'TP HCM': 'Tp Hcm', 'TT Huế': 'Tt Huế', 'Khánh Hoà': 'Khánh Hòa'})

# Ve do thi area
loan_car_province = thuexe.groupby(['Province']).size().reset_index(name='Count')




#cgo
# do thi group
fig_group = go.Figure()

fig_group.add_trace(go.Scatter(x=group['Group'], y=group['NumberOfThreads'], mode='markers+lines', name='Chủ đề'))
fig_group.update_xaxes(title_text='Group hãng xe')
fig_group.update_yaxes(title_text='Số lượng ')


fig_group.add_trace(go.Scatter(x=group['Group'], y=group['NumberOfArticles'], mode='markers+lines', name='Bài viết'))
fig_group.update_xaxes(title_text='Group hãng xe')

fig_group.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=2, color='DarkSlateGrey')))
# Thay đổi màu nền cho tiêu đề và trục
fig_group.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black')
)
# Thay đổi màu nền cho tiêu đề và trục
fig_group.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black'),

)
# Thêm lưới và đường kết nối giữa các điểm
fig_group.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')
fig_group.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')

fig_group.update_layout(title='Số lượng chủ đề và bài viết của group xe oto',title_x=0.5)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True,
           # external_stylesheets=external_stylesheets,

           )

# tabs_styles = {
#     'height': '44px',
#     'align-items': 'center'
# }
# tab_style = {
#     'borderBottom': '1px solid #d6d6d6',
#     'padding': '6px',
#     'fontWeight': 'bold',
#     'border-radius': '15px',
#     'background-color': '#F2F2F2',
#     'box-shadow': '4px 4px 4px 4px lightgrey',
#
# }
#
# tab_selected_style = {
#     'borderTop': '1px solid #d6d6d6',
#     'borderBottom': '1px solid #d6d6d6',
#     'backgroundColor': '#119DFF',
#     'color': 'white',
#     'padding': '6px',
#     'border-radius': '15px',
# }


app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='Gara-Showrrom', value='tab-1'),
        dcc.Tab(label='Group', value='tab-2'),
        # dcc.Tab(label='Upload file', value='tab-3'),
    ], colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"
    }),
    html.Div(id='tabs-content-props')
])

@callback(Output('tabs-content-props', 'children'),
              Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([

                html.Div([
                    html.Div([
                        html.Div([
                            html.H3('Garage Information in Vietnam', style={'margin-bottom': '0px', 'color': 'white'}),
                        ])
                    ], className="create_container1 twelve columns", id="title"),

                ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

                # drop down list (region)
                html.Div([
                    html.Div([
                        html.P('Select Region', className='fix_label',
                               style={'color': 'white', 'text-align': 'center'}),
                        dcc.Dropdown(id='select_region',
                                     multi=False,
                                     clearable=True,
                                     disabled=False,
                                     style={'display': True},
                                     value='Toàn quốc',
                                     placeholder='Select Province',
                                     options=[{'label': c, 'value': c}
                                              for c in (provinces)], className='dcc_compon')

                    ], className="create_container1 six columns", style={'margin-bottom': '8px'}),

                    html.Div([
                        html.P('Select Service', className='fix_label',
                               style={'color': 'white', 'text-align': 'center'}),



                        dcc.Dropdown(id='select_service',
                                     options=[{'label': c, 'value': c}
                                              for c in (service)],
                                     value=service[3],
                                     multi=False,
                                     clearable=True,
                                     disabled=False,
                                     style={'display': True},
                                     placeholder='Select Service', className='dcc_compon')

                    ], className="create_container1 six columns", style={'margin-bottom': '8px'}),

                ], className="row flex-display"),

                # data table
                html.Div([
                    html.Div([

                        html.P('Choose', className='fix_label', style={'text-align': 'center', 'color': 'red'}),
                        dcc.RadioItems(id='id_choose', options=['Gara', 'Showroom'],
                                       value='Showroom',
                                       inline=True,
                                       style={'text-align': 'center', 'color': 'white'}, className='custom-radio-items'),
                        # html.Br(),
                        dcc.Graph(id='top_1',
                                  config={'displayModeBar': 'hover'}),

                    ], className='create_container six columns'),

                    html.Div([
                        html.Br(),
                        dcc.Graph(id='top_2',
                                  config={'displayModeBar': 'hover'}),

                    ], className='create_container six columns'),

                ], className='row flex-display'),

                html.Div([
                    html.Div([
                        html.Br(),
                        dcc.Graph(id='top_3',
                                  config={'displayModeBar': 'hover'}),

                    ], className='create_container six columns'),

                    html.Div([
                        html.Br(),
                        dcc.Graph(id='top_4',
                                  config={'displayModeBar': 'hover'}),

                    ], className='create_container six columns'),

                ], className='row flex-display'),

                html.Div([
                    html.Div([
                        html.P('Select Brand', className='fix_label', style={'color': 'white', 'text-align': 'center'}),
                        dcc.Dropdown(id='select_brand',
                                     multi=False,
                                     clearable=True,
                                     disabled=False,
                                     style={'display': True},
                                     value='Multibrand',
                                     placeholder='Select Brand',
                                     options=[{'label': c, 'value': c}
                                              for c in (brand.unique())], className='dcc_compon')

                    ], className="create_container1 twelve columns", style={'margin-bottom': '8px'}),



                ], className="row flex-display"),

                # combination of bar and line chart (population and area)
                html.Div([
                    html.Div([
                        html.Br(),
                        dcc.Graph(id='bar_line_1',
                                  config={'displayModeBar': 'hover'}),

                    ], className='create_container six columns'),

                    # line chart (birth rate vs death rate)
                    html.Div([
                        html.Br(),
                        dcc.Graph(id='line_1',
                                  config={'displayModeBar': 'hover'}),

                    ], className='create_container six columns'),

                ], className='row flex-display'),



            ], id="mainContainer", style={"display": "flex", "flex-direction": "column"})

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div([
               html.Div([
                   html.Br(),
                   html.P('Visualize', className='fix_label', style={'text-align': 'center', 'color': 'red'}),
                   dcc.RadioItems(id='id_visua', options=['Group', 'Automobile Company'],
                                  value='Group',
                                  inline=True,
                                  style={'text-align': 'center', 'color': 'white'}, className='custom-radio-items')
               ])
            ],"row flex-display"),

            html.Div([
                html.Div([

                    dcc.Graph(id='chart_tab2',
                              config={'displayModeBar': 'hover'})], className="create_container1 twelve columns"),

            ], className="row flex-display"),
        ])


@app.callback(Output('top_1', 'figure'),
              [Input('select_region', 'value'),
               Input('id_choose', 'value')])
def update_graph(select_region, id_choose):

    tq_gara = df[['Brand', 'Name Gara']].groupby('Brand').agg(Name_count=('Name Gara', 'count')).reset_index()
    tq_gara.columns = ['Brand', 'Count']

    tq_showroom = showroom[['Brand', 'Name']].groupby('Brand').agg(Name_count=('Name', 'count')).reset_index()
    tq_showroom.columns = ['Brand', 'Count']

    brand_counts_showroom = showroom.groupby(['Province', 'Brand']).size().reset_index(name='Count')

    if select_region != 'Toàn quốc':
        if id_choose == 'Gara':
            filtered_brand_counts = brand_counts[brand_counts['Province'] == select_region]
        else:
            filtered_brand_counts = brand_counts_showroom[brand_counts_showroom['Province'] == select_region]
    else:
        if id_choose == 'Gara':
            filtered_brand_counts = tq_gara
        else:
            filtered_brand_counts = tq_showroom



    return {
        'data': [
                go.Pie(
                    labels=filtered_brand_counts['Brand'],  # Use 'Thương hiệu' for labels
                    values=filtered_brand_counts['Count'],         # Use 'Count' for values
                    textinfo='percent+label',  # Display percentage and label
                    hole=0.3,  # Set the size of the central hole
                    hoverinfo='label+percent+value',
                    marker=dict(
                        colors=['#04B77A', '#FFA500', '#FF6347', '#36C9E4', '#D8BFD8'],  # Define colors
                        line=dict(color='white', width=2)  # Add white borders to slices
                    )
                )
        ],

        'layout': go.Layout(
            plot_bgcolor='#010915',
            paper_bgcolor='#010915',
            title={
                'text': 'Top Brands of Gara in ' + select_region,  # Adjust the title as needed
                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                'color': 'white',
                'size': 15},

            hovermode='closest',
            margin=dict(l=130, b=0, r=0, t=17)
        )
    }



@app.callback(Output('top_3', 'figure'),
              [Input('select_region', 'value')])
def update_graph(select_region):

    data_all = pd.concat([data[['Name', 'Province', 'Service']], data_company[['Name', 'Province', 'Service']]])
    service_counts = data_all.groupby(['Province', 'Service']).size().reset_index(name='Count')

    tq_data = data_all[['Service', 'Name']].groupby('Service').agg(Name_count=('Name', 'count')).reset_index()
    tq_data.columns = ['Service', 'Count']

    # Use your brand_counts DataFrame instead of top_country_world
    if select_region != 'Toàn quốc':
        service_counts_filter = service_counts[service_counts['Province'] == select_region]
    else:
        service_counts_filter = tq_data

    bar_chart = go.Figure()

    bar_chart.add_trace(go.Bar(
        x=service_counts_filter['Service'],
        y=service_counts_filter['Count'],
        text=service_counts_filter['Count'],
        hoverinfo='text',
        hovertext=[f'{prov} - {count}' for prov, count in
                   zip(service_counts_filter['Service'], service_counts_filter['Count'])],
        marker_color =['#04B77A', '#FFA500', '#FF6347', '#36C9E4', '#D8BFD8', '#FF69B4', '#7B68EE', '#40E0D0',
                       '#87CEFA', '#FA8072']
    ))

    bar_chart.update_layout(
        xaxis_title='Service',
        yaxis_title='Count',
        title={
            'text': f'Dịch vụ về oto tại {select_region}',
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        # title_x=0.5,
        titlefont={'color': 'white', 'size': 15},
        xaxis=dict(
            title='<b>Service</b>',
            color='white',
            showline=True,
            # showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='white'
            )
        ),
        yaxis=dict(
            title='<b>Count</b>',
            autorange=True,
            color='white',
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='white',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='white'
            )
        ),
        plot_bgcolor='#010915',
        paper_bgcolor='#010915',
        hovermode='closest',
        margin=dict(l=130, b=0, r=0, t=17)
    )

    return bar_chart


@app.callback(Output('top_2', 'figure'), [Input('select_service', 'value')])
def update_graph(select_service):
    dt = data_company.groupby(['Service', 'Years active']).size().reset_index(name='Count')
    dt = dt.drop(dt[dt['Years active'] == 0].index)

    data_years = dt[dt['Service'] == select_service]
    stick_chart = px.strip(data_years, x='Years active', y='Count',
                           title=f'Stick Chart for Years Active in {select_service}',
                           orientation='v',  # 'v' for vertical
                           color_discrete_sequence=['#3498db'])  # Set color (e.g., blue)

    # Customize the chart appearance
    stick_chart.update_layout(
        plot_bgcolor='#010915',
        paper_bgcolor='#010915',
        font=dict(family='Arial', size=14, color='white'),
        title_font=dict(size=18, color='white'),
        showlegend=False,
        title_x=0.5,

        xaxis=dict(
            title='<b>Years Active</b>',
            color='white',
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=12,
                color='white'
            )
        ),
        yaxis=dict(
            title='<b>Count</b>',
            color='white',
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=12,
                color='white'
            )
        )
    )

    return stick_chart


@app.callback(Output('top_4', 'figure'),
              [Input('select_service', 'value')])

def update_graph(select_service):
    data_cpn_all = pd.concat([data[['Name', 'Province', 'Service']], data_company[['Name', 'Province', 'Service']]])
    dt1 = data_cpn_all.groupby(['Service', 'Province']).size().reset_index(name='Count')
    count_car = dt1[dt1['Service'] == select_service]
    area_chart = px.area(count_car, x='Province', y='Count', title='Số lượng doanh nghiệp ngành ' + str(select_service))

    # Customize the chart appearance
    area_chart.update_layout(
        plot_bgcolor='#010915',
        paper_bgcolor='#010915',
        font=dict(family='Arial', size=14, color='white'),  # Font settings
        title_font=dict(size=18, color='white'),  # Title font settings
        showlegend=True,  # Hide legend
        title_x=0.5,

        xaxis=dict(title='<b></b>',
                   color='white',
                   showline=True,
                   showgrid=False,
                   showticklabels=True,
                   # linecolor='white',
                   # linewidth=2,
                   # ticks='outside',
                   tickfont=dict(
                       family='Arial',
                       size=12,
                       color='white'
                   )

                   ),
        yaxis=dict(title='<b>Số lượng doanh nghiệp</b>',
                   color='white',
                   showline=True,
                   showgrid=False,
                   showticklabels=True,
                   # linecolor='white',
                   # linewidth=2,
                   # ticks='outside',
                   tickfont=dict(
                       family='Arial',
                       size=12,
                       color='white'
                   )

                   ),

    )

    area_chart.update_traces(
        fill='tozeroy',  # Fill area to the x-axis
        line=dict(color='#52BE80 ', width=2),  # Line style
        hovertemplate='<b>%{x}</b><br>Count: %{y}',  # Hover template
    )

    return area_chart

# combination of bar and line chart (population and area)
@app.callback(Output('bar_line_1', 'figure'),
              [Input('select_brand', 'value')])


def update_graph(select_brand):
    # Create a bar chart for brand counts by province (brand_pro DataFrame)
    brand_pro = df.groupby(['Brand', 'Province']).size().reset_index(name='Count')
    brand_lk = df.groupby(['Brand', 'Liên kết']).size().reset_index(name='Count')

    # Filter data for the selected brand
    brand_pro_selected = brand_pro[brand_pro['Brand'] == select_brand]

    brand_lk_selected = brand_lk[brand_lk['Brand'] == select_brand]
    province_names = brand_pro_selected['Province'].tolist()
    # Create a bar chart for brand counts by province
    bar_pro_fig = go.Bar(
        x=brand_pro_selected['Province'],
        y=brand_pro_selected['Count'],
        text=brand_pro_selected['Province'],  # Set the text to display the province names
        hoverinfo='text',
        hovertext=[f'{prov} - {count}' for prov, count in zip(brand_pro_selected['Province'], brand_pro_selected['Count'])],
        name='Province',
    )

    # Create a bar chart for brand counts by link
    bar_lk_fig = go.Bar(
        x=brand_lk_selected['Liên kết'],  # Use 'Liên kết' for x-axis
        y=brand_lk_selected['Count'],  # Use 'Count' for y-axis
        text=brand_lk_selected['Liên kết'],
        hoverinfo='text',
        hovertext=[f'{prov} - {count}' for prov, count in zip(brand_lk_selected['Liên kết'], brand_lk_selected['Count'])],
        name='Insurance company'
    )

    return {
        'data': [bar_pro_fig, bar_lk_fig],  # Return both bar charts
        'layout': go.Layout(
            plot_bgcolor='#010915',
            paper_bgcolor='#010915',
            title={
                'text': f'Biểu đồ số lượng hãng xe {select_brand}',
                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            titlefont={'color': 'white', 'size': 15},
            hovermode='closest',

            margin=dict(l=130, b=0, r=0, t=17),
            xaxis=dict(
                title='<b>Tỉnh và Công ty bảo hiểm</b>',
                color='white',
                showline=True,
                showgrid=True,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            ),
            yaxis=dict(
                title='<b>Số lượng gara</b>',
                autorange=True,
                color='white',
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='white',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='white'
                )
            )
        )
    }


# line_1
@app.callback(Output('line_1', 'figure'),
              [Input('select_brand', 'value')])
def update_graph(select_brand):


    quantity_car = showroom.groupby(['Brand', 'Province'])['Quantity'].sum().reset_index()
    brand_quantity_car = quantity_car[quantity_car['Brand'] == select_brand]
    return {
        'data': [go.Scatter(
                   x=brand_quantity_car['Province'],
                   y=brand_quantity_car['Quantity'],
                   name='Birth Rate',
                   mode='markers+lines',
                   marker=dict(color='green'),
                   hoverinfo='text',
                   hovertemplate='<b>%{x}</b><br>Count: %{y}'

            )],



        'layout': go.Layout(
             plot_bgcolor='#010915',
             paper_bgcolor='#010915',
             title={
                'text': 'Biểu đồ số lượng hãng xe : ' + (select_brand) + ' đang bán tai showroom',

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={'family': 'Oswald',
                        'color': 'white',
                        'size': 15},

             hovermode='x',
             margin=dict(b=100),

             xaxis=dict(title='<b></b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                        ),

             yaxis=dict(title='<b>Số lượng xe</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                        ),

             legend=dict(title='',
                         x=0.35,
                         y=1.2,
                         orientation='h',
                         bgcolor='#010915',
                         traceorder="normal",
                         font=dict(
                              family="sans-serif",
                              size=12,
                              color='white')),


                 )

    }

@app.callback(Output('chart_tab2', 'figure'),
              [Input('id_visua', 'value')])

def update_graph(id_visua):

    service_company = pd.concat([data, data_company])
    service_company = service_company.groupby(['Service', 'Province'])['Name'].count().reset_index()
    service_company.rename(columns={'Name': 'Company Count'}, inplace=True)


    if id_visua == 'Group':
        return fig_group
    elif id_visua == 'Automobile Company':
        fig = px.sunburst(service_company, path=['Service', 'Province'], values='Company Count', color='Company Count', color_continuous_scale='viridis')

        fig.update_layout(
            title={
                'text': 'Số lượng công ty của các tỉnh thành phân bố theo ngành',
                'x': 0.5
            },
            margin=dict(t=50, l=0, r=0, b=0),
        )

        return fig


if __name__ == '__main__':
    app.run(debug=True)