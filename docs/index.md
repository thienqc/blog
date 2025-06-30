---
exclude_from_blog: true
---

# Home

Chọn một bài bất kì và khám phá nào 💡

<button onclick="getRandomPost()" 
        style="padding: 10px 15px; background: #3f51b5; color: white; 
               border: none; border-radius: 5px; cursor: pointer; margin-top: 20px;">
  🎲 Bài ngẫu nhiên
</button>

{{ blog_content }}

<script src="{{ 'assets/js/random-post.js' | url }}"></script>