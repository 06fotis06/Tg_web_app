import streamlit as st
import aiohttp
import asyncio
import json



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.css-1avcm0n {display: none}
.css-18ni7ap {display: none}
.styles_terminalButton__JBj5T {display: none}
.css-1y4p8pa {color: white;background: rgb(49, 51, 63);}
.css-fg4pbf {color: white;background: rgb(49, 51, 63);}
.css-uf99v8 {display: block}
.css-1y4p8pa {padding:0;padding-left:20px;padding-top:230px}
.viewerBadge_link__qRIco {display:none}
.css-1y4p8pa {max-width:100vw}
img {width:350px}
.css-1y4p8pa {max-width:100%; background-image: url(http://4dam.ru/picture/matrix.jpg); background-size: cover}
.css-5rimss eqr7zpz4 {text-align:center, background-color: #636262; border-radius: 0 0 5px 5px }
p {font-size: 2,5rem}
.css-1y4p8pa { width:100vw}
.css-woz07z {width:350px}
.css-1y4p8pa {height:100vh}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

async def fetch(session, url, auth):
    async with session.get(url, auth=auth, ssl=False) as response:
        return await response.text()

async def get_name(session, id, auth):
    url = f'https://77.87.102.139:8081/api/hosts/{id}'
    response = await fetch(session, url, auth)
    data = json.loads(response)
    return data['result']['name']

async def get_time(session, id, auth):
    url = 'https://77.87.102.139:8081/api/users/balance'
    response = await fetch(session, url, auth)
    data = json.loads(response)
    for item in data['result']:
        if item['userId'] == id:
            available_time = item['availableTime']
            hours = available_time // 3600
            minutes = (available_time % 3600) // 60
            return f'{hours}ч. {minutes}м.'

async def get_data(session, id, auth):
    url = 'https://77.87.102.139:8081/api/usersessions/active'
    response = await fetch(session, url, auth)
    data = json.loads(response)
    for item in data['result']:
        if item['hostId'] == id:
            name = await get_name(session, item['hostId'], auth)
            time = await get_time(session, item['userId'], auth)
            return f'{time}'
    name = await get_name(session, id, auth)
    return f'свободен'

async def update_text(session, card, auth):
    text = card['text']
    new_text = await get_data(session, card['id'], auth)
    text.write(f'<p style="font-size: 30px; margin-left: 80px">{new_text}</p>', unsafe_allow_html=True)
    

async def main():
    cards = [
        {'id': 6, 'text': None},
        {'id': 7, 'text': None},
        {'id': 8, 'text': None},
        {'id': 9, 'text': None},
        {'id': 10, 'text': None},
        {'id': 11, 'text': None},
        {'id': 12, 'text': None},
        {'id': 13, 'text': None},
        {'id': 14, 'text': None},
        {'id': 15, 'text': None}
    ]

    auth = aiohttp.BasicAuth('ggbook', 'Vaymohk2411')
    async with aiohttp.ClientSession() as session:
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            st.image('https://i.ibb.co/CQ8JDJH/8.png')
            cards[2]['text'] = st.empty()
            st.image('https://i.ibb.co/Kjdy2p7/6.png')
            cards[0]['text'] = st.empty()
            
        with col2:
            
            st.image('https://i.ibb.co/mD5kk69/2.png')
            cards[3]['text'] = st.empty()
            st.image('https://i.ibb.co/PYW7CfN/7.png')
            cards[6]['text'] = st.empty()
        with col3:
            st.image('https://i.ibb.co/XDcsmNk/3.png')
            cards[4]['text'] = st.empty()
            st.image('https://i.ibb.co/zmH02kM/8.png')
            cards[7]['text'] = st.empty()
            
        with col4:
            st.image('https://i.ibb.co/TYcK68b/4.png')
            cards[5]['text'] = st.empty()
            st.image('https://i.ibb.co/257S3FS/9.png')
            cards[8]['text'] = st.empty()
        with col5:
            st.image('https://i.ibb.co/0fTfMSs/5.png')
            cards[1]['text'] = st.empty()
            st.image('https://i.ibb.co/mJgwqw0/10.png')
            cards[9]['text'] = st.empty()


        while True:
            tasks = [update_text(session, card, auth) for card in cards]
            await asyncio.gather(*tasks)
            await asyncio.sleep(60)  # Задержка в 60 секунд перед обновлением

asyncio.run(main())
