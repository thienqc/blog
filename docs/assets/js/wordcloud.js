document.addEventListener("DOMContentLoaded", function() {
    // Chỉ chạy script nếu đang ở trang Tags index
    const tagLinks = document.querySelectorAll(".md-typeset .md-tag-list a.md-tag");
    if (tagLinks.length === 0) return;

    tagLinks.forEach(tag => {
        const text = tag.textContent;
        // Sử dụng Regex để tìm số lượng bài viết nằm trong dấu ngoặc, ví dụ: "AI (12)"
        const match = text.match(/\((\d+)\)/);
        
        if (match) {
            const count = parseInt(match[1], 10);
            
            // Công thức tính toán kích cỡ font dựa trên số lượng bài viết (tối thiểu 0.8rem, tối đa 2.5rem)
            let fontSize = 0.8 + (count * 0.15);
            if (fontSize > 2.5) fontSize = 2.5; 
            
            tag.style.fontSize = fontSize + "rem";
            
            // Tăng độ đậm cho các từ khóa xuất hiện nhiều
            if (count > 5) tag.style.fontWeight = "700";
            if (count > 2 && count <= 5) tag.style.fontWeight = "500";
        }
    });
});