window.getRandomPost = async function () {
  try {
    const res = await fetch('/blog/sitemap.xml');
    const text = await res.text();

    const parser = new DOMParser();
    const xml = parser.parseFromString(text, "application/xml");
    const urls = Array.from(xml.querySelectorAll("url loc"))
      .map(loc => loc.textContent)
      .filter(url => url.includes("/post/")); // Lọc bài viết

    if (urls.length === 0) {
      alert("Không tìm thấy bài viết nào trong sitemap!");
      return;
    }

    const randomUrl = urls[Math.floor(Math.random() * urls.length)];
    window.location.href = randomUrl;
  } catch (error) {
    console.error("Lỗi khi tải sitemap:", error);
    alert("Không thể lấy bài viết ngẫu nhiên!");
  }
};

// Gán sự kiện khi DOM sẵn sàng
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('random-post-btn');
  if (btn) btn.onclick = window.getRandomPost;
});
