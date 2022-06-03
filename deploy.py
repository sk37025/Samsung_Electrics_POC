import streamlit as st 
import numpy as np
import time 
import pandas as pd 
import altair as alt 

progress_bar = st.progress(0)
status_text = st.empty()

# Create Select Box 
simple_select = st.selectbox("진동기 타입 선택.",["L_DSF_01","L_EF_04","L_SF_04","R_EF_05"])
def change_label_into_name(x):
    if x ==0:
        return "정상"
    elif x==1:
        return "베어링 불량"
    elif x==2:
        return "회전체 불평형"
    elif x==3:
        return "축정렬 불량"
    elif x==4:
        return "벨트 느슨함"

@st.cache
def load_data(str_):
    data = pd.read_csv("./data/{}_total_predict.csv".format(str_),index_col=0)
    # data.reset_index(inplace=True)
    data["predicted"] = data['predicted'].apply(lambda x:change_label_into_name(x) )
    data['target'] = data['target'].apply(lambda x: change_label_into_name(x))
    return data.reset_index(drop=False)

if simple_select:
    df_load_state = st.text("Loading data ...")
    df = load_data(simple_select)
    st.write(df.head())
    df_load_state.text("Done!")

st.write(df['index'].max(),df.shape[0])

lines = alt.Chart(df).mark_line().encode(
    x = alt.X('0:Q',axis = alt.Axis(title='timestamp')),
    y=alt.Y('1:Q',axis=alt.Axis(title='value'))
).properties(width = 800, height = 500)


domain = ['정상','베어링 불량','회전체 불평형','축정렬 불량','벨트 느슨함']
range_ = ['steelblue','red', 'chartreuse', '#D35400', '#7D3C98']

def plot_animation(df,title): # filled=True, size=5.0
    
    lines = alt.Chart(df).mark_line(point=True).encode(
       x=alt.X('index:Q', axis=alt.Axis(title='timestamp')),
       y=alt.Y('value:Q',axis=alt.Axis(title='value')),
       color = alt.Color('target',scale = alt.Scale(domain= domain, range = range_)),
       strokeWidth = alt.value(1) 
     ).properties(
        title = title,
       width=800,
       height=500
     ) 
    lines.configure_title(fontSize = 16,color="gray",align = "left",baseline = "bottom")
    return lines


N = df.shape[0] # number of elements in the dataframe
burst = 1       # number of elements (months) to add to the plot
size = burst

line_plot = st.altair_chart(lines)
start_btn = st.button("Start")

if start_btn:
    for i in range(0,N,1):
      if size>300:
        step_df = df.iloc[size-300:size]
      else:
        step_df = df.iloc[0:size]
      predicted_proba = 12000*((i//12000)+1)-1
      title= "predict probability {} : {} %".format(df.loc[predicted_proba,"predicted"],df.loc[predicted_proba,"predicted_proba"]) 
      lines = plot_animation(step_df,title)
      line_plot = line_plot.altair_chart(lines)
    #   st.text(predicted_proba)
    #   st.text(df.iloc[predicted_proba-5:predicted_proba+5,:])
    #   if df.loc[12000*((i//12000)+1)+1,"predicted"] != "정상":
    #     st.text("{}일 가능성은 {:.2f}".format(df.loc[12000*((i//12000)+1)+1,"predicted"],df.loc[12000*((i//12000)+1)+1,"predicted_proba"]))
    #   else:
    #     st.text("정상입니다")
    #   st.empty()
      size = i+burst
      if size >= N: 
         size = N - 1
      time.sleep(1)
