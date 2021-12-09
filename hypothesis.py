import streamlit as st
import pandas as pd
from scipy import stats
import numpy as np
import plotly.figure_factory as ff
from plotly.offline import  iplot
import plotly.graph_objects as go

def app():
    @st.cache(allow_output_mutation=True)
    # in this part below we will load data and handling hyphotesis testing process and get result of hyphotesis
    # load data
    def get_data_from_csv():
        df = pd.read_csv('data/supermarket_clean.csv')
        return df

    df = get_data_from_csv()

    # convert date to date time 
    df['Date'] = pd.to_datetime(df['Date'])

    # get data for hyphotesis testing
    df_h = df[["Gender", "Total","Date"]]
    df_h = df_h.rename(columns = { "Total":"Total Spending" })

    # get two sample data for hyphotesis testing
    female = df_h[df_h['Gender'] == 'Female' ].groupby(['Date']).mean()
    male = df_h[df_h['Gender'] == 'Male' ].groupby(['Date']).mean()

    # get result of t-statistic and p-value 
    t_stat, p_val = stats.ttest_ind(female, male)

    # generate confidence interval with treshold 90%
    ci = stats.norm.interval(0.90, female['Total Spending'].mean(), female['Total Spending'].std())

    # generate female population to draw distribution later
    female_population = np.random.normal(female['Total Spending'].mean(),female['Total Spending'].std(),10000)
    male_population = np.random.normal(male['Total Spending'].mean(),male['Total Spending'].std(),10000)

    # get area of alternatife hyphotesis result
    alternatif_right = female_population.mean()+t_stat[0]*female_population.std()
    alternatif_left = female_population.mean()-t_stat[0]*female_population.std()

    # Title for page
    st.markdown("<h1 style='text-align: center;'>Hypothesis Test: Average Daily Purchases between Male and Female Customer</h1>", unsafe_allow_html=True)

    # part-1 explanation of hyphotesis
    st.header('Introduction')
    st.write('''At a glance, we can see that the average daily purchases in supermarket store between male and female customer is similar. 
            But, there's one unit difference between both of them. 
            So, before making any assumption, we have to make sure that the difference is statistically significant and is not happening by chance. 
            Therefore, we need to conduct hypothesis testing to prove our assumption.''')

    # part-2
    st.header('Hypothesis Statement')
    st.markdown('**Null Hypothesis**: There is ***no*** significant difference  between the average daily purchases of a male and female customer.')
    st.markdown('**Alternative Hypothesis**: There is a significant difference between the average daily purchases of a male and female customer')


    # methodology
    st.header('Methodology')
    st.write('Since we want to compare the average purchase between male and female, we will use t-test Independent. This methodology was chosen because we have two independent sample.')
    st.write('This Hypothesis testing will use level significance (α) 0.05, When the probability of the test is greater than 0.05, we can accept the Null hypothesis')
    
    # t-test 
    st.header('''T-test Independent''')
    st.write('After conducting  t-test independent, we get t-statistic and p-value as follows:')
    st.markdown('- p-value :`0.14580477598170313`')
    st.markdown('- t-statistics: `1.4609767778104268`')
    st.markdown('- Confidence Interval: `(148.32277848092485, 515.1897254064801)` ')
    st.write('P-value is greater than the level of significance that we have set (0.05).')

    #GRAPHIC OF HYPOTHESIS TESTING 
    hist_data = [female_population,male_population]
    group_labels = ['Female Population','Male Population']

    fig = ff.create_distplot(hist_data, group_labels, bin_size=5)


    # add line in mean of populations
    fig.add_trace(go.Scatter(x=[female['Total Spending'].mean(),female['Total Spending'].mean()], 
                            y=[0,0.004], 
                            mode='lines', 
                            line=dict(color='blue', width=2, dash='dash'),
                            name='Female Average Purchased a Day *Pop'))
    fig.add_trace(go.Scatter(x=[male['Total Spending'].mean(),male['Total Spending'].mean()], 
                            y=[0,0.004], 
                            mode='lines', 
                            line=dict(color='red', width=2, dash='dash'),
                            name='Male Average Spending a Day *Pop'))

    # add line in alternative hyphothesis
    fig.add_trace(go.Scatter(x=[alternatif_right,
                                alternatif_right], 
                            y=[0,0.004], 
                            mode='lines', 
                            line=dict(color='black', width=2, dash='dash'),
                            name = 'Alternative Hypothesis'))

    fig.add_trace(go.Scatter(x=[alternatif_left,
                                alternatif_left], 
                            y=[0,0.004], 
                            mode='lines', 
                            line=dict(color='black', width=2, dash='dash'),
                            name = 'Alternative Hypothesis'))

    # add line in CI part
    fig.add_trace(go.Scatter(x=[ci[1],ci[1]], 
                            y=[0,0.004], 
                            mode='lines', 
                            line=dict(color='green', width=2, dash='dash'),
                            name='Confidence Interval Treshold 90%'))

    fig.add_trace(go.Scatter(x=[ci[0],ci[0]], 
                            y=[0,0.004], 
                            mode='lines', 
                            line=dict(color='green', width=2, dash='dash'),
                            name='Confidence Interval Treshold 90%'))


    st.plotly_chart(fig, use_container_width=True)

    # Conclusion
    st.header('Conclusion')
    st.markdown('- Decision : fail to reject null hyphotesis ')
    st.write('''From the test, we get result p-value is greater than level of significance. 
    We fail to reject null hypothesis. Therefore, we can conclude that There is ***no*** significant difference  between the average daily purchases of a male and female customer.
    ''')