---
filename: tao-mot-trang-blog-don-gian-bang-obsidian-va-mkdocs
URL: 

share: true
comments: true
tags:
  - tech
  - obsidian
date: 2023-09-22
description: Xây dựng bộ não thứ hai
extra: 
aliases:
  - Tạo một trang blog đơn giản bằng Obsidian và MkDocs
---
# Tạo một trang blog đơn giản bằng Obsidian và MkDocs

![](https://i.imgur.com/pIrAiBr.png)

Để làm được điều này có 2 bước:
## B1. Tạo 1 trang web tĩnh bằng MkDocs
Ở đây mình sẽ dùng [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). MkDocs có thể dễ dàng tạo 1 trang web tĩnh, dễ sử dụng và dễ sửa đổi. Trong đó Material là theme được đánh giá tốt nhất và nó phù hợp với việc tạo một trang blog tối giản, tập trung vào nội dung.

Mình dùng Github là nơi chứa trang web và chỉ cần vài bước là có ngay một trang web rồi. Bạn chỉ cần clone những template có sẵn về repo là có ngay 1 trang web để tuỳ chỉnh rồi. Mình dùng [theme này](https://github.com/liang2kl/mkdocs-blogging-plugin-bootstrap) và chỉnh sửa file `mkdocs.yml` cho phù hợp.
## B2. Sử dụng Obsidian để quản lí nội dung
Sau khi có được một trang web, nội dung của nó sẽ chứa trong thư mục `docs` dưới các file .md. Do đó, mình sẽ dùng plugin [GitHub Publisher](https://github.com/ObsidianPublisher/obsidian-github-publisher) để đồng bộ nội dung trong vault của mình và trên github. 
## Đánh giá
Ưu điểm:

- Giao diện tối giản, tập trung vào nội dung
- Dễ dàng chỉnh sửa nội dung
- Hỗ trợ `[[wikilink]]`
- Miễn phí

Nhược điểm:

- Khó làm nếu không quen lập trình
- Không tối ưu SEO bằng các nền tảng khác

Mình dùng cách này để tạo ra trang [thienqc's blog](https://thienqc.github.io/blog/) như một bộ não thứ hai. Các bạn có thể ghé vào và khám phá. Nó sẽ được cập nhật hằng ngày và không ngừng lớn lên.

*[Thảo luận tại group Obsidian - Second Brain](https://www.facebook.com/groups/594306492570157/posts/709835517683920/)*