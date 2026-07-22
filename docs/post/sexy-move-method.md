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
  
[Beginner Rubik's Cube Solution - Solve the cube using only 1 algorithm!](https://cube.rider.biz/beginner.php)  
  
[Solving the 3x3 Cube Using Only The Sexy Move - YouTube](https://www.youtube.com/watch?v=X2OH-lcbqTk)  
  
## Sexy move  
  
`R U R' U'` (RhSM - tay phải) - `L' U' L U` (LhSM - tay trái)  
  
Cái hay của sexy move là nó tác động vào các góc chứ các cạnh không bị ảnh hưởng.   
  
Lặp lại 6 lần sexy move thì sẽ quay lại hình dạng ban đầu.  
  
<iframe width="560" height="315" src="https://www.youtube.com/embed/cKs7wdo1OhY?si=HzW7Va4gGcj3SlhM&amp;start=52" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>  
  
## Thuật toán giải  
  
![](https://i.imgur.com/yqHsYzk.png)  
  
### Giải tầng 1 -2  
#### 1. Giải 4 cạnh ở tầng 1 (Tạo chữ thập)  
![](https://i.imgur.com/UsM7y6D.png)  
  
Bước này cơ bản, thường thì mình giải mặt màu trắng. Nhớ là <font color="green">Green</font> - <font color="blue">Blue</font>, <font color="red">Red</font> - <font color="orange">Orange</font>, White - <font color="yellow">Yellow</font> là đối diện với nhau. Và bộ ba Red - Yellow - Green đi ngược chiều kim đồng hồ.  
  
#### 2. Giải 3 cạnh ở tầng 2  
![](https://i.imgur.com/wgFeBXT.png)  
  
Lật rubik lại để mặt trắng ở dưới. Bước này cũng cơ bản. Nếu chưa quen thì tập vài lần theo công thức sau:  
  
- Case A: `R U' R'`  
- Case B: `F R' F' R`  
  
Nếu trường hợp không có cạnh nào ở tầng 3 như 2 trường hợp trên thì dùng bất kì công thức nào để đưa 1 cạnh từ tầng 2 lên lại tầng 3.  
#### 3. Giải 3 góc ở tầng 1  
![](https://i.imgur.com/bnP2CgX.png)  
  
Sử dụng cột trống này để đưa cục màu trắng từ tầng 3 xuống đúng tầng 1.  
  
- Quay 2 góc về cột trống  
- Sử dụng Sexy move cho tới khi cục màu trắng quay đúng vị trí (mặt trắng ở dưới)  
- Lặp lại cho tới khi xong 3 góc.  
  
Nếu đã quen thì có thể kết hợp bước 2 - 3 thành một.  
  
#### 4. Giải cột 1, 2 còn lại  
  
### Giải tầng 3  
#### 1. Tạo chữ thập vàng  
- `·`, `r`, `---` : F - R U R' U'  
- `.` --> (RhSM) `r` --> (F - RhSM) `---` --> (RhSM) --> `+`  
#### 2. Cho góc đúng vị trí  
- RhSM x3 - LhSM x3 (x2)  
### 3. Lật góc  
- Quay mặt trắng lên trên, dùng 1 cột tạm để xoay mặt vàng xuống, sử dụng RhSM  
  
#### 4. Đảo 3/4 cạnh  
- Ngược chiều kim đồng hồ: R1 - L1 - R5 - L5  
- Cùng chiều kim đồng hồ: L1 - R1 - L5 - R5  
  
