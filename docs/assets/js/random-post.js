window.getRandomPost = async function() {
  try {
    // Hiệu ứng loading
    const btn = document.querySelector('.md-header__random button');
    if (btn) {
      btn.style.animation = 'spin 1s linear infinite';
      btn.style.transformOrigin = 'center';
    }

    const res = await fetch('/blog/sitemap.xml');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    
    const text = await res.text();
    const parser = new DOMParser();
    const xml = parser.parseFromString(text, "application/xml");
    
    const urls = Array.from(xml.querySelectorAll("url loc"))
      .map(loc => loc.textContent.trim())
      .filter(url => url.includes("/post/"));

    if (!urls.length) throw new Error("Không tìm thấy bài viết");
    
    window.location.href = urls[Math.floor(Math.random() * urls.length)];
    
  } catch (error) {
    console.error("Lỗi:", error);
    alert(`Lỗi: ${error.message}`);
  } finally {
    const btn = document.querySelector('.md-header__random button');
    if (btn) btn.style.animation = '';
  }
};

// Thêm animation
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);