import os
from flask import Flask, request, send_file, render_template, jsonify
from flask import redirect
from flask import url_for
from flask import request
from flask_cors import CORS
from model.login import is_existed, exist_user, is_null
from model.register import add_user
import cv2
import numpy as np
import io

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('user_login'))


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form.get('username')
        password = request.form.get('password')
        if is_null(username, password):
            alert = "用户名和密码不能为空！"
            return render_template('login.html', message=alert)
        elif is_existed(username, password):
            return render_template('index.html', username=username)
        elif exist_user(username):
            alert = "用户名或密码错误！"
            return render_template('login.html', message=alert)
        else:
            alert = "用户不存在，请先注册！"
            return render_template('login.html', message=alert)
    return render_template('login.html')


@app.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('conf_password')
        if is_null(username, password):
            alert = "用户名和密码不能为空！"
            return render_template('register.html', message=alert)
        elif exist_user(username):
            alert = "用户已存在，请直接登录！"
            return render_template('register.html', message=alert)
        elif confirm_password != password:
            alert = "密码不一致！请重新输入！"
            return render_template('register.html', message=alert)
        else:
            alert = "注册成功，请返回登录！"
            add_user(request.form['username'], request.form['password'])
            return render_template('register.html', message=alert)
    return render_template('register.html')


# 启用CORS
CORS(app)
# 创建临时目录，存储前端发来的图片
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 设置文件夹权限（例如：用户读写执行，组读写执行，其他读写执行）
# 0o777 是八进制表示法
os.chmod(UPLOAD_FOLDER, 0o777)


@app.route('/invert', methods=['POST'])
#颜色取反
def invert():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file part'}), 400
    if file:
        # 保存上传的文件到临时目录
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'message': 'Invalid image'}), 400

        # 颜色取反
        inverted_img = cv2.bitwise_not(img)

        # 将处理后的图片以字节流的形式返回
        _, img_encoded = cv2.imencode('.jpg', inverted_img)
        return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/jpg')

    return jsonify({'message': 'Failed to upload file'}), 500

@app.route('/gray', methods=['POST'])
#灰度化
def gray():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file part'}), 400
    if file:
        # 保存上传的文件到临时目录
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'message': 'Invalid image'}), 400

        # 对每个像素的颜色进行取反
        inverted_img = 255 - img
        # 灰度化
        gray_img = cv2.cvtColor(inverted_img, cv2.COLOR_BGR2GRAY)

        # 将处理后的图片以字节流的形式返回
        _, img_encoded = cv2.imencode('.jpg', gray_img)
        return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/jpg')

    return jsonify({'message': 'Failed to upload file'}), 500

@app.route('/binarize', methods=['POST'])
#二值化
def binarize():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file part'}), 400
    if file:
        # 保存上传的文件到临时目录
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'message': 'Invalid image'}), 400

        # 对每个像素的颜色进行取反
        inverted_img = 255 - img
        # 灰度化
        gray_img = cv2.cvtColor(inverted_img, cv2.COLOR_BGR2GRAY)
        # 对灰度图进行阈值分割（二值化）
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

        # 将处理后的图片以字节流的形式返回
        _, img_encoded = cv2.imencode('.jpg', binary_img)
        return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/jpg')

    return jsonify({'message': 'Failed to upload file'}), 500

@app.route('/denoise', methods=['POST'])
#去噪
def denoise():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file part'}), 400
    if file:
        # 保存上传的文件到临时目录
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'message': 'Invalid image'}), 400

        # 对每个像素的颜色进行取反
        inverted_img = 255 - img
        # 灰度化
        gray_img = cv2.cvtColor(inverted_img, cv2.COLOR_BGR2GRAY)
        # 对灰度图进行阈值分割（二值化）
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

        # 中值滤波
        rec_img = cv2.medianBlur(binary_img, 3)

        # 将处理后的图片以字节流的形式返回
        _, img_encoded = cv2.imencode('.jpg', rec_img)
        return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/jpg')

    return jsonify({'message': 'Failed to upload file'}), 500

@app.route('/enhance', methods=['POST'])
#图像增强
def enhance():
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file part'}), 400
    if file:
        # 保存上传的文件到临时目录
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'message': 'Invalid image'}), 400

        # 对每个像素的颜色进行取反
        inverted_img = 255 - img
        # 灰度化
        gray_img = cv2.cvtColor(inverted_img, cv2.COLOR_BGR2GRAY)
        # 对灰度图进行阈值分割（二值化）
        _, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

        # 中值滤波
        rec_img = cv2.medianBlur(binary_img, 3)

        # 使用高斯滤波器进行平滑处理
        # cv2.GaussianBlur() 函数也接收图像和一个核大小，还可以指定X和Y方向的标准差
        gaussian_blurred_image = cv2.GaussianBlur(rec_img, (7, 7), 0)

        # 锐化
        # 定义锐化滤波器
        # 对于拉普拉斯滤波器，OpenCV提供了cv2.Laplacian()函数
        # 对于自定义滤波器，可以使用np.array定义滤波器核，并与图像进行卷积
        # 这里我们使用一个简单的锐化滤波器核
        sharpen_kernel = np.array([
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, 36, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1]])
        # 应用锐化滤波器
        sharpened_image = cv2.filter2D(gaussian_blurred_image, -1, sharpen_kernel)

        # 将处理后的图片以字节流的形式返回
        _, img_encoded = cv2.imencode('.jpg', sharpened_image)
        return send_file(io.BytesIO(img_encoded.tobytes()), mimetype='image/jpg')

    return jsonify({'message': 'Failed to upload file'}), 500



if __name__ == '__main__':
    app.run(debug=True)
