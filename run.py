from flask import Flask
from flask import render_template
from flask import request
from xiaohuaAPI import XiahuaClient
import json

app = Flask(__name__)


@app.route('/random', methods=['GET'])
def random():
    kw = request.args.get('n', '')
    if kw is None or kw == '':
        return ''
    xhc = XiahuaClient()
    return xhc.getRandomItem(xhc.getNum(), int(kw))


@app.route('/item', methods=['GET'])
def item():
    kw = request.args.get('s', '')
    if kw is None or kw == '':
        return ''
    xhc = XiahuaClient()
    return xhc.getItem(kw)


@app.route('/', methods=['GET'])
@app.route('/index.htm', methods=['GET'])
def main():
    xhc = XiahuaClient()
    text = xhc.getRandomItem(xhc.getNum(), 1)
    data = json.loads(text)
    return render_template('index.htm', data=data)


if __name__ == '__main__':
    app.run(debug=True)
