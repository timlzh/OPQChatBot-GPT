import os
import openai
from pickle import load, dump
from transformers import GPT2TokenizerFast
import edge_tts
import time
import asyncio
import base64

defaultApiKey = os.getenv('OPENAI_API_KEY')

config = {
    'default': {
        'preset': '',
        'api_key': '',
        'enable_context': True,
        'context': '',
        'voice': 'zh-CN-XiaoxiaoNeural',
        'openai': {
            'model': 'text-davinci-003',
            'temperature': 0.9,
            'max_tokens': 3000,
            'top_p': 1,
            'echo': False,
            'presence_penalty': 0,
            'frequency_penalty': 0,
        }
    }
}

supported_voices = ""

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
openai.proxy = {
   "http": "http://localhost:7890",
   "https": "http://localhost:7890",
}
if os.path.exists('config'):
    for file in os.listdir('config'):
        with open(f'config/{file}', 'rb') as f:
            config[file[:-7]] = load(f)
else:
    os.mkdir('config')

def newConfig(id):
    config[id] = config['default'].copy()
    saveConfig(id)

def saveConfig(id):
    with open(f'config/{id}.pickle', 'wb') as f:
        dump(config[id], f)

def getConfig(id):
    if id not in config:
        newConfig(id)
        saveConfig(id)
    return config[id]

def setConfig(id, conf):
    config[id] = conf;
    saveConfig(id)

def setPreset(id, preset):
    config[id]['preset'] = preset
    saveConfig(id)
    
def setVoice(id, voice):
    config[id]['voice'] = voice
    saveConfig(id)

def setApiKey(id, api_key):
    config[id]['api_key'] = api_key
    saveConfig(id)

def setAllApiKey(api_key):
    for id in config:
        config[id]['api_key'] = api_key
        saveConfig(id)
    
def setEnableContext(id, enable_context):
    config[id]['enable_context'] = enable_context
    saveConfig(id)

def setMaxTokens(id, max_tokens):
    config[id]['openai']['max_tokens'] = max(min(max_tokens, 4096),4)
    saveConfig(id)

def clear(id):
    config[id]['context'] = ''
    config[id]['preset'] = ''
    saveConfig(id)

def get_chat(prompt,group_config):
    try:
        openai.api_key = group_config['api_key'] or defaultApiKey
        resp = openai.Completion.create(**group_config['openai'],prompt=prompt)
        resp = resp['choices'][0]['text']
    except openai.OpenAIError as e:
        resp = str(e)
    return resp

def chat(id, prompt):
    group_config = getConfig(id)
    # 加载上下文
    if group_config['enable_context']:
        group_context = group_config['context']
    else:
        group_context = ''

    # 计算可发送的 token 数量
    token_limit = 4096 - group_config['openai']['max_tokens'] - len(tokenizer.encode(group_config["preset"])) - 3
    group_context = f'{group_context}Q:{prompt}\nA:'
    ids = tokenizer.encode(group_context)
    tokens = tokenizer.decode(ids[-token_limit:])
    # 计算可发送的字符数量
    char_limit = len(''.join(tokens))
    group_context = group_context[-char_limit:]
    # 从最早的提问开始截取
    pos = group_context.find('Q:')
    group_context = group_context[pos:]
    # 加载预设
    query = f'{group_config["preset"]}\n\n{group_context}'
    print(f'>>>{query}')
    resp = get_chat(query,group_config)
    resp = resp.strip()
    # 更新上下文
    if group_config['enable_context']:
        group_config['context'] = f'{group_context}{resp}\n\n'
    else:
        group_config['context'] = ''
    print(f'<<<{resp}')
    saveConfig(id)
    return resp

async def to_mp3(text, voice, name):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(name)

def to_speech(id, text):
    if 'voice' not in getConfig(id):
        setVoice(id, 'zh-CN-XiaoxiaoNeural')
    path = os.path.join(os.path.dirname(__file__), 'temp')
    name = os.path.join(path, f'{id}-{time.time()}.mp3')
    print(name)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(to_mp3(text, getConfig(id)['voice'], name))
    return name
    # base64_data = base64.b64encode(open(name, 'rb').read())
    # return base64_data
    
if __name__ == '__main__':
    while True:
        prompt = input('>>>')
        chat('test',prompt)
