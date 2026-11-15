document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("component-blog-list");
  if (!container) return;

  const allPosts = Array.from(container.querySelectorAll(".blog-post-item"));
  const paginationContainer = document.getElementById("blog-pagination");
  if (!paginationContainer || allPosts.length === 0) return;

  const isPt = (document.documentElement.lang || "").toLowerCase().startsWith("pt") ||
               window.location.pathname.indexOf("/pt/") !== -1;

  const pageSize = 10;
  const urlParams = new URLSearchParams(window.location.search);
  const activeCat = urlParams.get("cat") || "";
  const activeTag = urlParams.get("tag") || "";

  const filteredPosts = allPosts.filter((post) => {
    if (activeCat) {
      const cat = post.getAttribute("data-category") || "";
      if (cat !== activeCat) return false;
    }
    if (activeTag) {
      const tags = (post.getAttribute("data-tags") || "").split(",").map((t) => t.trim().toLowerCase());
      if (!tags.includes(activeTag.toLowerCase())) return false;
    }
    return true;
  });

  const totalPages = Math.max(1, Math.ceil(filteredPosts.length / pageSize));
  let currentPage = 1;
  const pageParam = parseInt(urlParams.get("page") || window.location.hash.replace("#page=", ""), 10);
  if (pageParam && pageParam >= 1 && pageParam <= totalPages) {
    currentPage = pageParam;
  }

  function updateNavButtonsText() {
    const prevBtn = document.getElementById("pagination-prev");
    const nextBtn = document.getElementById("pagination-next");
    if (prevBtn) {
      const span = prevBtn.querySelector("span");
      if (span) span.textContent = isPt ? "Anterior" : "Prev";
      prevBtn.setAttribute("aria-label", isPt ? "Página anterior" : "Previous page");
    }
    if (nextBtn) {
      const span = nextBtn.querySelector("span");
      if (span) span.textContent = isPt ? "Próxima" : "Next";
      nextBtn.setAttribute("aria-label", isPt ? "Próxima página" : "Next page");
    }
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
    const end = Math.min(start + pageSize, filteredPosts.length);
    const visibleSet = new Set(filteredPosts.slice(start, end));

    allPosts.forEach((post) => {
      post.style.display = visibleSet.has(post) ? "" : "none";
    });

    const statusEl = document.getElementById("pagination-status");
    if (statusEl) {
      if (filteredPosts.length === 0) {
        statusEl.textContent = isPt ? "Nenhum post encontrado neste filtro" : "No posts matched this filter";
      } else if (isPt) {
        statusEl.textContent = `Mostrando ${start + 1}–${end} de ${filteredPosts.length} posts · Página ${page} de ${totalPages}`;
      } else {
        statusEl.textContent = `Showing ${start + 1}–${end} of ${filteredPosts.length} posts · Page ${page} of ${totalPages}`;
      }
    }

    const prevBtn = document.getElementById("pagination-prev");
    if (prevBtn) {
      prevBtn.disabled = (currentPage === 1);
    }

    const nextBtn = document.getElementById("pagination-next");
    if (nextBtn) {
      nextBtn.disabled = (currentPage === totalPages);
    }

    paginationContainer.style.display = filteredPosts.length <= pageSize ? "none" : "";

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
          btn.setAttribute("aria-label", isPt ? `Página ${p}` : `Page ${p}`);
          if (p === currentPage) btn.setAttribute("aria-current", "page");
          btn.textContent = p;
          numbersContainer.appendChild(btn);
        }
      });
    }

    if (window.history.replaceState && !activeCat && !activeTag) {
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

  updateNavButtonsText();
  renderPage(currentPage, false);
});
