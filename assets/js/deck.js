/* Minimal slide-deck controller for portfolio project pages.
   No dependencies. Progressive enhancement: with JS disabled every slide
   is still in the DOM, so the page reads as a long-form document. */
(function () {
  'use strict';

  function initDeck(deck) {
    var slides = Array.prototype.slice.call(deck.querySelectorAll('.slide'));
    if (!slides.length) return;

    var prev = document.querySelector('[data-deck-prev]');
    var next = document.querySelector('[data-deck-next]');
    var counter = document.querySelector('[data-deck-counter]');
    var bar = document.querySelector('[data-deck-bar]');
    var index = 0;

    function render() {
      slides.forEach(function (s, i) {
        s.classList.toggle('active', i === index);
        s.setAttribute('aria-hidden', i === index ? 'false' : 'true');
      });
      if (counter) counter.textContent = 'Slide ' + (index + 1) + ' of ' + slides.length;
      if (bar) bar.style.width = ((index + 1) / slides.length) * 100 + '%';
      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index === slides.length - 1;
      // Let demo widgets know they became visible (charts need a size).
      var active = slides[index];
      active.dispatchEvent(new CustomEvent('slide:shown', { bubbles: true }));
      if (location.hash !== '#s' + (index + 1)) {
        history.replaceState(null, '', '#s' + (index + 1));
      }
    }

    function go(n) {
      index = Math.max(0, Math.min(slides.length - 1, n));
      render();
      // Keep the deck in view without yanking the page on first paint.
      var top = deck.getBoundingClientRect().top;
      if (top < 0) deck.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    if (prev) prev.addEventListener('click', function () { go(index - 1); });
    if (next) next.addEventListener('click', function () { go(index + 1); });

    // "Jump to the demo" controls: any element carrying data-deck-goto="N"
    // moves straight to that slide (1-based), so a visitor can reach the
    // interactive part without clicking through the deck.
    Array.prototype.forEach.call(
      document.querySelectorAll('[data-deck-goto]'),
      function (el) {
        el.addEventListener('click', function (e) {
          e.preventDefault();
          go(parseInt(el.getAttribute('data-deck-goto'), 10) - 1);
        });
      }
    );

    document.addEventListener('keydown', function (e) {
      if (/^(INPUT|SELECT|TEXTAREA)$/.test(e.target.tagName)) return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { go(index + 1); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { go(index - 1); }
      else if (e.key === 'Home') { go(0); }
      else if (e.key === 'End') { go(slides.length - 1); }
    });

    // Touch swipe.
    var x0 = null;
    deck.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    deck.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 55) go(index + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });

    var fromHash = parseInt((location.hash.match(/^#s(\d+)$/) || [])[1], 10);
    index = isNaN(fromHash) ? 0 : Math.min(slides.length, Math.max(1, fromHash)) - 1;
    render();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var deck = document.querySelector('[data-deck]');
    if (deck) initDeck(deck);
  });
})();
