import random, os, pickle
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
app = Flask(__name__, template_folder='templates')
CORS(app)

dict_name = {'能天使': 0, '推进之王': 1, '伊芙利特': 2, '艾雅法拉': 3, '安洁莉娜': 4, '闪灵': 5, '夜莺': 6, '星熊': 7, '塞雷娅': 8, '银灰': 9, '斯卡蒂': 10, '陈': 11, '黑': 12, '赫拉格': 13, '麦哲伦': 14, '莫斯提马': 15, '煌': 16, '阿': 17, '年': 18, '刻俄柏': 19, '风笛': 20, '傀影': 21, '温蒂': 22, 'W': 23, '早露': 24, '铃兰': 25, '棘刺': 26, '森蚺': 27, '史尔特尔': 28, '瑕光': 29, '泥岩': 30, '迷迭香': 31, '山': 32, '空弦': 33, '嵯峨': 34, '夕': 35, '灰烬': 36, '异客': 37, '歌蕾蒂娅': 38, '凯尔希': 39, '浊心斯卡蒂': 40, '卡涅利安': 41, '帕拉斯': 42, '水月': 43, '假日威龙陈': 44, '琴柳': 45, '远牙': 46, '焰尾': 47, '耀骑士临光': 48, '灵知': 49, '老鲤': 50, '令': 51, '澄闪': 52, '菲亚梅塔': 53, '号角': 54, '流明': 55, '艾丽妮': 56, '归溟幽灵鲨': 57, '黑键': 58, '多萝西': 59, '鸿雪': 60, '百炼嘉维尔': 61, '玛恩纳': 62, '白铁': 63, '伺夜': 64, '斥罪': 65, '缄默德克萨斯': 66, '焰影苇草': 67, '林': 68, '重岳': 69, '仇白': 70, '麒麟X夜刀': 71, '伊内丝': 72, '淬羽赫默': 73, '霍尔海雅': 74, '缪尔赛思': 75, '圣约送葬人': 76, '提丰': 77, '琳琅诗怀雅': 78, '纯烬艾雅法拉': 79}
lst_name = ['能天使', '推进之王', '伊芙利特', '艾雅法拉', '安洁莉娜', '闪灵', '夜莺', '星熊', '塞雷娅', '银灰', '斯卡蒂', '陈', '黑', '赫拉格', '麦哲伦', '莫斯提马', '煌', '阿', '年', '刻俄柏', '风笛', '傀影', '温蒂', 'W', '早露', '铃兰', '棘刺', '森蚺', '史尔特尔', '瑕光', '泥岩', '迷迭香', '山', '空弦', '嵯峨', '夕', '灰烬', '异客', '歌蕾蒂娅', '凯尔希', '浊心斯卡蒂', '卡涅利安', '帕拉斯', '水月', '假日威龙陈', '琴柳', '远牙', '焰尾', '耀骑士临光', '灵知', '老鲤', '令', '澄闪', '菲亚梅塔', '号角', '流明', '艾丽妮', '归溟幽灵鲨', '黑键', '多萝西', '鸿雪', '百炼嘉维尔', '玛恩纳', '白铁', '伺夜', '斥罪', '缄默德克萨斯', '焰影苇草', '林', '重岳', '仇白', '麒麟X夜刀', '伊内丝', '淬羽赫默', '霍尔海雅', '缪尔赛思', '圣约送葬人', '提丰', '琳琅诗怀雅', '纯烬艾雅法拉']
len_lst_name_1 = len(lst_name) - 1


@app.route('/new_compare', methods=['GET'])
@cross_origin()
def new_compare():
    a = random.randint(0, len_lst_name_1)
    b = random.randint(0, len_lst_name_1)
    while a == b:
        b = random.randint(0, len_lst_name_1)
    return lst_name[a] + ' ' + lst_name[b]


@app.route('/save_score', methods=['POST']) 
@cross_origin()
def save_score():
    if verify():
        with open('list/win_score.pickle', 'rb') as f:
            lst_win_score = pickle.load(f)
        with open('list/lose_score.pickle', 'rb') as f:
            lst_lose_score = pickle.load(f)
        
        lst_win_score[dict_name[request.args.get('win_name')]] += 1
        lst_lose_score[dict_name[request.args.get('lose_name')]] += 1

        with open('list/win_score.pickle', 'wb') as f:
            pickle.dump(lst_win_score, f)
        with open('list/lose_score.pickle', 'wb') as f:
            pickle.dump(lst_lose_score, f)

    return 'success'


@app.route('/view_final_order', methods=['GET'])
@cross_origin()
def view_final_order():
    with open('list/win_score.pickle', 'rb') as f:
        lst_win_score = pickle.load(f)
    with open('list/lose_score.pickle', 'rb') as f:
        lst_lose_score = pickle.load(f)

    lst_score = [lst_win_score[_] - lst_lose_score[_] for _ in range(len(lst_win_score))]
    # lst_score = lst_win_score
    dict_score = dict(zip(lst_name, lst_score))

    final_name, final_score = zip(*sorted(dict_score.items(), key=lambda _: -_[1]))
    return jsonify({'name': final_name, 'score': final_score, 'count': '已收集数据 ' + str(sum(lst_win_score)) + ' 条'})


@app.route('/page', methods=['GET'])
@cross_origin()
def page():
    return render_template('page.html')


@app.route('/favicon.ico', methods=['GET'])
@cross_origin()
def ico():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def get_client_ip():
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = real_ip.split(",")[0]
    except:
        try:
            client_ip = request.META['REMOTE_ADDR']
        except:
            client_ip = request.remote_addr
    return client_ip


def verify():
    client_ip = get_client_ip()
    with open('ip/ip_ban.pickle', 'rb') as f:
        ip_ban = pickle.load(f)
    if client_ip in ip_ban:
        return False

    with open('ip/ip_dict.pickle', 'rb') as f:
        ip_dict = pickle.load(f)
    if not client_ip in ip_dict:
        ip_dict[client_ip] = [0] * len(lst_name)
    
    win_index = dict_name[request.args.get('win_name')]
    lose_index = dict_name[request.args.get('lose_name')]
    ip_dict[client_ip][win_index] += 1
    ip_dict[client_ip][lose_index] -= 1

    if ip_dict[client_ip][win_index] == 7 or ip_dict[client_ip][lose_index] == -7:
        del ip_dict[client_ip]
        ip_ban.add(client_ip)

        with open('ip/ip_dict.pickle', 'wb') as f:
            pickle.dump(ip_dict, f)
        with open('ip/ip_ban.pickle', 'wb') as f:
            pickle.dump(ip_ban, f)
        return False
    else:
        with open('ip/ip_dict.pickle', 'wb') as f:
            pickle.dump(ip_dict, f)
        return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)