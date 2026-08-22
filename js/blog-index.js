(function () {
  var PER_PAGE = 10;
  var list = document.getElementById("blog-list");
  if (!list) return;

  var cards = Array.prototype.slice.call(list.querySelectorAll(".blog-card"));
  var nav = document.getElementById("blog-pagination");
  var pageLabel = document.getElementById("blog-page-label");
  var prevBtn = document.getElementById("blog-prev");
  var nextBtn = document.getElementById("blog-next");

  function totalPages() {
    return Math.max(1, Math.ceil(cards.length / PER_PAGE));
  }

  function pageFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var p = parseInt(params.get("page") || "1", 10);
    if (!p || p < 1) p = 1;
    return Math.min(p, totalPages());
  }

  function render(page, push) {
    var total = totalPages();
    page = Math.min(Math.max(1, page), total);
    var start = (page - 1) * PER_PAGE;
    var end = start + PER_PAGE;

    cards.forEach(function (card, i) {
      card.hidden = i < start || i >= end;
    });

    if (nav) nav.hidden = total <= 1;
    if (pageLabel) pageLabel.textContent = "Page " + page + " of " + total;
    if (prevBtn) prevBtn.disabled = page <= 1;
    if (nextBtn) nextBtn.disabled = page >= total;

    if (push) {
      var path = window.location.pathname;
      var url = page === 1 ? path : path + "?page=" + page;
      history.pushState({ page: page }, "", url);
    }
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      render(pageFromUrl() - 1, true);
      list.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      render(pageFromUrl() + 1, true);
      list.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  window.addEventListener("popstate", function () {
    render(pageFromUrl(), false);
  });

  render(pageFromUrl(), false);

  var trigger = document.getElementById("blog-topics-trigger");
  var panel = document.getElementById("blog-topics-panel");
  var label = document.getElementById("blog-topics-label");
  if (trigger && panel) {
    trigger.addEventListener("click", function () {
      var open = trigger.getAttribute("aria-expanded") === "true";
      trigger.setAttribute("aria-expanded", open ? "false" : "true");
      panel.hidden = open;
      if (label) label.textContent = open ? "Show topics" : "Hide topics";
    });
  }
})();
