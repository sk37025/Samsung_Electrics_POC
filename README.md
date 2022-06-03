# Samsung_Electrics_POC
프로젝트 목적 : 삼성전기 POC를 위한 빠르게 프로토타입 만들기 

## Streamlit은 무엇인가??? 

:point_right:  __Streamlit__은 파이썬 기반으로 웹 어플리케이션을 개발하는 오픈소스입니다. 


## 왜 Streamlit을 사용하였는지???
본 프로젝트에서는 간단한 데이터 Visualization 그리고 POC를 위한 프로토타입 모델 시연이 목적이었기에 본 오픈소스를 사용하였습니다. 

## Streamlit 설치하고 사용하기 (공식 홈페이지 샘플 코드) 
Streamlit 설치는 간단하게 아래의 구문을 통해서 이루어집니다. 
```bash
pip3 install streamlit 
```

설치를 진행한 이후에는 파이썬 파일을 작성하여 프로토 타입을 위한 파이썬 파일을 작성합니다. 
```python
import streamlit as st 
import pandas as pd 
import numpy as np 

st.title("Uber pickups in NYC")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(n_rows):
    data = pd.read_csv(DATA_URL, nrows= n_rows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
	
data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

```
코드 작성이 끝난 이후에는 Streamlit을 실행하면 빠르게 프로토타입을 확인하실 수 있습니다. 

```bash 
streamlit run sample_code.py
```

본 프로젝트의 경우 Pipfile을 통해 배포되었기에 아래의 구문을 통해서 환경을 설정할 수 있습니다.
```bash 
pipenv install
```

그리고 가상환경을 실행할 수 있습니다.
```bash
pipenv shell
```

가상환경 실행 후에는 Streamlit을 통해서 만든 프로토타입을 확인하실 수 있습니다.
```bash 
streamlit run deploy.py
```

감사합니다.



