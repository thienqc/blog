---
share: true
comments: true
filename: cach-doc-pdf-trang-doi
aliases:
  - Cách đọc PDF dạng trang đôi
description: 
tags:
  - tip
date: 2024-01-27
URL:
---
# Cách đọc PDF dạng trang đôi
Đôi khi đọc một số sách PDF mà có trang đôi (nhất là sách của nhà DK), cho dù bật chế độ xem 2 trang cùng lúc thì vẫn bị lệch, như thế này:

![](https://i.imgur.com/WGCsIEc.png)

Lí do là vì người đóng gói chưa chèn thêm 1 trang trống phía sau trang bìa, nên xuất hiện tình trạng lệch trang.

Cách giải quyết như sau

- Ở đây mình sử dụng phần mềm [Foxit Reader](https://www.foxit.com/downloads/#Foxit-Reader/) (free)
- Vào tab `View`
	- Chọn `Continuous Facing` để bật trang đôi
	- Chọn `Separate Cover Page` để tách trang bìa riêng ra (nếu không bị lệch thì thôi)
	- ![](https://i.imgur.com/DzByW0s.png)
- Vào `File` → `Preferences` → `Page Display` → `Default Layout and Zoom` → `Custom margin`: đặt **0 px**
	- ![](https://i.imgur.com/303xmMx.png)


Thành quả

![](https://i.imgur.com/ujKkgTJ.png)
