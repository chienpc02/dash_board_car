from dash import Dash, html, dcc,Input, Output,dash_table
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd


df = pd.read_csv('file_csv/Gara_all_clean.csv')
data = pd.read_csv('data_car_all.csv')
showroom = pd.read_csv('showroom_all_clean.csv')
thuexe = pd.read_csv('thuexe_all.csv')

group = pd.read_csv('group_oto_sg.csv')

brand_counts = df.groupby(['Province', 'Brand']).size().reset_index(name='Count')
df['Brand'] = df['Brand'].replace(['Huyndai','Huynhdai'], 'Multibrand')
df1 = df.drop_duplicates(subset=['Company']).drop_duplicates(['Name Gara']).drop_duplicates(subset=['Address'])

brand = pd.concat([df['Brand'],showroom['Brand']])

showroom['Province'] = showroom['Province'].replace({'TP HCM': 'Tp Hcm','TT Huế':'Tt Huế','Khánh Hoà':'Khánh Hòa'})

# Ve do thi area
loan_car_province = thuexe.groupby(['Province']).size().reset_index(name='Count')



area_chart = px.area(loan_car_province, x='Province', y='Count', title='Số lượng doanh nghiệp cho thuê')

# Customize the chart appearance
area_chart.update_layout(
    xaxis_title='Province',
    yaxis_title='Count',
    plot_bgcolor='lightblue',
    paper_bgcolor='lightgray',
    font=dict(family='Arial', size=14, color='black'),  # Font settings
    title_font=dict(size=18, color='darkblue'),         # Title font settings
    showlegend=False,       # Hide legend
    title_x=0.5
)

area_chart.update_traces(
    fill='tozeroy',  # Fill area to the x-axis
    line=dict(color='darkblue', width=2),  # Line style
    hovertemplate='<b>%{x}</b><br>Count: %{y}',  # Hover template
)

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


app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('Garage Information in Vietnam', style={'margin-bottom': '0px', 'color': 'white'}),
            ])
        ], className="create_container1 four columns", id="title"),


    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),


