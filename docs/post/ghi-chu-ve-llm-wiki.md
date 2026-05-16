---
share: true
comments: true
filename: ghi-chu-ve-llm-wiki
description: AI và não hai
tags:
  - PKM
date: 2026-05-16
---
# Ghi chú về "LLM Wiki - Karpathy"  
  
Gần đây có xuất hiện một tài liệu tên là "[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)" của tác giả Andrej Karpathy (T4/2026). Chuyện thì cũng không có gì đáng nói nếu không có những 'thánh lùa gà' nổi lên, và họ dấy lên một làn sóng khiến nhà nhà áp dụng AI cách-triệt-để vào trong việc *"chế tạo"* não hai của riêng mình. Do đó mình cũng mon men vào tìm hiểu gốc gác ra sao. Sau đây là vài ghi chú, suy nghĩ của mình trong lúc đọc tài liệu LLM Wiki của tác giả Karpathy *(cập nhật 16/05/2026)*.  
  
---  
  
> # LLM Wiki  
> A pattern for building personal knowledge bases using LLMs.  
  
Hình như ở đây có sự nhập nhằng giữa ==wiki== và ==personal knowledge bases==. Hãy cùng xem lại 2 định nghĩa:  
  
- A wiki (/ˈwɪki/ ⓘ WIK-ee) is a form of hypertext publication on the internet which is ==collaboratively== edited and managed by its audience directly through a web browser.  
- A personal knowledge base (PKB) is an electronic tool used by an ==individual== to express, capture, and later retrieve personal knowledge.  
  
Điểm khác biệt ở đây là "nhiều người" vào "một người". Theo mình thì wiki là một dạng bách khoa toàn thư mở mà mọi người có thể cùng nhau vào đọc và cùng chỉnh sửa, duy trì, nó mang tính cộng đồng. Điển hình là [Wikipedia](https://www.wikipedia.org/). Còn PKB là kho tri thức cá nhân, được tạo ra cho chính cá nhân đó, và nó mang nhiều tính cá nhân (bạn đặt vào đó cảm xúc, suy nghĩ, trải nghiệm của bản thân). Một ví dụ là [notes.andymatuschak.org](https://notes.andymatuschak.org/), tuy được chia sẻ công khai nhưng đây chỉ là thứ yếu.  
  
Xem thêm: [Is it a Wikipedia? — Zettelkasten Forum](https://forum.zettelkasten.de/discussion/2899/is-it-a-wikipedia)  
  
Bỏ qua sự nhầm lẫn này, mình nghĩ Karpathy muốn nhấn mạnh tới việc các ghi chú được liên kết với nhau để tạo thành một hệ thống tri thức (dù là wiki hay PKB), và việc duy trì/bảo trì được hệ thống này tốn rất nhiều công sức.  
  
Ý tưởng của Karpathy là sử dụng LLM để nó đọc bất kì cái gì bạn đưa vào vault, xử lí thành các mảnh thông tin và liên kết nó với các ghi chú khác.  
  
Mình không bàn về kỹ thuật, nhưng mình đặt ra một câu hỏi **"vậy vai trò của con người là gì trong suốt quá trình này?"**  
  
> The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.  
  
*Công việc của con người là chọn lọc nguồn thông tin, định hướng phân tích, đặt ra những câu hỏi hay và suy nghĩ về ý nghĩa của tất cả những điều đó. Công việc của LLM là tất cả những việc còn lại.*  
  
Những việc còn lại là:  
  
> It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis.  
  
*Nó đọc dữ liệu, trích xuất thông tin chính và tích hợp vào wiki hiện có — cập nhật các trang đã có, sửa đổi tóm tắt chủ đề, ghi chú những điểm dữ liệu mới mâu thuẫn với các thông tin cũ, củng cố hoặc thách thức sự tổng hợp đang phát triển.*  
  
Với mình, việc đọc từng mẫu thông tin, tự chắc lọc, tóm tắt nó, ghi lại với giọng văn của chính mình mới là cách truy tầm tri thức đúng đắn.  
  
Trong [Tôi tự học](./toi-tu-hoc.md), học giả Nguyễn Duy Cần có viết “Con chiên ăn cỏ, đâu phải để nhả cỏ, mà là để biến thành những bộ lông mướt đẹp. Con tằm ăn dâu, đâu phải để nhả dâu, mà là để nhả tơ”   
  
Nếu chỉ sử dụng những thứ AI "nhả cho", phải chăng mình đang hạ phẩm cách của con người ngang với máy móc?  
  
Đừng sợ việc không cập nhật được ghi chú: liên kết ghi chú này với ghi chú nào khác đây? ghi chú cũ có sai không? --> Đừng suy nghĩ quá nhiều về việc này, hãy thật sự làm việc với chính ghi chú của bản thân, mấy cái liên kết sẽ tự xuất hiện thôi, tiếp tục làm điều này nhiều lần, theo thời gian các ý tưởng được kết nối với nhau theo những cách đáng ngạc nhiên và vault lúc đó mới trở thành não-hai. Nếu bạn thấy còn mơ hồ chỗ này, hãy dùng [Map of Content (MOC)](./map-of-content-moc.md) nó sẽ giúp định hướng ghi chú cho bạn.  
  
Cuối cùng, mình thấy Karpathy đưa ra một ý tưởng rất hay, nhưng nó chỉ phù hợp trong việc tạo ra wiki (cho nhóm/công ty/cộng đồng) hơn là tạo một hệ thống tri thức cho cá nhân. Chính cái việc nhâm nhi từng mẩu kiến thức mới là thứ thú vị trên con đường tri thức.