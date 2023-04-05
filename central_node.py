import os
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import redis
import pandas as pd


# Set up Redis connection
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
r = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT)
# Set up Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Word Count Dashboard'),
    dcc.Graph(id='word-count-bar-chart'),
    dcc.Graph(id='word-count-word-cloud'),
    dcc.Interval(
        id='interval-component',
        interval=30000,  # update every second
        n_intervals=0
    )
])


# Update function for the Dash app
@app.callback(
    [dash.dependencies.Output('word-count-bar-chart', 'figure'),
     dash.dependencies.Output('word-count-word-cloud', 'figure')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_word_counts(n):
    # Get the word counts from Redis
    word_counts = r.hgetall('word_count')
    # Convert the byte strings to integers
    word_counts = {word.decode('utf-8'): int(count) for word, count in word_counts.items()}

    # Convert the word counts to a pandas DataFrame and sort by count
    word_counts_df = pd.DataFrame(list(word_counts.items()), columns=['word', 'count'])
    word_counts_df = word_counts_df.sort_values(by='count', ascending=False)
    # print(word_counts_df.head(10), '<---')

    # Create the bar chart
    bar_chart_fig = px.bar(word_counts_df.head(10), x='word', y='count', title='Top 10 Words')

    # Create the word cloud
    word_cloud_fig = px.scatter(word_counts_df, x=[1] * len(word_counts_df), y=[1] * len(word_counts_df),
                                text='word', size='count', size_max=60)
    word_cloud_fig.update_traces(textfont=dict(size=word_counts_df['count'] / 10))
    word_cloud_fig.update_layout(xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                                 yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                                 height=400, margin=dict(l=0, r=0, t=0, b=0))

    return bar_chart_fig, word_cloud_fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
    """
    while True:
        # Get the word counts from Redis
        print('11111')
        word_counts = r.hgetall('word_count')
        # Convert the byte strings to integers
        word_counts = {word.decode('utf-8'): int(count) for word, count in word_counts.items()}
        print('2222')
        # Convert the word counts to a pandas DataFrame and sort by count
        word_counts_df = pd.DataFrame(list(word_counts.items()), columns=['word', 'count'])
        word_counts_df = word_counts_df.sort_values(by='count', ascending=False)
        print(word_counts_df.head(10), '<---')
        time.sleep(30)
    """