# drop down list (region)
    html.Div([
        html.Div([
            html.P('Select Region', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
            dcc.Dropdown(id='select_region',
                     multi=False,
                     clearable=True,
                     disabled=False,
                     style={'display': True},
                     value= 'Hà Nội',
                     placeholder='Select Province',
                     options=[{'label': c, 'value': c}
                              for c in (df['Province'].dropna().unique())], className='dcc_compon')

         ], className="create_container1 four columns",  style={'margin-bottom': '8px'}),

    ], className="row flex-display"),




# data table
    html.Div([
        html.Div([
        html.Br(),
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
            dcc.Graph(figure= area_chart,id='top_4',
              config={'displayModeBar': 'hover'}),

    ], className='create_container six columns'),




 ], className='row flex-display'),

    html.Div([
        html.Div([
            html.P('Select Brand', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
            dcc.Dropdown(id='select_brand',
                     multi=False,
                     clearable=True,
                     disabled=False,
                     style={'display': True},
                     value= 'Multibrand',
                     placeholder='Select Brand',
                     options=[{'label': c, 'value': c}
                              for c in (brand.unique())], className='dcc_compon')

         ], className="create_container1 four columns",  style={'margin-bottom': '8px'}),

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

    html.Div([

        html.Div([
            html.Br(),
            html.Br(),
            dcc.Graph(figure = fig_group,id='top_',
                      config={'displayModeBar': 'hover'})], className="create_container1 twelve columns"),

            ], className="row flex-display"),

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})






@app.callback(Output('top_1', 'figure'),
              [Input('select_region', 'value')])
def update_graph(select_region):
    # Replace this line with your brand_counts DataFrame
    # brand_counts = df.groupby(['Province', 'Thương hiệu']).size().reset_index(name='Count')

    # Use your brand_counts DataFrame instead of top_country_world
    filtered_brand_counts = brand_counts[brand_counts['Province'] == select_region]

    return {
        'data': [go.Pie(
            labels=filtered_brand_counts['Brand'],  # Use 'Thương hiệu' for labels
            values=filtered_brand_counts['Count'],         # Use 'Count' for values
            textinfo='percent+label',  # Display percentage and label
            hole=0.3,  # Set the size of the central hole
            hoverinfo='label+percent+value',
            marker=dict(
                colors=['#04B77A', '#FFA500', '#FF6347', '#36C9E4', '#D8BFD8'],  # Define colors
                line=dict(color='white', width=2)  # Add white borders to slices
            )
        )],

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

@app.callback(Output('top_2', 'figure'),
              [Input('select_region', 'value')])
def update_graph(select_region):
    # Replace this line with your brand_counts DataFrame
    brand_counts_showroom = showroom.groupby(['Province', 'Brand']).size().reset_index(name='Count')
    # Use your brand_counts DataFrame instead of top_country_world
    filtered_brand_counts_showroom = brand_counts_showroom[brand_counts_showroom['Province'] == select_region]

    return {
        'data': [go.Pie(
            labels=filtered_brand_counts_showroom['Brand'],  # Use 'Thương hiệu' for labels
            values=filtered_brand_counts_showroom['Count'],         # Use 'Count' for values
            textinfo='percent+label',  # Display percentage and label
            hole=0.3,  # Set the size of the central hole
            hoverinfo='label+percent+value',
            marker=dict(
                colors=['#04B77A', '#FFA500', '#FF6347', '#36C9E4', '#D8BFD8'],  # Define colors
                line=dict(color='white', width=2)  # Add white borders to slices
            )
        )],

        'layout': go.Layout(
            plot_bgcolor='#010915',
            paper_bgcolor='#010915',
            title={
                'text': 'Top Brands of showroom in ' + select_region,  # Adjust the title as needed
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
    service_counts = data.groupby(['Province', 'Service']).size().reset_index(name='Count')

    # Use your brand_counts DataFrame instead of top_country_world
    service_counts_filter= service_counts[service_counts['Province'] == select_region]
    bar_chart = go.Figure()

    bar_chart.add_trace(go.Bar(
        x=service_counts_filter['Service'],
        y=service_counts_filter['Count'],
        text = service_counts_filter['Count'],
        hoverinfo = 'text',
        hovertext=[f'{prov} - {count}' for prov, count in
                   zip(service_counts_filter['Service'], service_counts_filter['Count'])],
        marker_color=['#04B77A', '#FFA500', '#FF6347', '#36C9E4', '#D8BFD8']
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
        x=brand_pro_selected['Province'],  # Use 'Province' for x-axis
        y=brand_pro_selected['Count'],  # Use 'Count' for y-axis
        text=brand_pro_selected['Province']  ,  # Set the text to display the province names
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
                   # hovertext=
                   # '<b>Brand</b>: ' + quantity_car[quantity_car['Brand'] == select_brand]['Brand'].astype(str) + '<br>'
                   # '<b>Country</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Country'].astype(str) + '<br>' +
                   # '<b>Birth Rate</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Birthrate'].astype(str) + '<br>'

            )],

            # go.Scatter(
            #     x=world_pop_1[world_pop_1['Region'] == select_region]['Country'],
            #     y=world_pop_1[world_pop_1['Region'] == select_region]['Deathrate'],
            #     name='Death Rate',
            #     mode='markers+lines',
            #     marker=dict(color='red'),
            #     hoverinfo='text',
            #     hovertext=
            #     '<b>Death Rate</b>: ' + world_pop_1[world_pop_1['Region'] == select_region]['Deathrate'].astype(str) + '<br>'
            #
            # )],


        'layout': go.Layout(
             plot_bgcolor='#010915',
             paper_bgcolor='#010915',
             title={
                'text': 'Hãng xe : ' + (select_brand),

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



# if __name__ == '__main__':
#     app.run_server(debug=True)