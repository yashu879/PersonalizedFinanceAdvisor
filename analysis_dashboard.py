import pandas as pd
import numpy as np
import plotly.express as px
import panel as pn

# Read transactions_categorized.csv
df = pd.read_csv('transactions_categorized.csv')
# Add year and month columns
df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month
df['Month Name'] = pd.to_datetime(df['Date']).dt.strftime("%b")

def make_monthly_bar_chart(df, year, label):
    df = df[(df['Expense'] == label) & (df['Year'] == year)]
    total_by_month = (df.groupby(['Month', 'Month Name'])['Amount'].sum()
                        .to_frame()
                        .reset_index()
                        .sort_values(by='Month')  
                        .reset_index(drop=True))
    if label == "Expense":
        color_scale = px.colors.sequential.OrRd
    
    bar_fig = px.bar(total_by_month, x='Month Name', y='Amount', text_auto='.2s', title=label+" per month", color='Amount', color_continuous_scale=color_scale)
    # bar_fig.update_traces(marker_color='lightslategrey')
    
    return bar_fig


def make_pie_chart(df, year):
    # Filter the dataset for expense transactions
    sub_df = df[(df['Year'] == year)]

    color_scale = px.colors.qualitative.Set2
    
    pie_fig = px.pie(sub_df, values='Amount', names='Category', color_discrete_sequence = color_scale)
    pie_fig.update_traces(textposition='inside', direction ='clockwise', hole=0.3, textinfo="label+percent")

    total_expense = df[(df['Expense'] == 'Expense') & (df['Year'] == year)]['Amount'].sum() 
    

    total_text = "$ " + str(round(total_expense))

   

    pie_fig.update_layout(uniformtext_minsize=10, 
                        uniformtext_mode='hide',
                        
                        # Add annotations in the center of the donut.
                        annotations=[
                            dict(
                                text=total_text, 
                                # Square unit grid starting at bottom left of page
                                x=0.5, y=0.5, font_size=12,
                                # Hide the arrow that points to the [x,y] coordinate
                                showarrow=False
                            )
                        ]
                    )
    return pie_fig

unique_year = df['Year'].unique()
year_list =unique_year.tolist()

# Create tabs
tabs = pn.Tabs()

for curr in year_list:
    yr = str(curr)
    barchart = make_monthly_bar_chart(df, curr, 'Expense')
    piechart = make_pie_chart(df,curr)
    tabs.append((yr, pn.Column(pn.Row(barchart),
                               pn.Row(piechart))))
    
                       
 
tabs.show()