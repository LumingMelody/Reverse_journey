from hashlib import md5


def get_pwd(pwd):
    new_md5 = md5()
    new_md5.update(pwd.encode('utf-8'))
    return new_md5.hexdigest()


if __name__ == '__main__':
    pwd = "123456"
    password = get_pwd(pwd)
    print(len(password))
    # print(get_pwd(pwd))
