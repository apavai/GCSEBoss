(function () {
  var APAVAI_WEBSITE_URL = "https://apavai.com";
  var PLATFORM_NAME = "GCSE Boss";

  var WORDMARK_SVG =
    '<svg viewBox="0 0 520 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="apavai-wordmark">' +
    '<path d="M 6,90 L 46,10 L 86,90" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter" />' +
    '<path d="M 108,10 L 168,45 L 108,80 L 108,90" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter" />' +
    '<path d="M 192,90 L 232,10 L 272,90" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter" />' +
    '<path d="M 292,10 L 332,90 L 372,10" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter" />' +
    '<path d="M 392,90 L 432,10 L 472,90" fill="none" stroke="#0090FF" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter" />' +
    '<line x1="498" y1="10" x2="498" y2="90" stroke="#0090FF" stroke-width="4" stroke-linecap="square" />' +
    "</svg>";

  function renderFooterBottom(container) {
    var year = new Date().getFullYear();
    var extraLegal = container.getAttribute("data-extra-legal");
    var extraHtml = extraLegal
      ? "<p>" + extraLegal + "</p>"
      : "";

    container.innerHTML =
      '<p class="footer-bottom-copy">&copy; ' + year + " " + PLATFORM_NAME + "</p>" +
      '<a href="' + APAVAI_WEBSITE_URL + '" target="_blank" rel="noopener noreferrer" class="apavai-badge">' +
      WORDMARK_SVG +
      '<span class="apavai-badge-label">An Apavai company</span>' +
      "</a>" +
      '<div class="footer-bottom-legal">' +
      "<p>" + PLATFORM_NAME + " is a trading name of Apavai Ltd</p>" +
      "<p>Registered in England &amp; Wales | Company No: 17036797</p>" +
      "<p>71-75 Shelton Street, Covent Garden, London, WC2H 9JQ</p>" +
      extraHtml +
      "</div>";
  }

  document.querySelectorAll(".footer-bottom").forEach(renderFooterBottom);
})();
