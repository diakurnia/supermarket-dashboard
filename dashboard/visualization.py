import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import numpy as np
import plotly.express as px
import matplotlib.ticker as mtick
from textwrap import wrap
# %matplotlib inline

def app():
    pd.set_option('display.max_columns', 40)
    pd.set_option('display.max_rows', 100)

   
    # --- Load Data From CSV ----
    fig = plt.figure(figsize=(6,3),dpi=150)
    gs = fig.add_gridspec(1, 1)
    gs.update(wspace=0.2, hspace=0.4)
    ax0 = fig.add_subplot(gs[0, 0])

    background_color = "#fafafa"
    fig.patch.set_facecolor(background_color) # figure background color
    ax0.set_facecolor(background_color) 

    ax0.text(1.167,0.85,"Customer Analysist Dashboard in Q1",color='#323232',fontsize=28, fontweight='bold', fontfamily='monospace',ha='center')
    ax0.text(1.13,-0.35,"stand-out facts",color='lightgray',fontsize=28, fontweight='bold', fontfamily='monospace',ha='center')

    ax0.text(0,0.4,"$400",color='#009473',fontsize=25, fontweight='bold', fontfamily='monospace',ha='center')
    ax0.text(0,0.1,"Average Spending",color='gray',fontsize=15, fontfamily='monospace',ha='center')

    ax0.text(0.77,0.4,"7 of top 10",color='#009473',fontsize=25, fontweight='bold', fontfamily='monospace',ha='center')
    ax0.text(0.75,0.1,"Average Rating",color='gray',fontsize=15, fontfamily='monospace',ha='center')

    ax0.text(1.5,0.4,"5 - 7 P.M",color='#009473',fontsize=25, fontweight='bold', fontfamily='monospace',ha='center')
    ax0.text(1.5,0.1,"Peak Hour",color='gray',fontsize=15, fontfamily='monospace',ha='center')

    ax0.text(2.25,0.4,"E-wallet",color='#009473',fontsize=25, fontweight='bold', fontfamily='monospace',ha='center')
    ax0.text(2.25,0.1,"Most Payment",color='gray',fontsize=15, fontfamily='monospace',ha='center')

    ax0.set_yticklabels('')
    ax0.set_xticklabels('')
    ax0.tick_params(axis='both',length=0)

    for s in ['top','right','left','bottom']:
        ax0.spines[s].set_visible(False)
        
    import matplotlib.lines as lines
    l1 = lines.Line2D([0.15, 1.95], [0.67, 0.67], transform=fig.transFigure, figure=fig,color = 'gray', linestyle='-',linewidth = 1.1, alpha = .5)
    fig.lines.extend([l1])
    l2 = lines.Line2D([0.15, 1.95], [0.07, 0.07], transform=fig.transFigure, figure=fig,color = 'gray', linestyle='-',linewidth = 1.1, alpha = .5)
    fig.lines.extend([l2])
        
    st.pyplot(fig)
    @st.cache()
    def get_data_from_csv():
        df = pd.read_csv('data/supermarket_clean.csv')
        return df

    df = get_data_from_csv()

    # header
    # st.header(":bar_chart: Supermarket Dashboard")
    st.markdown("----")

    ##### Create function for membership
    # @st.cache
    ##### Create function for membership
    df_average_gender = df.groupby(['Date','Gender'])['Total'].mean().unstack().reset_index()
    # title_one = 'Average customer daily purchasing based on Gender'
    title_two = 'green marker represent weekday and red marker represent weekend'
    y_title= 'Average $'

    line_kind = st.radio("Choose Data ", ('All','Male','Female'))
    x_values = pd.date_range(start=pd.Timestamp('2018-01-01'), end=pd.Timestamp('2019-01-01'), freq='1 D')

    # making color list
    # red if the day is saturday or sunday else green
    colors = ['red' if int(pd.Timestamp(d).weekday()) >= 5 else 'black' for d in x_values]
    fig = go.Figure()
    # for val in ['Female','Male']:
    if line_kind == 'Female' or line_kind == 'All':
        title_one = 'Average Female customer daily purchasing'
        fig.add_trace(go.Scatter(x=df_average_gender['Date'], 
                                    y=df_average_gender['Female'], 
                                    name='Female',
                                    mode='lines+markers',
                                    marker=dict(color = colors),
                                    line = dict(color = '#244747',
                                    )
                    )),
        
        fig.update_layout(
            title=f'<b>{"<br>".join(wrap(title_one, 70))}</b><br><sub>{title_two}</sub>', # Passing the name of the chart
            xaxis_title='', # Set the name of the x-axis
            yaxis_title=y_title, # Set the name of the y-axis
            plot_bgcolor='rgba(0,0,0,0)', # Setting the background color
            hovermode='x', # Using the x-axis values for the records
            # Setting the legend parameters
            legend_orientation='h',
            # Setting parameters for the text
            font=dict(
                family='Arials',
                size=13, 
                color='black'
            )
        )
    if line_kind == 'Male':
        title_one = 'Average male customer daily purchasing'
        fig.add_trace(go.Scatter(x=df_average_gender['Date'], 
                                    y=df_average_gender['Male'], 
                                    name='Male',
                                    mode='lines+markers',
                                    marker=dict(color = colors),
                                    line = dict(color = '#244747',
                                    )
                    )),
        
        fig.update_layout(
            title=f'<b>{"<br>".join(wrap(title_one, 70))}</b><br><sub>{title_two}</sub>', # Passing the name of the chart
            xaxis_title='', # Set the name of the x-axis
            yaxis_title=y_title, # Set the name of the y-axis
            plot_bgcolor='rgba(0,0,0,0)', # Setting the background color
            hovermode='x', # Using the x-axis values for the records
            # Setting the legend parameters
            legend_orientation='h',
            # Setting parameters for the text
            font=dict(
                family='Arials',
                size=13, 
                color='black'
            )
        )
    st.plotly_chart(fig, use_container_width=True)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    jenis = st.radio("Choose Data ", ('Product Category','Payment Method'))
    col1, col2 = st.columns([2, 4])
    with col1:
        if jenis == 'Product Category':
            data_pie =  df.groupby(['Product Category'])['Invoice ID'].count().reset_index().rename(columns = {'Invoice ID':'Total'})
            fig_category =  px.pie(data_pie, values='Total', 
                        names='Product Category', color='Product Category', 
                        color_discrete_sequence=px.colors.sequential.Teal)
            fig_category.layout.update(showlegend=False) 
            st.plotly_chart(fig_category)
        if jenis == 'Payment Method':
            data_pie =  df.groupby(['Payment'])['Invoice ID'].count().reset_index().rename(columns = {'Invoice ID':'Total'})
            fig_category =  px.pie(data_pie, values='Total', 
                        names='Payment', color='Payment', 
                        color_discrete_sequence=px.colors.sequential.Teal)
            fig_category.layout.update(showlegend=False) 
            st.plotly_chart(fig_category, use_container_width=True)

    with col2:
        # function to generate percentage by distribution
        def percentage_distribution(column, value, data1, data2):
            #aggregate function to generate new dataframe
            data_cg =  df.groupby([column,value]).size().unstack()
            data_cg['sum'] = data_cg.sum(axis=1)
            data_cg_ratio = (data_cg.T / data_cg['sum']).T[[data1, data2]][::-1]
            
            fig, ax = plt.subplots(1,1,figsize=(12, 6),)

            ax.barh(data_cg_ratio.index, data_cg_ratio[data1], 
                    color='#244247', alpha=0.7, label=data1)
            ax.barh(data_cg_ratio.index, data_cg_ratio[data2], left=data_cg_ratio[data1], 
                    color='#91b8bd', alpha=0.7, label=data2)


            ax.set_xlim(0, 1)
            ax.set_xticks([])
            ax.set_yticklabels((data_cg_ratio.index), fontfamily='serif', fontsize=11)


            # male percentage
            for i in data_cg_ratio.index:
                ax.annotate(f"{data_cg_ratio[data1][i]*100:.3}%", 
                            xy=(data_cg_ratio[data1][i]/2, i),
                            va = 'center', ha='center',fontsize=12, fontweight='light', fontfamily='serif',
                            color='white')

            for i in data_cg_ratio.index:
                ax.annotate(f"{data_cg_ratio[data2][i]*100:.3}%", 
                            xy=(data_cg_ratio[data1][i]+data_cg_ratio[data2][i]/2, i),
                            va = 'center', ha='center',fontsize=12, fontweight='light', fontfamily='serif',
                            color='#244247')

            if column == 'Product Category':
                fig.text(0.129, 0.98, 'Gender distribution by Product Category', fontsize=15, fontweight='bold', fontfamily='serif')   
                fig.text(0.129, 0.9, 
                        '''
                We find no significance difference between male and female in purchase every category,
                But we find something interesting in category Health and Beauty, male more dominant than female?''' , fontsize=12,fontfamily='serif')  
            if column == 'Payment':
                fig.text(0.129, 0.98, 'Gender distribution by Payment', fontsize=15, fontweight='bold', fontfamily='serif')   
                fig.text(0.129, 0.9, 
                        '''
                We see that Male more prefer to use E-wallet than Females
                ''' , fontsize=12,fontfamily='serif') 

            for s in ['top', 'left', 'right', 'bottom']:
                ax.spines[s].set_visible(False)

            ax.legend().set_visible(False)

            fig.text(0.77,0.98,data1, fontweight="bold", fontfamily='serif', fontsize=15, color='#244747')
            fig.text(0.819,0.98,"|", fontweight="bold", fontfamily='serif', fontsize=15, color='black')
            fig.text(0.827,0.98,data2, fontweight="bold", fontfamily='serif', fontsize=15, color='#0e7687' )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        if jenis == 'Product Category' :
            st.pyplot(percentage_distribution('Product Category','Gender','Male','Female'))
        if jenis == 'Payment Method':
            st.pyplot(percentage_distribution('Payment','Gender','Male','Female'))
        

    # distribution by hour buying or rating service
    # Order for plotting categorical vars
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    kind = st.radio("Choose Case", ('Hour Range','Rating Range'))
    if kind == 'Hour Range' :
        ab_order = ['9 ~ 11', '11 ~ 13', '13 ~ 15','15 ~ 17', '17 ~ 19', '19 ~ 21']
        color_map = ['#d4dddd' for _ in range(9)]
        color_map[4] = '#244747' 
        data = df['Hour Range'].value_counts()[ab_order]

        fig, ax = plt.subplots(1,1, figsize=(9, 6))
        ax.bar(data.index, data, width=0.5, 
                edgecolor='darkgray',
                linewidth=0.6,color=color_map)

        #annotations
        for i in data.index:
            ax.annotate(f"{data[i]}", 
                            xy=(i, data[i] + 3), #i like to change this to roughly 5% of the highest cat
                            va = 'center', ha='center',fontweight='light', fontfamily='serif')

        for s in ['top', 'left', 'right']:
            ax.spines[s].set_visible(False)

        ax.set_xticklabels(data.index, fontfamily='serif', rotation=0)

        # Title and sub-title

        fig.text(0.09, 1, 'Distribution by Time Buying', fontsize=20, fontweight='bold', fontfamily='serif')
        fig.text(0.09, 0.95, 'The two most numerous age bands have been highlighted.', fontsize=12, fontweight='light', fontfamily='serif')

        fig.text(1.185, 1.01, 'Insight', fontsize=20, fontweight='bold', fontfamily='serif')

        fig.text(1.185, 0.715, '''
        The most frequent time bands are 17-19 . 
        As we know, this time is finish working hour time.
        From this result, we get information that 5 - 7 p.m is 
        peak season
        '''
                    , fontsize=12, fontweight='light', fontfamily='serif')

        ax.grid(axis='y', linestyle='-', alpha=0.4)   


        grid_y_ticks = np.arange(0, 250, 20) # y ticks, min, max, then step

        ax.set_yticks(grid_y_ticks)
        ax.set_axisbelow(True)

        # Axis labels

        plt.xlabel("Time Range", fontsize=12, fontweight='light', fontfamily='serif',loc='left',y=-1.5)

        plt.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

        import matplotlib.lines as lines
        l1 = lines.Line2D([1.05, 1.05], [0, 1.05], transform=fig.transFigure, figure=fig,color='black',lw=0.2)
        fig.lines.extend([l1])

        st.pyplot(fig)
      
    else :
        ab_order = ['3 ~ 5','5 ~ 7', '7 ~ 9', '9 ~ 10']
        color_map = ['#d4dddd' for _ in range(9)]
        color_map[1] = '#244747' 
        data = df['Rating Range'].value_counts()[ab_order]

        fig, ax = plt.subplots(1,1, figsize=(9, 6))
        ax.bar(data.index, data, width=0.5, 
                edgecolor='darkgray',
                linewidth=0.6,color=color_map)

        #annotations
        for i in data.index:
            ax.annotate(f"{data[i]}", 
                            xy=(i, data[i] + 3), 
                            va = 'center', ha='center',fontweight='light', fontfamily='serif')

        for s in ['top', 'left', 'right']:
            ax.spines[s].set_visible(False)

        ax.set_xticklabels(data.index, fontfamily='serif', rotation=0)

        # Title and sub-title

        fig.text(0.09, 1, 'Distribution by Rating of Supermarket service', fontsize=20, fontweight='bold', fontfamily='serif')
        fig.text(0.09, 0.95, 'The two most numerous age bands have been highlighted.', fontsize=12, fontweight='light', fontfamily='serif')

        fig.text(1.185, 1.01, 'Insight', fontsize=20, fontweight='bold', fontfamily='serif')

        fig.text(1.185, 0.715, '''
        The  most frequent rating bands are 5-7. This value is relevant to the result of exploratory data analysis
        average rating is 7. With this result we can make conclusion that customer satisfied with customer service in supermarket
        '''
                    , fontsize=12, fontweight='light', fontfamily='serif')

        ax.grid(axis='y', linestyle='-', alpha=0.4)   


        grid_y_ticks = np.arange(0, 350, 20) # y ticks, min, max, then step

        ax.set_yticks(grid_y_ticks)
        ax.set_axisbelow(True)

        # Axis labels

        plt.xlabel("Rating Range", fontsize=12, fontweight='light', fontfamily='serif',loc='left',y=-1.5)


        print('cek')
        # thicken the bottom line if you want to
        plt.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

        import matplotlib.lines as lines
        l1 = lines.Line2D([1.05, 1.05], [0, 1.05], transform=fig.transFigure, figure=fig,color='black',lw=0.2)
        fig.lines.extend([l1])

        st.pyplot(fig)
       

        