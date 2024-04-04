---
filename: dataview
aliases:
  - DATAVIEW
tags:
  - obsidian_plugin
  - dataview
date: 2023-09-17
URL: https://www.facebook.com/groups/594306492570157/posts/707585224575616/
share: true
comments: true
description: chơi đùa với dữ liệu
---
# DATAVIEW
*Chơi đùa với dữ liệu*

Dataview là 1 plugin cực kì mạnh mẽ, giúp ta có thể truy vấn bất kì note nào có trong vault. Bạn có thể:

- Tạo danh sách những quyển sách đang đọc hay muốn đọc
- Liệt kê các công việc phải làm trong ngày
- Tạo bảng hiển thị số lần hoàn thành mục tiêu hàng ngày hoặc hàng tuần
- Bảng theo dõi giấc ngủ
- Tự động thu thập các note liên quan đến ngày hôm nay và hiển thị chúng trong ghi chú hàng ngày
- Tìm các trang không có tag để theo dõi
- Hiển thị sinh nhật hoặc sự kiện sắp tới
- và RẤT NHIỀU ứng dụng khác

## Cấu trúc 

```md
TABLE without ID
	embed(link(Cover,"10")) as Cover,
	file.link as Title,
	Author,
	dateformat(Last_Read,"MMM-dd") as Date
FROM #Books
WHERE Rating="⭐⭐⭐⭐⭐"
SORT date(Last_Read) DESC
LIMIT 25
```

`thêm ```dataview`

### 1. ` ```dataview`
Mục đích là khai báo ở dưới là 1 code block cho dataview
Lưu ý:

- phím bấm \` nằm ở góc trái trên của bàn phím, bên cạnh phím số 1, không phải dấu nháy đơn ‘.
- khi bấm 3 lần dấu \` thì Obsidian sẽ tạo ra 1 code block
- dataview phải được viết thường, không được viết hoa.

### 2. `TABLE`
Kiểu hiện thị dữ liệu. Có 4 dạng dữ liệu

- TABLE: dạng bảng
- LIST: dạng danh sách
- CALENDAR: dạng lịch
- TASK: lọc những note có chứa to do block (`- [ ]`)

Lưu ý:

- TABLE, Table, table hay tAbLe đều đúng 
- TABLE, LIST là như nhau, khác ở chỗ TABLE sẽ chia cột. Bài này mình sẽ nói về TABLE.
- CALENDAR: 

### 3. `embed(link(Cover,"10")) as Cover, file.link as Title, Author, dateformat(Last_Read,"MMM-dd") as Date`
Khai báo những thuộc tính sẽ hiển thị.

Có 2 loại thuộc tính:

- Thuộc tính ẩn: file.link
- Thuộc tính thấy được: Grade
	- Khai báo trong YAML
	- Khai báo trong inline


As : khai bao tên của cột đó, nếu không có thì mặc định là tên thuộc tính (ví dụ: file.link, Author)

Lưu ý:
- Để ý SÓT dấu ”,” cuối dòng

### 4. `FROM #Books`
Cho biết sẽ lấy những note nằm ở đâu, có thể là `“Folder”`, `#tag`, hoặc trong file cụ thể

Nếu không khai báo, mặc định là toàn bộ vault.

### 5. `WHERE Rating="⭐⭐⭐⭐⭐"`
Điều kiện lọc.
Những ví dụ về biểu thức:
- containt ()
- >, <, …

## Cách cài đặt và tài liệu

Để cài đặt dataview, bạn vào `Settings` → `Community plugins` → `Browse` → tìm "dataview" (hoặc nó nằm ngay trên cùng luôn).

Để sử dụng được dataview, bạn cần phải đọc qua hướng dẫn sử dụng tại đây: [https://blacksmithgu.github.io/obsidian-dataview/](https://blacksmithgu.github.io/obsidian-dataview/)

Tài liệu này có thể dài nhưng nó hữu ích giúp bạn có nền tảng để tự viết ra những đoạn . Nhanh hơn, bạn có thể đọc phần "Metadata" và "Structure of a Query", vẫn nên đọc từ trên xuống dưới nhé.

Bạn cũng có thể ghé qua [Basic Dataview Query Builder](https://s-blu.github.io/basic-dataview-query-builder/) để hiểu cách xây dựng 1 query cơ bản.

Khi đã có thể tự viết những query cơ bản, bạn có thể tìm thêm những cách viết nâng cao hơn tại [Dataview Example Vault](https://s-blu.github.io/obsidian_dataview_example_vault/)

Còn đây là bảng kiểm giúp bạn tránh những lỗi sai cơ bản: [checklist](https://docs.google.com/document/d/1P8QljzvtmdpL1mfA2VL5Q972bRAsU1-CLxryVIgH80w/edit)

*[Thảo luận tại group Obsidian - Second Brain](https://www.facebook.com/groups/594306492570157/posts/707585224575616/)*

> [!Example] Xem thêm
> - [DATABASE Notion vs DATAVIEW Obsidian](./database-notion-vs-dataview-obsidian.md)
> - [Test DATAVIEW](./test-dataview.md)
> - [Thư viện sách](./thu-vien-sach-template.md)
> - [Dataview TASK example](./dataview-task-example.md)
> - [Dataview Hiển thị link tới note](./dataview-hien-thi-link-toi-note.md)