---
share: true
comments: true
filename: dataview-hien-thi-link-toi-note
aliases:
  - Dataview Hiển thị link tới note
description: 
tags:
  - dataview
  - obsidian
date: 2024-01-07
URL:
---
# Dataview Hiển thị link tới note

> [!question] Yêu cầu
> Hiển thị những note được link kết tới ghi chú

## Giải pháp

Sử dụng [metadata trong page](https://blacksmithgu.github.io/obsidian-dataview/annotation/metadata-pages/#implicit-fields), cụ thể:

- `file.outlinks`: tất cả các liên kết gửi đi từ tệp này, nghĩa là tất cả các liên kết mà tệp chứa.
- `file.inlinks`: tất cả các liên kết đến tệp này, nghĩa là tất cả các tệp có chứa liên kết đến tệp này.

![](https://i.imgur.com/d4U3t3d.png)


Nếu chỉ sử dụng `file.outlinks + file.inlinks` thì sẽ xảy ra trường hợp nó sẽ liệt kê luôn những file hình ảnh được embed trong note.

=> Sử dụng `filter(file.outlinks, (x) => !contains(string(x), "png"))` để loại bỏ những link có đuôi là png, mở rộng ra nếu sử dụng jpg, jpge, gif...

## Query
`thêm ```dataview`

```md
TABLE
	filter(file.outlinks, (x) => !contains(string(x), "png")) + file.inlinks as "Links"
FROM #journal
SORT file.cday ASC
```


> [!Example] Xem thêm
> [Dataview](./dataview.md)