---
filename: database-notion-vs-dataview-obsidian
URL: 

date: 2023-06-09
link: https://www.facebook.com/groups/594306492570157/posts/654784003189072/
tags:
  - obsidian
  - notion
description: Cái nhìn tổng quan về Notion và Obsidian.
share: true
comments: true
aliases:
  - DATABASE Notion vs DATAVIEW Obsidian
---
# DATABASE Notion vs DATAVIEW Obsidian
*Bài viết này sẽ giúp bạn có cái nhìn tổng quan về Notion và Obsidian.* 

![](https://i.imgur.com/vrikCw3.png)

Database là nơi chứa tất cả note của bạn. Cách tiếp cận của Notion là từ đầu, bạn sẽ tạo ra các database và cấu trúc chúng, sau đó sẽ đặt các note vào vị trí tương ứng. Điều này tưởng chừng đơn giản, và dễ hiểu giống như đặt một quyển sách vào đúng giá sách. Tuy nhiên, đời không như mơ, một ngày nào đó, xuất hiện một con cừu đen không biết thuộc đàn nào. Ví dụ, mình có một note về `bệnh Lupus`, mình sẽ rất bối rối khi không biết bỏ note này vào "Nội khoa", "Da liễu", hay "Nội tiết", vì đây là một bệnh hệ thống, liên quan tới nhiều hệ cơ quan. Ngoài ra còn rất nhiều trường hợp khác khi mà 1 note có thể thuộc nhiều database khác nhau. Tới lúc này, bạn sẽ nghĩ tới việc bỏ chung các note vào cùng 1 master database và phân loại chúng. Đây là cách tiếp cận của Obsidian, khi mà xem các note trong 1 vault là cùng chung 1 database. [Dataview](./dataview.md) là 1 plugin giúp truy vấn tới các note mình cần. Ban đầu bạn cứ thoải mái tạo note, không cần quan tâm nó ở chỗ nào, chỉ cần đặt cho nó các tag cần thiết. Khi nào cần, sử dụng dataview để truy vấn note bất kì lúc nào, và liên kết chúng với nhau một cách dễ dàng. Nghe giống bộ não nhỉ.

Về cách hiển thị, Notion có 6 view chính là Table, List, Calendar, Board, Gallery, Timeline và chuyển đổi qua lại dễ dàng. Đây là điều mình rất thích ở Notion, khi mà có thể xử lí các note trong các kiểu khác nhau. Còn đối với dataview, bạn chỉ có 4 view: Table, List, Calendar, Task. Những cách hiển thị khác (Board, Gallery, Timeline) cần phải cài dùng plugin. Và để chuyển đổi giống Notion, Obisidian cũng có plugin tên là Project, tuy nhiên, trải nghiệm các nhân của mình thì vẫn không so được với Notion.

Về thuộc tính, Notion gọi là property, bạn chỉ có thể tạo nó ở đầu trang, và nó sẽ hiện ở tất cả các note cùng chung 1 database. Nếu bạn xây dựng master database, thì sẽ có rất nhiều thuộc tính cần không thiết nằm trong note khác. Còn với Obsidian, bạn có thể đặt nó ở đầu trang (Frontmatter YAML), hoặc ở bất kì đâu trong phần nội dung (inline), và chỉ cần gọi nó ra khi cần thiết, điều này giúp note của bạn gọn gàng và tự nhiên hơn. Tuy nhiên, Notion có thể dễ dàng chỉnh sửa các giá trị thuộc tính trực tiếp, hàng loạt. Còn với Obsidian thì bạn cần một số thủ thuật.

Xét về tốc độ xử lí, mình có làm một bài test nhỏ: Lọc những quyển sách mình đã đọc trong năm 2023. Notion ra kết quả sau 3-4 giây. Còn Obisidian, chưa tới 1 giây (vừa bấm ENTER) đã có kết quả. Điều này khá dễ hiểu khi mà Notion sử dụng đám mây lưu trữ, mà còn phải ôm đồm nhiều tính năng. Còn Obsidian thì xử lí file trên máy tính, và chỉ cần truy vấn dữ liệu.

Về bản chất thì mỗi block của Notion (một đoạn text, một hình ảnh, một heading,...) là một item trong master database chứ ko phải mỗi page. Bản chất mỗi page của Notion là một index của các block nhỏ lại với nhau. Do đó mỗi page càng dài thì thời gian query, open càng lâu.

Giao diện của Notion mình đánh giá là khá thân thiện với người dùng. Còn dataview thì bạn phải hiểu được các câu lệnh để có thể sử dụng.

Chỉ có Notion hỗ trợ API, giúp kết nối với nhiều hệ thống khác hơn. Ngoài ra Notion còn có relation, rollup, formula, giúp xử lí note theo nhiều cách khác nhau. Những điều này Obsidian vẫn còn nhiều hạn chế.

Nói tóm lại, mình thấy Notion được xây dựng thêm hướng app quản lí, còn Obsidian là một app ghi chú tuyệt vời. Cả 2 đều sẽ có những ưu nhược điểm riêng phù hợp với từng đối tượng khác nhau. Hi vọng qua bài viết này, bạn có thể sử dụng công cụ phù hợp với nhu cầu của mình.
Nếu có bất kì thắc mắc hay thảo luận, hãy để lại bình luận nhé. Chúc bạn một ngày tốt lành.

*[Bài viết thuộc group Obsidian - Second Brain](https://www.facebook.com/groups/594306492570157/posts/654784003189072/)*

> [!Example] Xem thêm
> - [DATAVIEW](./dataview.md)