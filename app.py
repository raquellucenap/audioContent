import os.path
import random
import streamlit as st
import pandas
import pandas as pd
import pickle


m3u_filepaths_file = 'playlists/streamlit.m3u8'
#ESSENTIA_ANALYSIS_PATH = 'data/features.jsonl.pickle'


#def load_essentia_analysis():
    #return pandas.read_pickle(ESSENTIA_ANALYSIS_PATH)

#with open('data/features.jsonl.pickle','rb') as f:
#	data = pickle.load(f)
#audio_analysis = pd.Dataframe(data)
#st.dataframe(audio_analysis)
with open('data/features.csv','rb') as f1:
	data1 = pd.read_csv(f1)
#audio_analysis = pd.Dataframe(data)
audio_analysis1 = pd.DataFrame(data1)

#st.dataframe(audio_analysis)
st.dataframe(audio_analysis1)
audio_analysis = audio_analysis1
st.write('# Audio analysis playlists example')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
audio_analysis = load_essentia_analysis()
audio_analysis_styles = audio_analysis.columns
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write('## 🔍 Select')
st.write('### By style')
st.write('Style activation statistics:')
st.write(audio_analysis.describe())

style_select = st.multiselect('Select by style activations:', audio_analysis_styles)
if style_select:
    # Show the distribution of activation values for the selected styles.
    st.write(audio_analysis[style_select].describe())

    style_select_str = ', '.join(style_select)
    style_select_range = st.slider(f'Select tracks with `{style_select_str}` activations within range:', value=[0.5, 1.])

st.write('## 🔝 Rank')
style_rank = st.multiselect('Rank by style activations (multiplies activations for selected styles):', audio_analysis_styles, [])

st.write('## 🔀 Post-process')
max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
shuffle = st.checkbox('Random shuffle')

if st.button("RUN"):
    st.write('## 🔊 Results')
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
