import os.path
import random
import streamlit as st
import pandas
import pandas as pd
import pickle


m3u_filepaths_file = 'playlists/streamlit.m3u8'
ESSENTIA_ANALYSIS_PATH = 'data/features.csv'
with open(ESSENTIA_ANALYSIS_PATH,'rb') as f:
	data = pd.read_csv(f)
audio_analysis = data

st.dataframe(audio_analysis)
st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
audio_analysis_styles = audio_analysis["style"].unique()
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write('## 🔍 Select')
st.write('### By style')
st.write('Style activation statistics:')
st.write(audio_analysis.describe())

style_select = st.multiselect('Select by style activations:', audio_analysis_styles)
if style_select:
    st.write('Select tracks with `{style_select}` styles.')

st.write('## Select Tempo⏲️')
tempo_select_range = st.slider('Select a range', 60,185, (60,185))
st.write("You selected the range:", tempo_select_range)

st.write('## Select Voice or instrument')
vi_checkbox = st.checkbox('Select voice!')
if vi_checkbox:
    st.write('Voice is selected!🎤👄')
else:
    st.write('Instrument is selected!🎻🎺')
    
st.write('## Select Danceability🕺🏻💃🪩')
danceability_select_range = st.slider('Select a range', 0,3, (0,3))
st.write("You selected the range:", danceability_select_range)

st.write('## Select Arousal')
arousal_select_range = st.slider('Select a range', 1,9, (1,9))
st.write("You selected the range:", arousal_select_range)

st.write('## Select valence')
valence_select_range = st.slider('Select a range', 1,8, (1,8))
st.write("You selected the range:", valence_select_range)

st.write('## 🔀 Post-process')
max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
shuffle = st.checkbox('Random shuffle')

if st.button("RUN"):
    st.write('## 🔊 Results')
    result=audio_analysis.loc[(audio_analysis['tempo'] >= tempo_select_range[0]) & (audio_analysis['tempo'] <= tempo_select_range[1])]
    result=result.loc[(result['danceability'] >= danceability_select_range[0]) & (result['danceability'] <= danceability_select_range[1])]
    result = result.loc[(result["arousal"] >= arousal_select_range[0]) & (result["arousal"] <= arousal_select_range[1])]
    result = result.loc[(result["valence"] >= valence_select_range[0]) & (result["valence"] <= valence_select_range[1])]
    if vi_checkbox:
        result = result.loc[result["instrumentalvoice"] == "voice"]
    else:
        result = result.loc[result["instrumentalvoice"] == "instrumental"]
    if style_select:
        result = result.loc[result["style"].isin(style_select)]
    audio_analysis = result
    mp3s = list(audio_analysis.index)
    if max_tracks:
        mp3s = mp3s[:max_tracks]
        st.write('Using top', len(mp3s), 'tracks from the results.')

    if shuffle:
        random.shuffle(mp3s)
        st.write('Applied random shuffle.')

    # Store the M3U8 playlist.
    with open(m3u_filepaths_file, 'w') as f:
        # Modify relative mp3 paths to make them accessible from the playlist folder.
        mp3_paths = [os.path.join('..', mp3) for mp3 in mp3s]
        f.write('\n'.join(mp3_paths))
        st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

    st.write('Audio previews for the first 10 results:')
    for mp3 in mp3s[:10]:
        st.audio(mp3, format="audio/mp3", start_time=0)
