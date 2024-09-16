import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO


# Function to create charts and tables
def create_charts(df, col_to_analyze, filter_col=None, filter_values=None):
    st.write(f"### Analysis of Column: {col_to_analyze}")

    # Filter data if needed
    if filter_col and filter_values:
        if df[filter_col].dtype == 'datetime64[ns]':
            if 'year' in filter_values:
                df = df[df[filter_col].dt.year.isin(filter_values['year'])]
            if 'month' in filter_values:
                df = df[df[filter_col].dt.month.isin(filter_values['month'])]
            if 'day' in filter_values:
                df = df[df[filter_col].dt.day.isin(filter_values['day'])]
        else:
            df = df[df[filter_col].isin(filter_values)]

    if col_to_analyze == 'All':
        for column in df.columns:
            if df[column].dtype == 'object':
                st.write(f"#### Bar and Pie Chart for {column}")
                if df[column].nunique() > 10:
                    top_values = df[column].value_counts().nlargest(10)
                    others_count = df[column].value_counts().iloc[10:].sum()
                    others = pd.Series(others_count, index=['Others'])
                    top_values = pd.concat([top_values, others])
                else:
                    top_values = df[column].value_counts()
                fig, axs = plt.subplots(1, 2, figsize=(14, 6))
                sns.barplot(x=top_values.index, y=top_values.values, ax=axs[0])
                axs[0].set_title(f"Bar Chart of {column}")
                axs[1].pie(top_values, labels=top_values.index, autopct='%1.1f%%', startangle=90)
                axs[1].set_title(f"Pie Chart of {column}")
                st.pyplot(fig)

                if pd.api.types.is_datetime64_any_dtype(df[column]):
                    st.write("##### Date and Time Analysis")
                    year_counts = df[column].dt.year.value_counts()
                    month_counts = df[column].dt.month.value_counts()
                    day_counts = df[column].dt.day.value_counts()

                    st.write("##### Year Counts")
                    st.write(year_counts)
                    st.write("##### Month Counts")
                    st.write(month_counts)
                    st.write("##### Day Counts")
                    st.write(day_counts)

            elif pd.api.types.is_numeric_dtype(df[column]):
                st.write(f"#### Line Chart for {column}")
                fig, ax = plt.subplots(figsize=(10, 5))
                df[column].plot(kind='line', ax=ax)
                ax.set_title(f"Line Chart of {column}")
                st.pyplot(fig)

            st.write(f"#### Table for {column}")
            st.write(df[column].value_counts().reset_index().rename(columns={'index': column, column: 'Count'}))

    else:
        if df[col_to_analyze].dtype == 'object':
            st.write(f"#### Bar and Pie Chart for {col_to_analyze}")
            if df[col_to_analyze].nunique() > 10:
                top_values = df[col_to_analyze].value_counts().nlargest(10)
                others_count = df[col_to_analyze].value_counts().iloc[10:].sum()
                others = pd.Series(others_count, index=['Others'])
                top_values = pd.concat([top_values, others])
            else:
                top_values = df[col_to_analyze].value_counts()
            fig, axs = plt.subplots(1, 2, figsize=(14, 6))
            sns.barplot(x=top_values.index, y=top_values.values, ax=axs[0])
            axs[0].set_title(f"Bar Chart of {col_to_analyze}")
            axs[1].pie(top_values, labels=top_values.index, autopct='%1.1f%%', startangle=90)
            axs[1].set_title(f"Pie Chart of {col_to_analyze}")
            st.pyplot(fig)

            if pd.api.types.is_datetime64_any_dtype(df[col_to_analyze]):
                st.write("##### Date and Time Analysis")
                year_counts = df[col_to_analyze].dt.year.value_counts()
                month_counts = df[col_to_analyze].dt.month.value_counts()
                day_counts = df[col_to_analyze].dt.day.value_counts()

                st.write("##### Year Counts")
                st.write(year_counts)
                st.write("##### Month Counts")
                st.write(month_counts)
                st.write("##### Day Counts")
                st.write(day_counts)

        elif pd.api.types.is_numeric_dtype(df[col_to_analyze]):
            st.write(f"#### Line Chart for {col_to_analyze}")
            fig, ax = plt.subplots(figsize=(10, 5))
            df[col_to_analyze].plot(kind='line', ax=ax)
            ax.set_title(f"Line Chart of {col_to_analyze}")
            st.pyplot(fig)

        st.write(f"#### Table for {col_to_analyze}")
        st.write(df[col_to_analyze].value_counts().reset_index().rename(columns={'index': col_to_analyze, col_to_analyze: 'Count'}))


def main():
    st.title('CSV Data Analyzer')

    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.write("Uploaded file is empty.")
            return

        st.write("### Dataset Overview")
        st.write(df.head())

        columns = list(df.columns) + ['All']
        col_to_analyze = st.selectbox("Select Column to Analyze", options=columns)

        filter_col = st.selectbox("Select Column to Filter", options=['None'] + list(df.columns))

        if filter_col != 'None':
            if pd.api.types.is_datetime64_any_dtype(df[filter_col]):
                filter_values = {
                    'year': st.multiselect("Select Years", options=df[filter_col].dt.year.unique()),
                    'month': st.multiselect("Select Months", options=df[filter_col].dt.month.unique()),
                    'day': st.multiselect("Select Days", options=df[filter_col].dt.day.unique())
                }
            else:
                filter_values = st.multiselect("Select Filter Values", options=df[filter_col].unique())
        else:
            filter_values = None

        st.write("### Analysis Dashboard")
        create_charts(df, col_to_analyze, filter_col if filter_col != 'None' else None, filter_values)

if __name__ == "__main__":
    main()
