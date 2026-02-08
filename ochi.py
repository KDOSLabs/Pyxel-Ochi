import pyxel
import random


# ゲーム設定
W, H = 120, 240 #画面サイズ
jspeed = 10 # 自機移動速度
rspeed = 2 # 岩移動速度

# 自機初期パラメーター
jx = W // 2  # X座標
jy = H - 20 # Y座標
jr = 3   # サイズ(r)
jc = 10  # 色

# 岩初期パラメーター
rx = W // 2  # X座標
ry = 0 # Y座標
rr = 3   # サイズ(r)
rc = 9  # 色

# 岩回避回数＆スコア初期化
i = 0
score = 0

# 当たりフラグ
hit = False

# ウインドウ初期化
pyxel.init(W, H, title="Ochi-Yoke")


def update():
    global jx
    global rx
    global ry
    global rr
    global rspeed
    global i
    global score
    global hit

    # 当たってた場合(hit == True)はupdateを停止。Rキー入力でリセット
    if hit == True:
        if pyxel.btnp(pyxel.KEY_R):
            # 岩回避回数＆スコア初期化
            i = 0
            score = 0
            rx = W // 2  # X座標
            ry = 0 # Y座標
            rr = 3
            jx = W // 2  # X座標
            rspeed = 2 # 岩移動速度

            # 当たりフラグ
            hit = False 
        return

    # ボタン入力受付(左右)
    if pyxel.btn(pyxel.KEY_LEFT):
        jx -= jspeed
    if pyxel.btn(pyxel.KEY_RIGHT):
        jx += jspeed

    # 画面外飛び出し防止
    if jx < jr:
        jx = jr
    if jx > W - jr - 1:
        jx = W - jr -1

    # 岩移動
    ry += rspeed

    # 当たり判定（円と円）
    dx = jx - rx
    dy = jy - ry
    if dx*dx + dy*dy <= (jr + rr) * (jr + rr):
        hit = True
        return
    

    # 画面下まで行ったら上に戻す。X座標はランダムにする。岩回避回数をカウントアップする
    if ry - rr > H:
        ry = -rr # Y座標を上に
        rx = random.randint(rr, W - rr -1)  # X座標はランダム
        i = i + 1 # 岩回避回数をカウントアップ
        score = i * 10 # スコア計算
        # 回避するごとに難易度アップ
        if i > 0 and i % 2 == 0:
            rspeed = rspeed + 1
            rr = min (rr + 1, 30)


def draw():
    # 画面初期化
    pyxel.cls(0)

    # デバッグ表示
    # pyxel.text(x = 10, y = 20, s = "jx:" + str(jx), col = 1)

    # スコア表示
    pyxel.text(x = 10, y = 10, s = "SCORE :" + str(score), col = 7)

    # 自機を描画
    pyxel.circ(x = jx, y = jy, r = jr, col = jc)

    # 岩を描画
    pyxel.circ(x = rx, y = ry, r = rr, col = rc)

    if hit == True:
        pyxel.text(10, 40, "GAME OVER !", 7)        
        pyxel.text(10, 50, "PRESS R KEY TO CONTINUE", 7)        

pyxel.run(update, draw)

