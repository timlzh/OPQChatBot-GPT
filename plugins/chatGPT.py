# from botoy import Action, Botoy, EventMsg, FriendMsg, GroupMsg
from botoy import S, ctx, mark_recv, action
from json import loads
# from botoy import decorators as deco
import plugins.api as api
import time
import os

# qq = 1315284898 
# bot = Botoy(qq=qq, use_plugins=False)
# action = Action(qq)



# @bot.on_group_msg
# @deco.ignore_botself
async def chat_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        try:
            content = loads(g.text)['Content']
        except:
            content = g.text
        print(content)
        print(type(content))
        if not (content.startswith('/chat') or content.startswith('/vchat')):
            return
        if content in ['/chat', '/vchat']:
            await S.text('请输入聊天内容')
        else:
            id = g.from_group
            msg = content[6:]
            res = api.chat(str(id), msg)
            if content.startswith('/chat'):
                # await action.replyGroupMsg(g.from_group, res, g.msg_seq, g.msg_time, g.from_user, g.text)
                await S.text(res, at = True)
            else:
                await S.text("语音功能暂未开放")
                # name = api.to_speech(str(id), res)
                # await action.sendGroupVoice(g.from_group, voicePath=name)
                # time.sleep(10)
                # os.remove(name)


# @bot.on_group_msg
# @deco.ignore_botself
# @deco.startswith('/key')
async def key_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        if not g.text.startswith('/key'): return
        if g.text == '/key':
            await S.text('请输入 API Key')
        else:
            id = g.from_group
            msg = g.text[5:]
            api.setApiKey(str(id), msg)
            api.setAllApiKey(msg)
            await S.text('已设置 API Key')


# @bot.on_group_msg
# @deco.ignore_botself
# @deco.startswith('/mem')
async def mem_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        if not g.text.startswith('/mem'): return
        if g.text == '/mem':
            await S.text('请输入长度上限')
        else:
            id = g.from_group
            msg = g.text[5:]
            await S.text('已修改长度上限')
            print(int(msg))
            api.setMaxTokens(str(id), int(msg))


async def key_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        try:
            content = loads(g.text)['Content']
        except:
            content = g.text
        print(content)
        print(type(content))
        if not content.startswith('/set'):
            return
        if content == '/set':
            await S.text('请输入config')
        else:
            id = g.from_group
            msg = content[5:]
            msg_par = ''
            for i in msg:
                if i == '"':
                    msg_par += "'"
                elif i == "'":
                    msg_par += '"'
                else:
                    msg_par += i
            msg_par = msg_par.replace("True", "true")
            msg_par = msg_par.replace("False", "false")
            api.setConfig(str(id), dict(loads(msg_par)))
            await S.text('已设置config')


# @bot.on_group_msg
# @deco.ignore_botself
async def preset_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        try:
            content = loads(g.text)['Content']
        except:
            content = g.text
        print(content)
        print(type(content))
        if not content.startswith('/preset'):
            return
        if content == '/preset':
            await S.text('请输入预设内容')
        else:
            id = g.from_group
            msg = content.replace('/preset', '')
            api.setPreset(str(id), msg)
            await S.text('已设置预设内容')


# @bot.on_group_msg
# @deco.ignore_botself
# @deco.equal_content('/reset')
async def reset_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        if g.text != '/reset': return
        id = g.from_group
        api.newConfig(str(id))
        await S.text('已重置')

# @bot.on_group_msg
# @deco.ignore_botself
# @deco.equal_content('/get')
async def get_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        if g.text != '/get': return
        id = g.from_group
        res = str(api.getConfig(str(id)))
        await S.text(res)


# @bot.on_group_msg
# @deco.ignore_botself
# @deco.equal_content('/clear')
async def clear_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        if g.text != '/clear': return
        id = g.from_group
        api.clear(str(id))
        await S.text('已重置对话')


# @bot.on_group_msg
# @deco.ignore_botself
# @deco.equal_content('/help')
async def help_msg():
    if g := ctx.g:
        if g.from_user == g.bot_qq: return
        if g.text != '/help': return
        await S.text('''\
    OPQChatBot-GPT 指令列表
    /chat   ：生成对话
    /vchat  ：生成语音对话
    /clear  ：重置对话
    /get    ：查看配置
    /set    ：设置配置（直接传入get的返回值即可）
    /reset  ：重置配置
    /preset ：修改预设
    /key    ：设置 OpenAI API Key
    /mem    ：设置记忆长度，范围为 4~4096
    /help   ：查看帮助
    项目地址 ：https://github.com/timlzh/OPQChatBot-GPT
    配置参考 ：https://beta.openai.com/docs/api-reference/completions/create
    鸣谢     ：Byaidu✌✌
    ''')

_ = mark_recv + chat_msg + key_msg + mem_msg + preset_msg + reset_msg + get_msg + clear_msg + help_msg
