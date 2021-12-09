import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import seaborn as sns
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.ticker as mtick
# %matplotlib inline

def app():
    pd.set_option('display.max_columns', 40)
    pd.set_option('display.max_rows', 100)

    # st.set_page_config(page_title="Supermarket Dashboard", 
    #                     page_icon=":bar_chart:", 
    #                     layout="wide")'
    # st.markdown(""" <style>
    #     #MainMenu {visibility: hidden;}
    #     footer {visibility: hidden;}
    #     </style> """, unsafe_allow_html=True)

    # --- Load Data From CSV ----
    @st.cache()
    def get_data_from_csv():
        df = pd.read_csv('data/supermarket_clean.csv')
        return df

    df = get_data_from_csv()

    # header
    st.header(":bar_chart: Supermarket Dashboard")
    st.markdown("----")

    ##### Create function for membership
    # @st.cache
    ##### Create function for membership
    df_average_gender = df.groupby(['Date','Gender'])['Total'].mean().unstack().reset_index()


    x_values = pd.date_range(start=pd.Timestamp('2018-01-01'), end=pd.Timestamp('2019-01-01'), freq='1 D')
    # making a random time series
    y_values = np.random.randn(len(x_values))
    # making color list
    # red if the day is saturday or sunday else green
    colors = ['red' if int(pd.Timestamp(d).weekday()) >= 5 else 'green' for d in x_values]
    fig = go.Figure()
    # for val in ['Female','Male']:
    fig.add_trace(go.Scatter(x=df_average_gender['Date'], 
                                y=df_average_gender['Female'], 
                                name='Female',
                                mode='lines+markers',
                                marker=dict(color = colors)
                )),
    fig.layout.update(title_text='Average customer daily purchasing based on Gender, green marker represent weekday and red marker represent weekend', hovermode='x')

    st.plotly_chart(fig, use_container_width=True)

    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    jenis = st.radio("Pilih Kasus ", ('Product Category','Payment Method'))
    col1, col2 = st.columns([2, 4])
    # jenis = st.radio("Pilih Kasus ", ('Product Category','Payment Method'))
    with col1:
        # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        # jenis = st.radio("Pilih Kasus ", ('Product Category','Payment Method'))
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
        

    # distribution by hour buying
    # Order for plotting categorical vars
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    kind = st.radio("Choose Case", ('Hour Range','Rating Range'))
    print("ck")
    # function generate barplot
    # Order for plotting categorical vars
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
        The two most frequent age bands are 20-30 
        and 30-40. In the early stages of our 
        exploratory analysis, we can already start
        to think about who our most important customers
        are and, importantly, how we might tailor our
        marketing activities or promotional offers based
        on customer segments.
        '''
                    , fontsize=12, fontweight='light', fontfamily='serif')

        ax.grid(axis='y', linestyle='-', alpha=0.4)   


        grid_y_ticks = np.arange(0, 250, 20) # y ticks, min, max, then step

        ax.set_yticks(grid_y_ticks)
        ax.set_axisbelow(True)

        # Axis labels

        plt.xlabel("Time banding", fontsize=12, fontweight='light', fontfamily='serif',loc='left',y=-1.5)


        print('cek')
        # thicken the bottom line if you want to
        plt.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

        import matplotlib.lines as lines
        l1 = lines.Line2D([1.05, 1.05], [0, 1.05], transform=fig.transFigure, figure=fig,color='black',lw=0.2)
        fig.lines.extend([l1])

        # st.set_option('deprecation.showPyplotGlobalUse', False)
        # if kind == 'Hour Range' :
        st.pyplot(fig)
        # if kind == 'Rating Range':
        # st.pyplot(bar_plot('Rating Range'))
    else :
        ab_order = ['3 ~ 5','5 ~ 7', '7 ~ 9', '9 ~ 10']
        color_map = ['#d4dddd' for _ in range(9)]
        color_map[2] = '#244747' 
        data = df['Rating Range'].value_counts()[ab_order]

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
        The two most frequent age bands are 20-30 
        and 30-40. In the early stages of our 
        exploratory analysis, we can already start
        to think about who our most important customers
        are and, importantly, how we might tailor our
        marketing activities or promotional offers based
        on customer segments.
        '''
                    , fontsize=12, fontweight='light', fontfamily='serif')

        ax.grid(axis='y', linestyle='-', alpha=0.4)   


        grid_y_ticks = np.arange(0, 350, 20) # y ticks, min, max, then step

        ax.set_yticks(grid_y_ticks)
        ax.set_axisbelow(True)

        # Axis labels

        plt.xlabel("Time banding", fontsize=12, fontweight='light', fontfamily='serif',loc='left',y=-1.5)


        print('cek')
        # thicken the bottom line if you want to
        plt.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

        import matplotlib.lines as lines
        l1 = lines.Line2D([1.05, 1.05], [0, 1.05], transform=fig.transFigure, figure=fig,color='black',lw=0.2)
        fig.lines.extend([l1])

        # st.set_option('deprecation.showPyplotGlobalUse', False)
        # if kind == 'Hour Range' :
        st.pyplot(fig)
        # if kind == 'Rating Range':
        # st.pyplot(bar_plot('Rating Range'))

        