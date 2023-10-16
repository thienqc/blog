---
share: true
tags:
  - obsidian
date: 2023-10-16
URL: 
description: 
---

# Thay đổi font một đoạn text trong Obsidian

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

> [!Example] Xem thêm
> [Q&A Obisidian](./Q&A%20Obisidian.md)