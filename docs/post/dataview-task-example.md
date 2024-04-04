---
filename: dataview-task-example
share: true
comments: true
tags:
  - obsidian
  - dataview
date: 2023-10-28
URL: 
description: 
aliases:
  - Dataview TASK example
---
# Dataview TASK example

> [!question] [Yêu cầu](https://www.facebook.com/groups/obsidian.secondbrain/posts/707585224575616/?comment_id=729045892429549)
> Lọc task chưa hoàn thành từ 2 thư mục, không bao gồm 2 tag, chỉ những task có scheduled, và scheduled quá hạn, sắp xếp theo priority


```md
TASK
FROM "3. Journal" OR "8. Resources/Bank"
WHERE !completed
	AND scheduled
	AND date(scheduled) <= date(today)
	AND none(econtains(tags, "#inbox"))
	AND none(econtains(tags, "#shopping"))
SORT priority
```

`thêm ```dataview`


> [!Example] Xem thêm
> [Dataview](./dataview.md)