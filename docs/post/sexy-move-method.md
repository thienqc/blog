---
filename: sexy-move-method

share: true
comments: true
tags:
  - rubik
date: 2023-11-03
URL: Phương pháp giải Rubik chỉ cần nhớ 1 công thức
description:
---
# Sexy move method

## Sexy move

`R U R' U'`

Cái hay của sexy move là nó tác động vào các góc chứ các cạnh không bị ảnh hưởng. 

Lặp lại 6 lần sexy move thì sẽ quay lại hình dạng ban đầu.

<iframe width="560" height="315" src="https://www.youtube.com/embed/cKs7wdo1OhY?si=HzW7Va4gGcj3SlhM&amp;start=52" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Thuật toán giải

![](https://i.imgur.com/yqHsYzk.png)


### 1. Giải 4 cạnh ở tầng 1 (Tạo chữ thập)
![](https://i.imgur.com/UsM7y6D.png)

Bước này cơ bản, thường thì mình giải mặt màu trắng. Nhớ là <font color="green">Green</font> - <font color="blue">Blue</font>, <font color="red">Red</font> - <font color="orange">Orange</font>, White - <font color="yellow">Yellow</font> là đối diện với nhau.

### 2. Giải 3 cạnh ở tầng 2
![](https://i.imgur.com/wgFeBXT.png)

Lật rubik lại để mặt trắng ở dưới. Bước này cũng cơ bản. Nếu chưa quen thì tập vài lần theo công thức sau:

- Case A: `R U' R'`
- Case B: `F R' F' R`

Nếu trường hợp không có cạnh nào ở tầng 3 như 2 trường hợp trên thì dùng bất kì công thức nào để đưa 1 cạnh từ tầng 2 lên lại tầng 3.
## 3. Giải 3 góc ở tầng 1
![](https://i.imgur.com/bnP2CgX.png)

Sử dụng cột trống này để đưa cục màu trắng từ tầng 3 xuống đúng tầng 1.

- Quay 2 góc về cột trống
- Sử dụng Sexy move cho tới khi cục màu trắng quay đúng vị trí (mặt trắng ở dưới)
- Lặp lại cho tới khi xong 3 góc.

Nếu đã quen thì có thể kết hợp bước 2 - 3 thành một.

### 4. Giải 3 cạnh ở tầng 3


### 5. Giải 2 cạnh còn lại
`(R U R' U) (R U2 R')`

### 6. Giải 3 (hoặc 4) góc ở tầng 3
Lặp lại Sexy move
### 7. Giải 2 (hoặc 1) góc còn lại
Lặp lại Sexy move
