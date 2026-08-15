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
