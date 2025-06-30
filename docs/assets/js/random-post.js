// docs/javascripts/random-post.js
window.getRandomPost = function() {
  // Lấy danh sách bài viết từ thẻ <script type="application/json">
  const postsData = document.getElementById('posts-data');
  if (!postsData) return alert("Không tìm thấy dữ liệu bài viết!");
  
  const posts = JSON.parse(postsData.textContent);
  if (posts.length > 0) {
    const randomUrl = posts[Math.floor(Math.random() * posts.length)];
    window.location.href = randomUrl;
  } else {
    alert("Không tìm thấy bài viết nào!");
  }
};

// Gán sự kiện
document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('random-post-btn');
  if (btn) btn.onclick = window.getRandomPost;
});