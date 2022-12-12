text = '四川省#2成都市#3东升航#1都大楼#4'
norm_text = text.replace('#1', '').replace('#2', '').replace('#3', '').replace('#4', '')
dict = ['东升航都', '解甲园', '四川省', '成都市', '广东省', '深圳市']
dict_str = '/t'.join(dict)

window = ''
i = 0
in_dicts = []
while i < len(norm_text):
    window += norm_text[i]
    if window in dict_str:
        pass
    else:
        if len(window) == 1:
            window = ''
        else:
            before_window = window[:-1]
            if before_window in dict:
                in_dicts.append(before_window)
            window = window[-1]
    i += 1

if window in dict_str:
    in_dicts.append(window)

print(in_dicts)
