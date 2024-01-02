---
share: true
tags:
  - obsidian
date: 2023-10-13
URL: 
description: 
---

# Obsidian Search

Chi tiết xem ở [Search - Obsidian Help](https://help.obsidian.md/Plugins/Search)

## Một số ví dụ
### Property là Checkbox

Cú pháp bình thường cho property sẽ là `[property]` ví dụ: `["type":book]`.

Tuy nhiên nếu property là checkbox hay dạng true/false thì dùng cú pháp này không được. Lúc này ta sẽ dùng cú pháp tìm cụm từ.

Cụ thể là `"share: true"`

### Phân biệt line và section
Định nghĩa:

- Section: văn bản giữa 2 tiêu đề
- Line: dòng

Tức là Section có thể gồm nhiều Line.

Khi tìm bằng `line:` thì các từ khoá phải trên cùng 1 dòng.

Khi tìm bằng `section:` thì các từ khoá có thể trên nhiều dòng khác nhau.


![](https://i.imgur.com/cCkQ0tR.png)
