function getRandomPost() {
  // Lấy danh sách bài viết từ biến `blog_posts` (nếu dùng plugin blog)
  const posts = [
    {% for post in blog_posts %}
      "{{ post.url }}",
    {% endfor %}
  ];

  // Chọn ngẫu nhiên và chuyển hướng
  if (posts.length > 0) {
    const randomUrl = posts[Math.floor(Math.random() * posts.length)];
    window.location.href = "{{ config.site_url }}" + randomUrl;
  } else {
    alert("Không tìm thấy bài viết nào!");
  }
}