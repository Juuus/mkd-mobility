# Import packages
import numpy as np
import pandas as pd
import streamlit as st
#import plotly.express as px
import plotly.graph_objects as go



st.title("Measuring the Macedonian dream")

st.markdown("How much time does it take for Macedonian workers to improve their income status?")
st.markdown("By employing ideas and techniques from statistical mechanics, we can provide a disaggregated view on a worker's income timeline. Here we use data for Macedonia and estimate the time for an individual worker to change their initial income to a target income.")


st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")


# read the data
data = pd.read_excel('mkd_mfpt_results.xlsx')
# set the mfpt
mfpt_mean = data['mfpt_mean'].values
mfpt_ub = data['mfpt_ub'].values
mfpt_lb = data['mfpt_lb'].values
# get the years
years = data['years'].values
# get the starting percentiles
x0 = data['x0'].values
y =  data['y'].values

target_x0 = st.sidebar.slider(
    'Select initial income (in percentile)',
    1, 100, 40)
target_y = st.sidebar.slider(
    'Select target income (in percentile)',
    1, 100, 90)


x0_locs = np.where(x0 == target_x0)
y_locs = np.where(y == target_y)
locs = np.intersect1d(x0_locs,y_locs)
plot_mfpt_mean = mfpt_mean[locs]
plot_mfpt_ub = mfpt_ub[locs]
plot_mfpt_lb = mfpt_lb[locs]
years_loc = years[locs]


dikt = {"Year": list(years_loc), "Years to target" : list(plot_mfpt_mean), 
        "mfpt_ub" : list(plot_mfpt_ub), "mfpt_lb" : list(plot_mfpt_lb)}
df = pd.DataFrame(dikt)


#df["Upper bound"] = df["mfpt_ub"] - df["Years to target"]
#df["Lower bound"] = df["Years to target"] - df["mfpt_lb"]
#fig = px.scatter(df, x="Year", y="Years to target", 
 #                error_y="Upper bound", error_y_minus="Lower bound")
#st.plotly_chart(fig)


#st.line_chart(plot_data, x="Year", y="Years to target")


fig = go.Figure([
      go.Scatter(
          name='Estimate',
          x = years_loc,
          y= plot_mfpt_mean, 
          mode='lines+markers',  
          line=dict(color='royalblue', width=2),  
          marker=dict(size=10,color='royalblue',symbol='circle'),
          showlegend=False
    ),
    go.Scatter(
        name='Upper Bound',
        x = years,
        y = plot_mfpt_ub, 
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
    ),
    go.Scatter(
        name='Lower Bound',
        x = years,
        y = plot_mfpt_lb,
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False
    )
  ])
fig.update_layout(yaxis = dict(title="MFPT in (years)",
                 showgrid = True,gridcolor = "black", showline = False, showticklabels = True),
    xaxis = dict(title="Years",zeroline = True, showline = True,showticklabels = True,tickangle=0, showgrid = True),
    hovermode="x",
   # paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)')
fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

st.plotly_chart(fig)