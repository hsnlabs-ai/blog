/**
 * Founder Avatar Rotation Engine — HSN Labs
 * Smoothly rotates across the 20-photo curated pool of Hugo Soares portraits every 10 seconds.
 * Provides distinct initial portrait per page/context, with zero layout shift and smooth crossfade.
 */
(function () {
  'use strict';

  var POOL_SIZE = 20;
  var ROTATION_INTERVAL_MS = 10000;
  var TRANSITION_DURATION_MS = 450;

  // Detect base path for assets:
  // In production hsnlabs.ai (site or blog), /assets/images/author/pool/ always works.
  // In local mkdocs serve (localhost:8000), if /blog/ prefix is present or mkdocs root:
  var isLocalMkdocs = window.location.hostname === 'localhost' && window.location.port !== '8000' && window.location.port !== '';
  var assetBase = '/assets/images/author/pool/';
  if (window.location.pathname.startsWith('/blog/') && window.location.hostname === 'localhost') {
    assetBase = '/blog/assets/images/author/pool/';
  }

  var pool = [];
  for (var i = 1; i <= POOL_SIZE; i++) {
    var num = i < 10 ? '0' + i : '' + i;
    pool.push(assetBase + 'hugo_' + num + '.jpg');
  }

  // Preload remaining pool images in background after first paint
  function preloadPool() {
    for (var j = 0; j < pool.length; j++) {
      var img = new Image();
      img.src = pool[j];
    }
  }

  if (typeof window.requestIdleCallback === 'function') {
    window.requestIdleCallback(preloadPool);
  } else {
    setTimeout(preloadPool, 2500);
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
    var avatars = document.querySelectorAll('.founder-avatar-box, .founder-callout-avatar, [data-founder-avatar]');
    if (!avatars || avatars.length === 0) return;

    avatars.forEach(function (box, boxIndex) {
      var img = box.querySelector('img');
      if (!img) return;

      // Determine initial index
      var initialIdxAttr = box.getAttribute('data-initial-index');
      var currentIndex = 0;

      if (initialIdxAttr !== null && !isNaN(parseInt(initialIdxAttr, 10))) {
        currentIndex = parseInt(initialIdxAttr, 10) % POOL_SIZE;
      } else {
        // Derive from pathname + boxIndex for deterministic variety per page
        var pathHash = hashString(window.location.pathname || '') + boxIndex * 7;
        currentIndex = pathHash % POOL_SIZE;
      }

      // Ensure proper base styles for smooth transition
      img.style.transition = 'opacity ' + TRANSITION_DURATION_MS + 'ms ease-in-out';
      img.style.willChange = 'opacity';

      // Set initial image if not already set to pool
      if (!img.src.includes('/pool/hugo_')) {
        img.src = pool[currentIndex];
      }

      // Start rotation loop every 10s
      setInterval(function () {
        currentIndex = (currentIndex + 1) % POOL_SIZE;
        img.style.opacity = '0';

        setTimeout(function () {
          var nextSrc = pool[currentIndex];
          var temp = new Image();
          temp.onload = function () {
            img.src = nextSrc;
            img.style.opacity = '1';
          };
          temp.onerror = function () {
            img.src = nextSrc;
            img.style.opacity = '1';
          };
          temp.src = nextSrc;
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
