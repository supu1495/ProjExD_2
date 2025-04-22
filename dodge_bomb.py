import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectまたは爆弾Rect
    戻り値:タプル(横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    side, tate = True, True #縦,横の変数
    #横方向判定(画面内だったら)
    if rct.left < 0 or WIDTH < rct.right:
        side = False
    #縦方向判定(画面内だったら)
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return side, tate
#演習1
def gameover(screen: pg.Surface) -> None:
    if kk_rct.colliderect(bb_rct):
        gameover(screen)

#演習2
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    
    #加速度のリスト策系
    # bb_accs = [a for a in range(1,11)]
    
    bb_accs = []
    for a in range(1,11):
        bb_accs.append(a)

    # bb_accs は[1,2,3,4,5,6,7,8,9,10]

    #拡大爆弾Surfaceのリスト
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    # イメージ
    # bb_imgs = [bb_img1, bb_img2, bb_img3, bb_img4.....]
    # bb_accs = [speed1, speed2, speed3, speed4,,,,,,,,]

    return  bb_imgs, bb_accs


# def return_num():
#     num = 1
#     return num

# ret_num =  return_num()

# lst = [1,2,3,4,5,6,7]
# print(lst[0])

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾の初期化
    bb_imgs, bb_accs = init_bb_imgs()

    bb_img = bb_imgs[0]
    # pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    # bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    # bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])


        if kk_rct.colliderect(bb_rct):
            go_img = pg.Surface((1600,900))
            pg.draw.rect(go_img, (0, 0, 0), (0,0, 1600,900))
            go_img.set_alpha(90) #透明化
            screen.blit(go_img,[0, 0])
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255, 0, 0))
            screen.blit(txt, [300,200])
            pg.display.update()
            time.sleep(5)
            return           
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items(): #DELTAの中身が4つ分for文で回ってる
            if key_lst[key]:
                sum_mv[0] += mv[0] #左右方向
                sum_mv[1] += mv[1] #上下方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5 
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

       
        # main
        

        # イメージ
        # bb_imgs = [bb_img1, bb_img2, bb_img3, bb_img4]
        # bb_accs = [speed1, speed2, speed3, speed4]

        # avx = vx*bb_accs[min(tmr//500, 9)]
        # bb_img = bb_imgs[min(tmr//500, 9)]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #画面内に戻す
        screen.blit(kk_img, kk_rct)

        a_vx = vx*bb_accs[min(tmr//500, 9)]
        a_vy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.width = bb_img.get_width()
        bb_rct.height = bb_img.get_height()
        
        bb_img.set_colorkey((0, 0, 0))
        bb_rct.move_ip(a_vx, a_vy)
        screen.blit(bb_img, bb_rct)
        side, tate = check_bound(bb_rct)
        if not side:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
