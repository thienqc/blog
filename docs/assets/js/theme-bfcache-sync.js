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
