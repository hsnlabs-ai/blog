document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("component-blog-list");
  if (!container) return;

  const posts = container.querySelectorAll(".blog-post-item");
  const paginationContainer = document.getElementById("blog-pagination");
  if (!paginationContainer || posts.length <= 10) return;

  const pageSize = 10;
  const totalPages = Math.ceil(posts.length / pageSize);
  let currentPage = 1;

  const urlParams = new URLSearchParams(window.location.search);
  const pageParam = parseInt(urlParams.get("page") || window.location.hash.replace("#page=", ""), 10);
  if (pageParam && pageParam >= 1 && pageParam <= totalPages) {
    currentPage = pageParam;
  }

  function renderPage(page) {
    currentPage = page;
    const start = (page - 1) * pageSize;
    const end = Math.min(start + pageSize, posts.length);

    posts.forEach((post, idx) => {
      if (idx >= start && idx < end) {
        post.style.display = "";
      } else {
        post.style.display = "none";
      }
    });

    const statusEl = document.getElementById("pagination-status");
    if (statusEl) {
      statusEl.textContent = `Mostrando artigos ${start + 1} a ${end} de ${posts.length}`;
    }

    const prevBtn = document.getElementById("pagination-prev");
    if (prevBtn) {
      prevBtn.disabled = (currentPage === 1);
    }

    const nextBtn = document.getElementById("pagination-next");
    if (nextBtn) {
      nextBtn.disabled = (currentPage === totalPages);
    }

    const numBtns = paginationContainer.querySelectorAll(".pagination-num");
    numBtns.forEach(btn => {
      const target = parseInt(btn.getAttribute("data-target-page"), 10);
      if (target === currentPage) {
        btn.classList.add("active");
        btn.setAttribute("aria-current", "page");
      } else {
        btn.classList.remove("active");
        btn.removeAttribute("aria-current");
      }
    });

    if (window.history.replaceState) {
      const newUrl = page === 1 ? window.location.pathname : `${window.location.pathname}?page=${page}`;
      window.history.replaceState(null, "", newUrl);
    }
  }

  paginationContainer.addEventListener("click", function (e) {
    const btn = e.target.closest("button");
    if (!btn || btn.disabled) return;

    if (btn.id === "pagination-prev" && currentPage > 1) {
      renderPage(currentPage - 1);
      container.scrollIntoView({ behavior: "smooth" });
    } else if (btn.id === "pagination-next" && currentPage < totalPages) {
      renderPage(currentPage + 1);
      container.scrollIntoView({ behavior: "smooth" });
    } else if (btn.classList.contains("pagination-num")) {
      const target = parseInt(btn.getAttribute("data-target-page"), 10);
      if (target && target !== currentPage) {
        renderPage(target);
        container.scrollIntoView({ behavior: "smooth" });
      }
    }
  });

  renderPage(currentPage);
});
