---
share: true
comments: true
filename: comment-system
aliases:
  - Hệ thống bình luận cho blog
  - Comment System
description: 
tags:
  - tech
date: 2024-04-04
URL: 
---
# Hệ thống bình luận cho blog
Trầy trật mãi mới kích hoạt được hệ thống bình luận cho blog này.

![](https://i.imgur.com/fZRJmZX.png)


Dựa trên [bài hướng dẫn này](https://squidfunk.github.io/mkdocs-material/setup/adding-a-comment-system/), có một số vấn đề mình gặp phải

## Đặt tên thư mục "Overrides" thành "Override"
Sau khi tạo được file `comments.html` theo hướng dẫn, mình cần đặt nó vào thư mục `overrides/partials/`. Vấn đề ở đây là do trước đó mình clone từ một repo để tạo blog, và repo này lại để tên thư mục là "override" (thiếu chữ s) cho nên `custom_dir: overrides` không thể nhận diện được.

Lỗi này fix đơn giản là đổi tên lại cho đúng yêu cầu là được.

## Không sử dụng được meta plugin
[Meta plugin](https://squidfunk.github.io/mkdocs-material/plugins/meta/) là một plugin của Material for MkDocs (tức là không cần cài đặt thêm), để đặt metadata vào tất cả file trong một thư mục cụ thể. Nghĩa là mình muốn đặt `comments: true` vào trong tất cả note của thư mục `docs/post` (là nơi chứa toàn bộ bài viết trên blog này) mà không cần thêm thủ công.

Nghe có vẻ hay hay, nhưng vấn đề là tới thời điểm hiện tại (04/04/2024, ngày đẹp ghê), plugin này vẫn đang được phát triển, tức là chỉ có những người Insider mới được sử dụng. Do đó mình không sử dụng được nó mà phải thêm thủ công vào mỗi bài viết.

## Tóm lại
Và còn vô số lỗi khác mà mình mày mò sửa trong quá trình thêm hệ thống bình luận này. Dù mình đọc đi đọc lại docs nhiều lần nhưng mà do đọc không kĩ, bỏ sót những từ quan trọng, không hiểu cấu trúc của blog nên mắc phải những lỗi như trên.

Nếu có bất kì bình luận này, vui lòng để lại bình luận bên dưới :))