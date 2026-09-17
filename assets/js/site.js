/* Gộp 3 script tuỳ chỉnh (random-post, theme-bfcache-sync, tag-cloud) vào
   1 file để giảm số HTTP request cuối trang — mỗi file tách riêng trước
   đây chỉ vài KB nhưng dưới điều kiện mạng chậm/độ trễ cao, mỗi request
   thêm vẫn tốn thời gian xếp hàng riêng của nó. */

// ===== random-post.js =====
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

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('random-post-btn');
  if (btn) btn.onclick = window.getRandomPost;
});

// ===== theme-bfcache-sync.js =====
// Material chỉ đọc localStorage["__palette"] và set data-md-color-* trên
// <body> một lần lúc trang tải. Khi quay lại trang bằng nút Back và trình
// duyệt phục hồi từ bfcache thay vì tải lại, đoạn bootstrap đó không chạy
// lại nên theme hiển thị có thể không khớp với lựa chọn mới nhất (vd đã đổi
// theme ở một trang khác như ebook.html rồi bấm Back quay về đây).
(function () {
  function applyStoredPalette() {
    try {
      var scope = new URL(".", location);
      var raw = localStorage.getItem(scope.pathname + ".__palette");
      if (!raw) return;
      var palette = JSON.parse(raw);
      if (!palette || !palette.color) return;
      Object.keys(palette.color).forEach(function (key) {
        document.body.setAttribute("data-md-color-" + key, palette.color[key]);
      });
    } catch (e) { /* ignore */ }
  }
  window.addEventListener("pageshow", function (e) {
    if (e.persisted) applyStoredPalette();
  });
})();

// ===== tag-cloud.js =====
// Biến grid tag phẳng (từ mkdocs-blogging-plugin) trên trang /tags/ thành
// tag cloud thật: cỡ chữ theo số bài viết (thang log, vì phân bố rất lệch),
// sắp lại theo alphabet cho dễ tìm. Không đụng tới danh sách tag nhỏ ở
// cuối mỗi bài viết (cùng class nhưng khác trang).
(function () {
  function isTagsIndexPage() {
    return /\/tags\/?$/.test(window.location.pathname);
  }

  function applyTagCloud() {
    if (!isTagsIndexPage()) return;
    const grid = document.querySelector(".blogging-tags-grid");
    if (!grid || grid.classList.contains("tag-cloud-ready")) return;

    const links = Array.from(grid.querySelectorAll(".blogging-tag"));
    if (links.length === 0) return;

    const counts = new Map();
    links.forEach((link) => {
      const id = decodeURIComponent((link.getAttribute("href") || "").split("#")[1] || "");
      const heading = document.getElementById(id);
      let count = 0;
      if (heading) {
        let el = heading.nextElementSibling;
        while (el && el.tagName !== "H3") {
          if (el.tagName === "LI") count++;
          el = el.nextElementSibling;
        }
      }
      counts.set(link, count || 1);
    });

    const values = Array.from(counts.values());
    const min = Math.min(...values);
    const max = Math.max(...values);
    const MIN_SIZE = 0.75;
    const MAX_SIZE = 1.9;

    links.forEach((link) => {
      const count = counts.get(link);
      const ratio =
        max === min ? 0 : (Math.log(count) - Math.log(min)) / (Math.log(max) - Math.log(min));
      const size = MIN_SIZE + (MAX_SIZE - MIN_SIZE) * ratio;
      link.style.fontSize = size.toFixed(2) + "rem";
      link.style.fontWeight = ratio > 0.6 ? "700" : ratio > 0.3 ? "500" : "400";
      link.title = count + " bài viết";
    });

    links
      .slice()
      .sort((a, b) => a.textContent.localeCompare(b.textContent, "vi", { sensitivity: "base" }))
      .forEach((link) => grid.appendChild(link));

    grid.classList.add("tag-cloud-ready");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyTagCloud);
  } else {
    applyTagCloud();
  }
})();
