# import libraries
import streamlit as st
from streamlit_player import st_player
import re
import pandas as pd
import malaya

# table of content
class Toc:
    def __init__(self):
        self._items = []
        self._placeholder = None
    
    def title(self, text):
        self._markdown(text, "h1")

    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=True):
        self._placeholder = st.sidebar.empty() if sidebar else st.empty()

    def generate(self):
        if self._placeholder:
            self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
    
    def _markdown(self, text, level, space=""):
        key = "-".join(text.split()).lower()
        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")

def cleaning(text):
    new_string = text.replace("\\n", "")
    new_string2 = new_string.replace("\\xa0", "")
    new_string3 = new_string2.replace("\\'", "")
    new_string4 = re.sub(r'www\S+', '', new_string3)
    new_string5 = new_string4.replace("Â", "")
    new_string6 = new_string5.replace("\\x9d", "")
    new_string7 = new_string6.replace("â€", "")
    new_string8 = new_string7.replace("â€œ", "")
    new_string9 = new_string8.replace("œ", "")
    new_string11 = re.sub(' +', ' ', new_string9).strip()
    new_string12 = new_string11.replace(". . .", "")
    new_string13 = re.sub(r'http\S+', '', new_string12)
    new_string14 = re.sub(r'[-+]?\d*\.\d+|\d+', '', new_string13)
    return new_string14

# hide menu bar
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# set up layout
padding = 1
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# set up title
st.markdown("<h1 style='text-align: center;'>Ujian Kebolehbacaan Khadijah Rohani</h1>", unsafe_allow_html=True)
st.write('\n')

# set up sidebar
st.sidebar.header("Kandungan")
toc = Toc()
toc.placeholder()

# calculate single text
toc.header('Kalkulator Khadijah Rohani')
st.write("Apakah kebolehbacaan [Khadijah Rohani](#tahap-gred-khadijah-rohani)❓")

# upload file
toc.header("Upload csv file")
file_upload = st.file_uploader("", type=["csv"])
if file_upload is not None:
    data = pd.read_csv(file_upload, encoding='unicode_escape')
    st.write(data)
    name = file_upload.name.replace('.csv', '')
    name = name+"_labelled.csv"

def en_emotion(text):
    with bz2.BZ2File('Emotion/en_emotion.pbz2', 'rb') as training_model:
        en_model = cPickle.load(training_model)

    label = en_model.predict([text])
    return label

# run the program
result = st.button("Run")
if result:
    wc = []
    ans = []
    st.write("Be patient, need to wait 2 to 3 minutes :smile:")
    st.write("If raising error, please reduce the number of clusters")

    # Topic clustering
    #wc, ans, topic_df = processing(data, gensim, malaya, word_tokenize, np, MovieGroupProcess, pd, WordCloud, int_val, list_stop)

    # Detect language
    #topic_df['Language'] = topic_df['comment'].apply(detect_lang)

    # Detect sentiment
    #sentiment_df = detect_sentiment(topic_df, malaya)

    # Detect emotion
    #final_df = detect_emotion(data, malaya)
    
    # malay emotion analysis
    ms_model = malaya.emotion.multinomial()
    #ms_model = malaya.emotion.transformer(model = 'albert')
    clean = data['comment'].values.tolist()
    ms_emo = ms_model.predict(clean)
    data = data.assign(Emotion = ms_emo)
    # english emotion analysis
    data.loc[df['Language'] == "en", 'Emotion'] = data['clean'].apply(en_emotion)

    # remove unwanted coulmns
    data = data.drop(['Language', 'clean'], axis = 1)
    
    # download labelled file
    st.write("Below is the labelled file, click button to download.")
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=name,
        mime='text/csv',
    )
    st.write('\n')
    
# input text
TextBox = st.text_area('Masukkan teks untuk menyemak kebolehbacaan', height=200)

# run the test
test = st.button("Kira Kebolehbacaan")

new_content = cleaning(TextBox)

if test:
    my_expander = st.expander(label='Teks yang Dibersihkan')
    with my_expander:
        st.write(new_content)
    
    zxc = malaya.emotion.multinomial()
    labels = []
    labels = zxc.predict(["new_content"])
    st.write(labels)
    
st.write('\n')
st.write('\n')


toc.header("Tahap Gred Khadijah Rohani")
st.write("Kebolehbacaan Khadijah Rohani ialah pengukuran kebolehbacaan sesuatu bahan untuk membolehkan para pendidik, ibu bapa dan para penulis cuba menyesuaikan kebolehan membaca murid-murid dengan bahan yang mereka baca.")
st.write("Dalam kalkulator ini,")
st.write(
    """    
- Kami mengalih keluar nombor termasuk perpuluhan.
- Kami mengalih keluar pautan url.
    """)
st.write("Had formula Khadijah Rohani,")
st.write(
    """    
- Teks perlu dalam 300 perkataan.
- Tetapi kami memperbaiki had ini dengan [formula ini](#kalkulator-khadijah-rohani-yang-diperbaikan).
    """)

toc.header("Tukar kepada fail CSV")
st.write('Video ini akan mengajar anda cara menukar fail excel kepada fail csv.')
# Embed a youtube video
st_player("https://www.youtube.com/watch?v=IBbJzzj5r90")
st.write('\n')

toc.generate()
