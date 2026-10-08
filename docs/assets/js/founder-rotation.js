/**
 * Founder Callout 5-Pair Synchronized Rotation Engine — HSN Labs
 * Cycles through the 5 specific (Photo + Copy) pairings every 10 seconds.
 * Strictly preserves the 90-degree zero-border-radius design and zero-parentheses policy.
 * Directs button clicks to the homepage contact form (#contact / pt/#contact).
 */
(function () {
  'use strict';

  var ROTATION_INTERVAL_MS = 10000;
  var TRANSITION_DURATION_MS = 350;

  var isPt = document.documentElement.lang === 'pt-BR' ||
             window.location.pathname.startsWith('/pt') ||
             window.location.pathname.includes('/pt/');

  var isBlog = window.location.pathname.startsWith('/blog') ||
               window.location.pathname.includes('/blog/');

  var contactBase = isBlog
    ? (isPt ? 'https://hsnlabs.ai/pt/#contact' : 'https://hsnlabs.ai/#contact')
    : (isPt ? '/pt/#contact' : '/#contact');

  // Asset base path detection for local dev vs production
  var assetBase = '/assets/images/author/pool/';
  if (isBlog && window.location.hostname === 'localhost') {
    assetBase = '/blog/assets/images/author/pool/';
  }

  // The 5 pairs defined by user (Photos 1, 6, 9, 8, 5)
  var pairsEN = [
    {
      img: assetBase + 'hugo_01.jpg',
      label: 'Have a project in mind?',
      title: 'Talk to Hugo S. Nascimento, CPTO',
      btn: 'Share Your Project'
    },
    {
      img: assetBase + 'hugo_06.jpg',
      label: "Let's talk about your project",
      title: 'Ask Hugo Soares, Founder & CPTO',
      btn: 'Get in Touch'
    },
    {
      img: assetBase + 'hugo_09.jpg',
      label: 'Building something new?',
      title: 'Share it with Hugo S. Nascimento, CPTO',
      btn: 'Tell Me About It'
    },
    {
      img: assetBase + 'hugo_08.jpg',
      label: 'Want to run an idea by me?',
      title: 'Ask Hugo S. Nascimento, Founder & CPTO',
      btn: 'Send a Message'
    },
    {
      img: assetBase + 'hugo_05.jpg',
      label: 'Need help getting started?',
      title: 'Talk directly with Hugo Soares, CPTO',
      btn: 'Start a Conversation'
    }
  ];

  var pairsPT = [
    {
      img: assetBase + 'hugo_01.jpg',
      label: 'Tem um projeto em mente?',
      title: 'Fale com Hugo S. Nascimento, CPTO',
      btn: 'Compartilhar Projeto'
    },
    {
      img: assetBase + 'hugo_06.jpg',
      label: 'Vamos falar sobre o seu projeto?',
      title: 'Fale com Hugo Soares, Founder e CPTO',
      btn: 'Entrar em Contato'
    },
    {
      img: assetBase + 'hugo_09.jpg',
      label: 'Pensando em construir algo novo?',
      title: 'Compartilhe com Hugo S. Nascimento, CPTO',
      btn: 'Contar Sobre o Projeto'
    },
    {
      img: assetBase + 'hugo_08.jpg',
      label: 'Quer trocar uma ideia sobre seu projeto?',
      title: 'Fale com Hugo S. Nascimento, Founder e CPTO',
      btn: 'Enviar Mensagem'
    },
    {
      img: assetBase + 'hugo_05.jpg',
      label: 'Precisa de ajuda para comecar?',
      title: 'Fale diretamente com Hugo Soares, CPTO',
      btn: 'Iniciar Conversa'
    }
  ];

  var pairs = isPt ? pairsPT : pairsEN;

  // Preload the 5 images
  function preloadImages() {
    for (var i = 0; i < pairs.length; i++) {
      var img = new Image();
      img.src = pairs[i].img;
    }
  }

  if (typeof window.requestIdleCallback === 'function') {
    window.requestIdleCallback(preloadImages);
  } else {
    setTimeout(preloadImages, 2000);
  }

  function hashString(str) {
    var hash = 0;
    for (var k = 0; k < str.length; k++) {
      hash = (hash << 5) - hash + str.charCodeAt(k);
      hash |= 0;
    }
    return Math.abs(hash);
  }

  function initRotation() {
    var callouts = document.querySelectorAll('.hero-founder-callout, .founder-callout-card');
    if (!callouts || callouts.length === 0) return;

    callouts.forEach(function (card, cardIndex) {
      var img = card.querySelector('.founder-avatar-img, img');
      var label = card.querySelector('.founder-meta-title, .founder-callout-label, .founder-meta-label');
      var name = card.querySelector('.founder-meta-name, .founder-callout-name');
      var btn = card.querySelector('.founder-callout-btn, .btn, a');

      if (!img) return;

      var box = card.querySelector('.founder-avatar-box, .founder-callout-avatar');
      var initialIdx = 0;
      if (box && box.getAttribute('data-initial-index') !== null) {
        initialIdx = parseInt(box.getAttribute('data-initial-index'), 10) % pairs.length;
      } else {
        var pathHash = hashString(window.location.pathname || '') + cardIndex * 2;
        initialIdx = pathHash % pairs.length;
      }

      var currentIdx = initialIdx;

      // Apply initial contact href if applicable
      if (btn && btn.tagName === 'A') {
        btn.href = contactBase;
      }

      // Prepare transition styles
      var transStyle = 'opacity ' + TRANSITION_DURATION_MS + 'ms ease-in-out';
      img.style.transition = transStyle;
      if (label) label.style.transition = transStyle;
      if (name) name.style.transition = transStyle;
      if (btn) btn.style.transition = transStyle;

      // Interval rotation loop
      setInterval(function () {
        currentIdx = (currentIdx + 1) % pairs.length;
        var next = pairs[currentIdx];

        // Fade out
        img.style.opacity = '0';
        if (label) label.style.opacity = '0';
        if (name) name.style.opacity = '0';
        if (btn) btn.style.opacity = '0';

        setTimeout(function () {
          img.src = next.img;
          if (label) label.textContent = next.label;
          if (name) name.textContent = next.title;
          if (btn) {
            btn.textContent = next.btn;
            btn.href = contactBase;
          }

          // Fade in
          img.style.opacity = '1';
          if (label) label.style.opacity = '1';
          if (name) name.style.opacity = '1';
          if (btn) btn.style.opacity = '1';
        }, TRANSITION_DURATION_MS);
      }, ROTATION_INTERVAL_MS);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRotation);
  } else {
    initRotation();
  }
})();
