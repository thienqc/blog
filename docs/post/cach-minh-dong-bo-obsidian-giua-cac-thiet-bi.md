---
filename: cach-minh-dong-bo-obsidian-giua-cac-thiet-bi
aliases:
  - Cách mình đồng bộ obsidian giữa các thiết bị
description: 
URL: 

date: 2023-05-21
Link: https://www.facebook.com/groups/594306492570157/posts/644009084266564
tags:
  - obsidian
share: true
comments: true
---
# Cách mình đồng bộ obsidian giữa các thiết bị

![](https://i.imgur.com/dr0JHdK.jpg)


Có nhiều cách đề đồng bộ dữ liệu giữa các thiết bị như là _Obsidian Sync_ (chính chủ của Obsidian nhưng trả phí), các dịch vụ lưu trữ đám mây (Dropbox, Google Drive, OneDrive, iCloud), Syncthing, Git...

Vì thiết bị mình sử dụng là Window và Android nên mình sẽ sử dụng **Dropbox kết hợp với Dropsync** (để đồng bộ lên di động).

##### B1: TẢI DROPBOX VÀ CÀI ĐẶT TRÊN MÁY TÍNH

[Download & Install - Dropbox](https://www.dropbox.com/install)

##### B2: TẠO VAULT TRONG THƯ MỤC DROPBOX

Nếu đã có sẵn vault thì có thể copy thư mục vault đó qua Dropbox

##### B3: TẢI DROPSYNC TRÊN ANDROID

và đăng nhập vào tài khoản Dropbox, nhớ chọn "allow permissions to your storage"

##### B4: THIẾT LẬP TRÊN DROPSYNC

- Vào SYNCED FOLDERS  
- Chọn Add Folders  
- Remote folder in cloud storage: chọn cái thư mục vault tải lên Dropbox -> Select  
- Local folder in device: chọn nơi lưu vault (nhớ tạo 1 cái thư mục trống)  
- Sync method: two-way  
- Bỏ chọn hết 4 mục ở dưới  
- Save  
- Enable autosync: mình không bật tính năng này để tiết kiệm pin và sẽ tạo 1 widget ở ngoài màn hình để khi nào cần thì sẽ đồng bộ.

##### B5: LẤY DỮ LIỆU TỪ DROPBOX VỀ ĐIỆN THOẠI

Nhấn vào kí hiệu Sync (ở góc phải) để nó lấy dữ liệu trên Dropbox xuống điện thoại

##### B6: MỞ OBSIDIAN TRÊN ĐIỆN THOẠI

- Open folder as vault -> chọn thư mục vừa tải về trên điện thoại

##### B7: TEST THÔI  

> Để đồng bộ thì có thể chọn **Autosync** hoặc Sync thủ công bằng cách nhấn vào nút Sync ở góc phải hoặc nhanh hơn là **tạo 1 widget** ở ngoài màn hình chính.

**Lưu ý nè:**

- Không đặt tên file có chứa emoji
- Ngoài combo Dropbox - Dropsync bạn có thể dùng Google Drive - Autosync, OneDrive - Onesync, cách thiết lập cũng tương tự

🍏 Với người dùng iPhone

- Nếu bạn dùng Mac: sử dụng iCloud làm máy chủ trung gian
- Nếu bạn dùng Window: cách tốt nhất hiện nay là dùng plugin Remotely Save

> Bài [Meta Post - Syncing between Devices - Meta - Obsidian Forum](https://forum.obsidian.md/t/meta-post-syncing-between-devices/20983) giới thiệu nhiều cách đồng bộ các thiết bị với nhau.

*[Thảo luận tại group Obsidian - Second Brain](https://www.facebook.com/groups/594306492570157/posts/644009084266564/)*

> [!Example] Xem thêm
> - [Nếu một ngày Notion biến mất](./neu-mot-ngay-notion-bien-mat.md)