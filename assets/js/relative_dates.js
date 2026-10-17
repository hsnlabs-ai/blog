document.addEventListener("DOMContentLoaded", function () {
  var elements = document.querySelectorAll(".blog-sidebar-date[data-date]");
  var today = new Date();
  today.setHours(0, 0, 0, 0);

  elements.forEach(function (el) {
    var dateStr = el.getAttribute("data-date");
    if (!dateStr) return;
    var parts = dateStr.split("-");
    if (parts.length < 3) return;
    var y = parseInt(parts[0], 10);
    var m = parseInt(parts[1], 10) - 1;
    var d = parseInt(parts[2], 10);
    var postDate = new Date(y, m, d);
    var diffTime = today - postDate;
    var diffDays = Math.floor(diffTime / 86400000);
    var isPt = document.documentElement.lang.indexOf("pt") === 0 || window.location.pathname.indexOf("/pt/") !== -1;

    if (isPt) {
      if (diffDays <= 0) {
        el.textContent = "postado hoje";
      } else if (diffDays === 1) {
        el.textContent = "há 1 dia";
      } else {
        el.textContent = "há " + diffDays + " dias";
      }
    } else {
      if (diffDays <= 0) {
        el.textContent = "posted today";
      } else if (diffDays === 1) {
        el.textContent = "1 day ago";
      } else {
        el.textContent = diffDays + " days ago";
      }
    }
  });
});
