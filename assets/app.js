// eSIM Coach — region filtering for the plan grid.
(function () {
  var filters = document.querySelectorAll('.filter');
  var cards = document.querySelectorAll('#grid .card');
  if (!filters.length) return;
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filters.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var f = btn.getAttribute('data-filter');
      cards.forEach(function (c) {
        var show = f === 'all' || c.getAttribute('data-region') === f;
        c.classList.toggle('hidden', !show);
      });
    });
  });
})();
