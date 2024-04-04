---
filename: cach-ghep-cac-note-nho-trong-obsidian

share: true
comments: true
tags:
  - obsidian
date: 2023-11-01
URL: 
description:
---
# Cách ghép các note nhỏ trong Obsidian

> [!Question] [Câu hỏi](https://www.facebook.com/photo/?fbid=1344245219528391&set=p.1344245219528391)
> ví dụ mà nếu mình note theo dạng tách file ra thành từng file con nhỏ nhỏ vậy nè, giờ làm sao merge nó lại thành 1 rồi xuất ra không ta.
> 
> Xưa đang note theo 1 file bự cái dùng quick switcher ngồi tách ra hết cái giờ không xuất ra 1 bản PDF được buồn ghê

## Dùng plugin ghép thành file lớn
[Advanced Merger](https://obsidian.md/plugins?id=advanced-merger) : cái này các note phải chung 1 folder

[Merge Notes](https://obsidian.md/plugins?id=merge-notes) : cái này thì mình có thể sắp xếp thứ tự các note đc.

## Embed các note nhỏ vào 1 file
Embed các note nhỏ vào note bự dưới dạng `![[Note 1]]` ...

Sử dụng [clean-embeds.css](https://raw.githubusercontent.com/thienqc/obsidian/main/clean-embeds.css) để export file sạch hơn (Demo 2)

```md
---
cssClasses: clean-embeds
---
```

![](https://i.imgur.com/53FxpTP.png)



> [!Example] Xem thêm
> [Q&A Obisidian](./Q&A-obsidian.md)