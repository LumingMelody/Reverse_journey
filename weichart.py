import execjs

ctx = execjs.compile(open("./weixin.js", "r", encoding='utf-8').read())
pwd = ctx.call("getPwd", "123456")
print(pwd)
