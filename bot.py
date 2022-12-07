from botoy import Action, Botoy, EventMsg, FriendMsg, GroupMsg
from json import loads
from botoy import decorators as deco
import api

qq = 2985781277
bot = Botoy(qq=qq, use_plugins=False)
action = Action(qq)

@bot.on_group_msg
@deco.ignore_botself
@deco.startswith('/chat')
def chat_msg(ctx: GroupMsg):
    if ctx.Content == '/chat':
        action.sendGroupText(ctx.FromGroupId, '请输入聊天内容')
    else:
        id = ctx.FromGroupId
        msg = ctx.Content[6:]
        res = api.chat(str(id), msg)
        action.replyGroupMsg(ctx.FromGroupId, res, ctx.MsgSeq, ctx.MsgTime, ctx.FromUserId, ctx.Content)
        # action.sendGroupText(ctx.FromGroupId, res)


@bot.on_group_msg
@deco.ignore_botself
@deco.startswith('/key')
def key_msg(ctx: GroupMsg):
    if ctx.Content == '/key':
        action.sendGroupText(ctx.FromGroupId, '请输入 API Key')
    else:
        id = ctx.FromGroupId
        msg = ctx.Content[5:]
        api.setApiKey(str(id), msg)
        action.sendGroupText(ctx.FromGroupId, '已设置 API Key')


@bot.on_group_msg
@deco.ignore_botself
@deco.startswith('/mem')
def mem_msg(ctx: GroupMsg):
    if ctx.Content == '/mem':
        action.sendGroupText(ctx.FromGroupId, '请输入长度上限')
    else:
        id = ctx.FromGroupId
        msg = ctx.Content[5:]
        action.sendGroupText(ctx.FromGroupId, '已修改长度上限')
        print(int(msg))
        api.setMaxTokens(str(id), int(msg))
        

@bot.on_group_msg
@deco.ignore_botself
def key_msg(ctx: GroupMsg):
    try:
        content = loads(ctx.Content)['Content']
    except:
        content = ctx.Content
    print(content)
    print(type(content))
    if not content.startswith('/set'):
        return
    if content == '/set':
        action.sendGroupText(ctx.FromGroupId, '请输入config')
    else:
        id = ctx.FromGroupId
        msg = content[5:]
        msg_par = ''
        for i in msg:
            if i == '"': msg_par += "'"
            elif i == "'": msg_par += '"'
            else: msg_par += i
        msg_par = msg_par.replace("True","true")
        msg_par = msg_par.replace("False","false")
        api.setConfig(str(id), dict(loads(msg_par)))
        action.sendGroupText(ctx.FromGroupId, '已设置config')

@bot.on_group_msg
@deco.ignore_botself
def preset_msg(ctx: GroupMsg):
    try:
        content = loads(ctx.Content)['Content']
    except:
        content = ctx.Content
    print(content)
    print(type(content))
    if not content.startswith('/preset'):
        return
    if content == '/preset':
        action.sendGroupText(ctx.FromGroupId, '请输入预设内容')
    else:
        id = ctx.FromGroupId
        msg = content.replace('/preset', '')
        api.setPreset(str(id), msg)
        action.sendGroupText(ctx.FromGroupId, '已设置预设内容')




@bot.on_group_msg
@deco.ignore_botself
@deco.equal_content('/reset')
def reset_msg(ctx: GroupMsg):
    id = ctx.FromGroupId
    api.newConfig(str(id))
    action.sendGroupText(ctx.FromGroupId, '已重置')


@bot.on_group_msg
@deco.ignore_botself
@deco.equal_content('/get')
def get_msg(ctx: GroupMsg):
    id = ctx.FromGroupId
    res = str(api.getConfig(str(id)))
    action.sendGroupText(ctx.FromGroupId, res)

@bot.on_group_msg
@deco.ignore_botself
@deco.equal_content('/clear')
def clear_msg(ctx: GroupMsg):
    id = ctx.FromGroupId
    api.clear(str(id))
    action.sendGroupText(ctx.FromGroupId, '已重置对话')

@bot.on_group_msg
@deco.ignore_botself
@deco.equal_content('/help')
def help_msg(ctx: GroupMsg):
    action.sendGroupText(ctx.FromGroupId,
                         '''\
OPQChatBot-GPT 指令列表
/chat   ：生成对话
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


if __name__ == "__main__":
    bot.run()
