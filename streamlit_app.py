import pandas as pd
import plotly.data as pldata
import plotly.express as px
import streamlit as st

st.title('Stock Index Change Dashboard')
st.markdown("Shows **stocks**, *their indexes change* through _time_")
st.set_page_config(layout="wide")

stocks_df = pldata.stocks(return_type='pandas', indexed=False, datetimes=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Stock Index by Company')

    selected_options = st.multiselect('Select Stock', [symbol for symbol in stocks_df.columns if symbol != "date"],
                                      stocks_df.columns[1])
    st.metric('Tickers name', f"{", ".join(so for so in selected_options)}")

    fig_line_stocks = px.line(stocks_df, "date", y=selected_options,
                              title=f"{", ".join(so for so in selected_options)} Price")
    fig_line_stocks.update_layout(xaxis_title="Date")
    fig_line_stocks.update_layout(yaxis_title="Index change")
    st.plotly_chart(fig_line_stocks)
with col2:
    st.subheader('Stock Index change on specific date')

    # Cast timestamps from df date column to datetime to be able to compare with datepicker result
    stocks_df['date'] = pd.to_datetime(stocks_df['date']).dt.date

    selected_date = st.date_input('Select a date', value=stocks_df['date'][0], min_value=min(stocks_df['date']),
                                  max_value=max(stocks_df['date']))
    final_date = None
    if selected_date in stocks_df['date'].values:
        final_date = selected_date
    else:
        st.error(f"Date {selected_date} not found")
        valid_date = st.selectbox(
            "Please select a date that exists from the list:",
            options=stocks_df['date']
        )
        print(f"valid_date = {valid_date}")

        final_date = valid_date

    selected_row = stocks_df[stocks_df['date'] == final_date]
    if not selected_row.empty:
        # Convert selected_row series to df with proper columns to be able to use in bar chart
        data = selected_row.drop(columns='date').iloc[0]
        bar_df = data.reset_index()
        bar_df.columns = ['Stock', 'Normalized Price']

        fig_bar_stocks = px.bar(bar_df, x='Stock', y='Normalized Price', title=f"Stock Index change on {selected_date}",
                                barmode='group')

        st.plotly_chart(fig_bar_stocks)
