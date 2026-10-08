/**
 * Founder Callout 5-Pair Synchronized Rotation Engine — HSN Labs
 * Strictly standardizes the two CTA parts:
 *   - Subtitle: "Share it with Hugo, CPTO" (PT: "Compartilhe com Hugo, CPTO")
 *   - Button: "Start a Conversation" (PT: "Iniciar Conversa")
 * Rotating ONLY the Photo (1, 6, 9, 8, 5) and the Title Question every 10 seconds.
 * Strictly preserves 90-degree zero-border-radius design and zero-parentheses policy.
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

  var assetBase = '/assets/images/author/pool/';
  if (isBlog && window.location.hostname === 'localhost') {
    assetBase = '/blog/assets/images/author/pool/';
  }

  // The 5 pairs with standardized subtitle and button
  var pairsEN = [
    {
      img: assetBase + 'hugo_01.jpg',
      label: 'Have a project in mind?',
      title: 'Share it with Hugo, CPTO',
      btn: 'Start a Conversation'
    },
    {
      img: assetBase + 'hugo_06.jpg',
      label: "Let's talk about your project",
      title: 'Share it with Hugo, CPTO',
      btn: 'Start a Conversation'
    },
    {
      img: assetBase + 'hugo_09.jpg',
      label: 'Building something new?',
      title: 'Share it with Hugo, CPTO',
      btn: 'Start a Conversation'
    },
    {
      img: assetBase + 'hugo_08.jpg',
      label: 'Want to run an idea by me?',
      title: 'Share it with Hugo, CPTO',
      btn: 'Start a Conversation'
    },
    {
      img: assetBase + 'hugo_05.jpg',
      label: 'Need help getting started?',
      title: 'Share it with Hugo, CPTO',
      btn: 'Start a Conversation'
    }
  ];

  var pairsPT = [
    {
      img: assetBase + 'hugo_01.jpg',
      label: 'Tem um projeto em mente?',
      title: 'Compartilhe com Hugo, CPTO',
      btn: 'Iniciar Conversa'
    },
    {
      img: assetBase + 'hugo_06.jpg',
      label: 'Vamos falar sobre o seu projeto?',
      title: 'Compartilhe com Hugo, CPTO',
      btn: 'Iniciar Conversa'
    },
    {
      img: assetBase + 'hugo_09.jpg',
      label: 'Pensando em construir algo novo?',
      title: 'Compartilhe com Hugo, CPTO',
      btn: 'Iniciar Conversa'
    },
    {
      img: assetBase + 'hugo_08.jpg',
      label: 'Quer trocar uma ideia sobre seu projeto?',
      title: 'Compartilhe com Hugo, CPTO',
      btn: 'Iniciar Conversa'
    },
    {
      img: assetBase + 'hugo_05.jpg',
      label: 'Precisa de ajuda para comecar?',
      title: 'Compartilhe com Hugo, CPTO',
      btn: 'Iniciar Conversa'
    }
  ];

  var pairs = isPt ? pairsPT : pairsEN;

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
      var btn = card.querySelector('.founder-callout-btn');

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

      // Lock button styles to never wrap or shrink
      if (btn) {
        btn.style.whiteSpace = 'nowrap';
        btn.style.flexShrink = '0';
        if (btn.tagName === 'A') btn.href = contactBase;
      }

      var transStyle = 'opacity ' + TRANSITION_DURATION_MS + 'ms ease-in-out';
      img.style.transition = transStyle;
      if (label) label.style.transition = transStyle;
      if (name) name.style.transition = transStyle;
      if (btn) btn.style.transition = transStyle;

      setInterval(function () {
        currentIdx = (currentIdx + 1) % pairs.length;
        var next = pairs[currentIdx];

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
