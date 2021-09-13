import execjs

ctx = execjs.compile(open("./fkw.js", "r", encoding='utf-8').read())
pwd = ctx.call('md5', '123')
print(pwd)