(function () {
  document.addEventListener('click', function (event) {
    var link = event.target.closest('[data-canvas-cta]');
    if (!link) return;

    var slug = link.getAttribute('data-article-slug') || '';
    var lang = link.getAttribute('data-page-lang') || 'en';
    var ctaType = link.getAttribute('data-canvas-cta') || 'banner_modelo_1';
    var href = link.getAttribute('href') || '';

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'canvas_banner_click', {
        event_category: 'blog_conversion',
        event_label: slug,
        cta_variant: ctaType,
        page_language: lang,
        destination_url: href,
        transport_type: 'beacon'
      });
    }
  });
})();
