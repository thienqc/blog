---
filename: thay-doi-font-mot-doan-text-trong-obsidian

share: true
comments: true
tags:
  - obsidian
date: 2023-10-16
URL: 
description:
---
# Thay đổi font một đoạn text trong Obsidian

> [!question] [Câu hỏi](https://www.facebook.com/groups/obsidian.secondbrain/posts/722968966370575/)
> Mọi người cho em hỏi: có cách nào để thay đổi font chữ của 1 đoạn text trong note không ạ?
> 
> Note của em có cả tiếng Trung & tiếng Việt. Font chữ mặc định trong Appearance là Times New Roman, nên những chữ tiếng Trung hiển thị khá xấu. Em muốn tìm cách chọn 1 font khác cho từng đoạn text tiếng Trung ạ.
## Dùng quote block

[raw.githubusercontent.com/thienqc/obsidian/main/Font quote.md](https://raw.githubusercontent.com/thienqc/obsidian/main/Font%20quote.md)

```css
/* for editor */
.cm-quote {
    font-family: 'Noto Sans Traditional Chinese';
  }

/* for preview */
  .markdown-preview-view blockquote {
    font-family: 'Noto Sans Traditional Chinese';
  }
```

Tạo 1 file css, copy đoạn mã trên vào file css, bỏ vào thư mục [CSS snipper](https://help.obsidian.md/Extending+Obsidian/CSS+snippets) của vault. Kích hoạt nó lên.
Khi sử dụng tạo [quote block](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax#Quotes): `>`

## Dùng callout

Tương tự quote block

[Customize callouts](https://help.obsidian.md/Editing+and+formatting/Callouts#Customize+callouts)
## Dùng html-tag

Cài plugin [Templater](https://github.com/SilentVoid13/Templater):

Tải [file này](https://raw.githubusercontent.com/thienqc/obsidian/main/CN%20font%20template.md) về bỏ vào thư mục template: 

```html
<p style="font-family: 'Noto Sans Traditional Chinese'"> <% tp.file.selection() %> </p>
```

Tạo hotkey cho nó trong mục Template Hotkeys

Khi sử dụng thì bôi đen đoạn chữ cần đổi font, rồi dùng hotkey là ok.

## Dùng tag

[Format text based on header or tag - Help - Obsidian Forum](https://forum.obsidian.md/t/format-text-based-on-header-or-tag/33754/4)

## Sử dụng 2 bộ font bằng CSS

Times New Roman không có ký tự CJK nên Obsidian fallback về 1 cái default CJK font của máy. Thay vì chỉ target blockquote như Thiện để cập ở trên thì bạn có thể sử dụng cái snippet này để hoạt động ở mọi nơi và sử dụng mix hai font trong cùng 1 đoạn luôn.

```css

/* for editor*/
.markdown-source-view .cm-editor .cm-scroller, .cm-quote {
    font-family: 'Times New Roman', 'tên font tiếng Trung' !important; 
  }
 
/* for preview*/
.markdown-preview-view, blockquote {
    font-family: 'Times New Roman', 'tên font tiếng Trung' !important; 
  }
```

## Sử dụng 2 bộ font trong Settings

Dựa trên cmt trên, thì mình nghĩ cách này là tối ưu nhất, không cần thay đổi CSS Snippet

Settings → Apprearance → Font → Text font → Manage

![](https://i.imgur.com/0tumERv.png)



> [!Example] Xem thêm
> [Q&A Obisidian](./Q&A-obsidian.md)