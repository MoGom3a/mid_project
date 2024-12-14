
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st
st.set_page_config(layout='wide')
df = pd.read_excel('data.xlsx')
def fun(x):
    if x.startswith('F'):
        x = "Female"
    else:
        x = "Male"
        
    return x
df['Sex'] = df['Sex'].apply(fun)
df['Price'] = df['Item Price'].apply(lambda x : x.split(' ')[0])
df['Currency'] = df['Item Price'].apply(lambda x : x.split(' ')[1])
df['Price']=df['Price'].astype('float')
df['Sales'] = df['Price'] * df['Items per Ticket']
df.drop(['Item Price'], axis = 1, inplace = True)
def page1():
    st.title('Gender Based Analysis')
    fig = px.pie(df,names='Sex', title = 'Total Gender Distribution',color = 'Sex', color_discrete_map={
    'Male': 'darkblue',
    'Female': 'pink'})
    st.plotly_chart(fig , key = '0')

    tab1 , tab2 = st.tabs(['histogram' , 'pie'])

    with tab1 :
        fig = px.histogram(data_frame = df, x = 'City', color = 'Sex', text_auto = True, color_discrete_map={
        'Male' : 'cornflowerblue',
        'Female' : 'deeppink'}, title = 'City Gender Distribution')
        st.plotly_chart(fig , key = '1')

    with tab2 :
        city = st.sidebar.selectbox('Select City' , options=df['City'].unique())
        msk = df['City'] == city
        fig = px.pie(data_frame = df[msk],names='Sex', title = 'Gender Share for City of choice' , 
               facet_col = 'City' )
        st.plotly_chart(fig , key = '5')

        
def page2():
    st.title('Payment Method Analysis')
    fig = px.pie(df,names='Payment Type',title = 'Total Payment Method Distribution', 
                 color_discrete_map={
                     'card payment' : 'navy',
                     'cash payment' : 'deeppink'})
    st.plotly_chart(fig , key = '0')

    tab1 , tab2 = st.tabs(['histogram' , 'pie'])

    with tab1 :
        fig = px.histogram(df, x = 'City', text_auto = True, color_discrete_map={
            'card payment' : 'cornflowerblue',
            'cash payment' : 'deeppink'},title = 'Payment Method over Cities')
        st.plotly_chart(fig , key = '1')

    with tab2 :
        city = st.sidebar.selectbox('Select City' , options=df['City'].unique())
        msk = df['City'] == city
        fig =px.pie(data_frame = df[msk],names='Payment Type', title = 'Paymenth Method for each City' , facet_col = 'City')
        st.plotly_chart(fig , key = '5')

        
def page3():
    st.title('Invoices Distribution per month')
    
    st.header('Invoice Percentage per Month'.title() ,divider = True )
    df['Invoice Month'] = df['Invoice Date'].dt.month
    fig =px.pie(df, names= 'Invoice Month')
    st.plotly_chart(fig , key = '4')
    
    st.header('Payment Type Percentage for each Month'.title() ,divider = True )
    fig =px.pie(df,names='Payment Type', facet_col = 'Invoice Month')
    st.plotly_chart(fig , key = '5')
    
    st.header('Gender Share each Month'.title() ,divider = True )
    fig =px.pie(df,names='Sex', facet_col = 'Invoice Month')
    st.plotly_chart(fig , key = '6')
    

    
def page4():
    st.title('Item Categories Percentage')
    
    st.header('Item Category per Month'.title() ,divider = True )
    fig =px.pie(df,names='Item Category')
    st.plotly_chart(fig , key = '7')
    
    st.header('Payment Type Percentage per Category'.title() ,divider = True )
    fig =px.pie(df,names='Payment Type', facet_col = 'Item Category')
    st.plotly_chart(fig , key = '8')
    
    st.header('Gender share for each Item Category'.title() ,divider = True )
    fig =px.pie(df,names='Sex', facet_col = 'Item Category', color_discrete_map={
        'Male' : ['darkgray'],
        'Female' : ['salmon']
    })
    st.plotly_chart(fig , key = '9')
    

def page5():
    st.title('Sales Statistics')
    
    st.header('Total Sales for each City (sorted)'.title() ,divider = True )
    city_sales_order = df.groupby('City')['Sales'].sum().sort_values(ascending=False).index.tolist()
    fig =px.histogram(df, x = 'City', y = 'Sales', category_orders={"City": city_sales_order},
                      color_discrete_sequence=['navy'])
    st.plotly_chart(fig , key = '10')
    
    
    st.header('Total Sales for each Month'.title() ,divider = True )
    df['Invoice Month'] = df['Invoice Date'].dt.month
    month_sales_df = df.groupby('Invoice Month')['Sales'].sum().reset_index()
    fig =px.line(month_sales_df, x = 'Invoice Month', y = 'Sales')
    st.plotly_chart(fig , key = '11')
    
    st.header('Total Sales for each Item Category'.title() ,divider = True )
    ic_sales_df = df.groupby('Item Category')['Sales'].sum().reset_index()
    ic_sales_order = df.groupby('Item Category')['Sales'].sum().sort_values(ascending=False).index.tolist()
    fig =px.histogram(ic_sales_df, x = 'Item Category', y = 'Sales',category_orders={"Item Category": ic_sales_order},
                      color_discrete_sequence=['navy'])
    st.plotly_chart(fig , key = '12')
    
    st.header('Total Sales for each Channel'.title() ,divider = True )
    fig = px.histogram(df, x = 'Channel', y = 'Sales',color_discrete_sequence=['navy'])
    st.plotly_chart(fig , key = '13')
    

    
def page6():
    st.title('Top Five Ranks')
    rank = st.selectbox('Select Top Five' , options= ['Store', 'Product', 'Item Category' ] )
    if rank == 'Store':
        store_sales_order = df.groupby('Store Name')['Sales'].sum().nlargest(5).index.tolist()
        top_5_stores = df[df['Store Name'].isin(store_sales_order)]
        fig = px.histogram(top_5_stores, x = 'Store Name', y = 'Sales', category_orders={"Store Name": store_sales_order},
                           title = 'Top Five Stores in Sales (sorted)',color_discrete_sequence=['navy'])
        st.plotly_chart(fig , key = '14')
    elif rank == 'Product':
        pn_sales_order = df.groupby('Product Name')['Sales'].sum().nlargest(5).index.tolist()
        top_5_pns = df[df['Product Name'].isin(pn_sales_order)]
        fig = px.histogram(top_5_pns, x = 'Product Name', y = 'Sales', category_orders={"Product Name": pn_sales_order},
             title = 'Top Five Products in Sales (sorted)',color_discrete_sequence=['navy'])
        st.plotly_chart(fig , key = '15')
    else:
        df['Invoice Day'] = df['Invoice Date'].dt.day
        day_sales_order = df.groupby('Invoice Day')['Sales'].sum().nlargest(5).index.tolist()
        top_5_days = df[df['Invoice Day'].isin(day_sales_order)]
        fig = px.pie(top_5_days, names = 'Invoice Day',title = 'Top Five Days in Sales (sorted)',
               color_discrete_sequence=['navy'])
        st.plotly_chart(fig , key = '16')
        
pgs = {
    'Gender Analysis' : page1,
    'Payment Analysis' : page2,
    'Months Analysis' : page3,
    'Category Analysis' : page4,
    'Salese Analysis' : page5,
    'Achievements' : page6
}
pg = st.sidebar.radio('Navigate Pages ' ,options= pgs.keys())
pgs[pg]()
