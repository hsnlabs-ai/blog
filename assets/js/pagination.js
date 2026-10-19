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

  function scrollToBlogTop() {
    const header = document.querySelector(".header-nav");
    const headerHeight = header ? header.offsetHeight : 80;
    const targetY = container.getBoundingClientRect().top + window.pageYOffset - headerHeight - 24;
    window.scrollTo({
      top: Math.max(0, targetY),
      behavior: "smooth"
    });
  }

  function renderPage(page, shouldScroll) {
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
      statusEl.textContent = `Showing ${start + 1}–${end} of ${posts.length} posts · Page ${page} of ${totalPages}`;
    }

    const prevBtn = document.getElementById("pagination-prev");
    if (prevBtn) {
      prevBtn.disabled = (currentPage === 1);
    }

    const nextBtn = document.getElementById("pagination-next");
    if (nextBtn) {
      nextBtn.disabled = (currentPage === totalPages);
    }

    const numbersContainer = document.getElementById("pagination-numbers");
    if (numbersContainer) {
      numbersContainer.innerHTML = "";
      
      let pages = [];
      if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) pages.push(i);
      } else {
        if (currentPage <= 4) {
          pages = [1, 2, 3, 4, 5, "...", totalPages];
        } else if (currentPage >= totalPages - 3) {
          pages = [1, "...", totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
        } else {
          pages = [1, "...", currentPage - 1, currentPage, currentPage + 1, "...", totalPages];
        }
      }

      pages.forEach(p => {
        if (p === "...") {
          const dots = document.createElement("span");
          dots.className = "pagination-ellipsis";
          dots.textContent = "…";
          numbersContainer.appendChild(dots);
        } else {
          const btn = document.createElement("button");
          btn.className = `pagination-btn pagination-num ${p === currentPage ? "active" : ""}`;
          btn.setAttribute("data-target-page", p);
          btn.setAttribute("aria-label", `Page ${p}`);
          if (p === currentPage) btn.setAttribute("aria-current", "page");
          btn.textContent = p;
          numbersContainer.appendChild(btn);
        }
      });
    }

    if (window.history.replaceState) {
      const newUrl = page === 1 ? window.location.pathname : `${window.location.pathname}?page=${page}`;
      window.history.replaceState(null, "", newUrl);
    }

    if (shouldScroll) {
      scrollToBlogTop();
    }
  }

  paginationContainer.addEventListener("click", function (e) {
    const btn = e.target.closest("button");
    if (!btn || btn.disabled) return;

    if (btn.id === "pagination-prev" && currentPage > 1) {
      renderPage(currentPage - 1, true);
    } else if (btn.id === "pagination-next" && currentPage < totalPages) {
      renderPage(currentPage + 1, true);
    } else if (btn.classList.contains("pagination-num")) {
      const target = parseInt(btn.getAttribute("data-target-page"), 10);
      if (target && target !== currentPage) {
        renderPage(target, true);
      }
    }
  });

  window.addEventListener("popstate", function () {
    const params = new URLSearchParams(window.location.search);
    const p = parseInt(params.get("page") || "1", 10);
    if (p >= 1 && p <= totalPages && p !== currentPage) {
      renderPage(p, false);
    }
  });

  renderPage(currentPage, false);
});
