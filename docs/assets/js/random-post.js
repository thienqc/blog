// assets/js/random-post.js
// Defer execution
(function() {
  // Chỉ chạy sau khi page fully loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRandomPost);
  } else {
    setTimeout(initRandomPost, 1000); // Delay 1s để ưu tiên LCP
  }
  
  function initRandomPost() {
    var btn = document.getElementById('random-post-btn');
    if (!btn) return;
    
    // Hiển thị nút
    btn.style.display = 'inline-block';
    
    // Load posts list async
    fetch('/blog/post/list.json')
      .then(response => response.json())
      .then(posts => {
        btn.addEventListener('click', function() {
          var randomIndex = Math.floor(Math.random() * posts.length);
          window.location.href = posts[randomIndex].url;
        });
      })
      .catch(error => {
        console.warn('Could not load posts list:', error);
        btn.style.display = 'none';
      });
  }
})();