import pyxel
import random


# ゲーム設定(定数)
W, H = 120, 200     # 画面サイズ
JSPEED = 10         # 自機スピード
JC = 10             # 自機カラー
RC = 9              # 岩カラー
N_LEVELUP = 5       # 何回ごとに難易度アップするか
RSPEED_MAX = 10     # 岩スピードの上限
RR_MAX = 30         # 岩サイズの上限

# clamp関数
def clamp(v, min_v, max_v):
    if v < min_v:
        return min_v  # v が下限値未満の場合は下限値(min_v)を返却
    if v > max_v:
        return max_v  # v が上限値を超える場合は上限値(max_v)を返却
    else:
        return v      # v が下限値～上限値の範囲内の場合は vを返却


class Game:
    def __init__(self):
        pyxel.init(W, H, title="Ochi-Yoke", fps = 60) # 画面初期化
        self.reset()                                  # リセット処理呼び出し
        pyxel.run(self.update, self.draw)             # ゲーム開始


    # リセット処理
    def reset(self):
        # 自機
        self.jx = W // 2         # X座標
        self.jy = H - 20         # Y座標
        self.jr = 3              # サイズ(r)
        self.jc = JC             # カラー
        self.jspeed = JSPEED     # スピード

        # 岩
        self.rx = W // 2         # X座標
        self.ry = 0              # Y座標
        self.rr = 3              # サイズ(r)
        self.rc = RC             # カラー
        self.rspeed = 2          # スピード

        # フラグ・カウンタ
        self.hit = False         # 当たりフラグ
        self.passed_count = 0    # 回避回数
        self.score = 0           # スコア


    def update(self):
        # 当たってた場合(hit == True)は以降の処理をスキップ(returnでupdate抜ける)。Rキーでリセット。
        if self.hit == True:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        # ボタン入力受付(左右)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.jx -= self.jspeed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.jx += self.jspeed

        # 画面外飛び出し防止(自機のX座標をclamp関数で補正)
        # 下限は自機サイズ(半径)
        # 上限は画面幅 - 自機サイズ - 1
        self.jx = clamp(self.jx, self.jr, W - self.jr - 1)

        # 岩移動
        self.ry += self.rspeed

        # 当たり判定（円と円）
        dx = self.jx - self.rx
        dy = self.jy - self.ry
        if dx*dx + dy*dy <= (self.jr + self.rr) * (self.jr + self.rr):
            self.hit = True
            return
    
        # 岩が画面下まで行った時の処理
        if self.ry - self.rr > H:
            #岩 リスポーン
            self.ry = -self.rr                                  # Y座標を上に
            self.rx = random.randint(self.rr, W - self.rr -1)   # X座標はランダム

            # 回避回数 ＆ スコア更新
            self.passed_count = self.passed_count + 1         # 回避回数をカウントアップ
            self.score = self.passed_count * 10               # スコア計算

            # 難易度アップ
            if self.passed_count > 0 and self.passed_count % N_LEVELUP == 0:
                self.rspeed = min(self.rspeed + 1, RSPEED_MAX)
                self.rr = min(self.rr + 1, RR_MAX)


    def draw(self):
        # 画面初期化
        pyxel.cls(0)

        # スコア表示
        pyxel.text(x = 10, y = 10, s = "SCORE: " + str(self.score), col = 7)

        # 自機を描画
        pyxel.circ(x = self.jx, y = self.jy, r = self.jr, col = self.jc)

        # 岩を描画
        pyxel.circ(x = self.rx, y = self.ry, r = self.rr, col = self.rc)

        if self.hit == True:
            pyxel.text(10, 40, "GAME OVER !", 7)        
            pyxel.text(10, 50, "PRESS R KEY TO RESTART", 7)        

Game()
