/* Sidebar navigation behaviour for the SCCG site.
 * Markup comes from _includes/sccg-nav.html; everything here is progressive
 * enhancement, so the nav stays a usable link list without JavaScript. */
(function () {
  "use strict";

  var nav = document.getElementById("sccg-nav");
  if (!nav) {
    return;
  }

  var layout = nav.parentNode;
  var filterInput = document.getElementById("sccg-nav-filter");
  var noMatch = document.getElementById("sccg-nav-no-match");
  var categories = Array.prototype.slice.call(nav.querySelectorAll(".sccg-nav-category"));
  var narrow = window.matchMedia
    ? window.matchMedia("(max-width: 61.99em)")
    : { matches: false };
  var STORAGE_KEY = "sccg-nav-open";

  /* ---- stored open/closed state per category --------------------------- */

  function readStoredState() {
    try {
      return JSON.parse(window.localStorage.getItem(STORAGE_KEY)) || {};
    } catch (error) {
      return {};
    }
  }

  function writeStoredState(state) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (error) {
      /* private mode or blocked storage: keep the default open state */
    }
  }

  var storedState = readStoredState();
  categories.forEach(function (details) {
    var id = details.getAttribute("data-category");
    if (Object.prototype.hasOwnProperty.call(storedState, id)) {
      details.open = Boolean(storedState[id]);
    }
    details.addEventListener("toggle", function () {
      if (nav.classList.contains("is-filtering")) {
        return;
      }
      var state = readStoredState();
      state[id] = details.open;
      writeStoredState(state);
    });
  });

  /* ---- link targets on this page --------------------------------------- */

  function safeDecode(value) {
    try {
      return decodeURIComponent(value);
    } catch (error) {
      /* malformed percent-encoding: no anchor can match it anyway */
      return value;
    }
  }

  function targetFor(link) {
    var href = link.getAttribute("href") || "";
    var hashIndex = href.indexOf("#");
    if (hashIndex < 0) {
      return null;
    }
    var id = safeDecode(href.slice(hashIndex + 1));
    if (!id) {
      return null;
    }
    return document.getElementById(id);
  }

  function inDocumentOrder(a, b) {
    var relation = a.target.compareDocumentPosition(b.target);
    if (relation & Node.DOCUMENT_POSITION_FOLLOWING) {
      return -1;
    }
    if (relation & Node.DOCUMENT_POSITION_PRECEDING) {
      return 1;
    }
    return 0;
  }

  var navLinks = Array.prototype.slice.call(nav.querySelectorAll("a[href*='#']"));
  var spyTargets = [];

  navLinks.forEach(function (link) {
    var target = targetFor(link);
    if (!target) {
      return;
    }
    /* The rule tree is rendered on every page; on the page that owns the
     * anchor, keep the link in-page so following it does not reload. */
    link.setAttribute("href", "#" + target.id);
    spyTargets.push({ link: link, target: target });
  });

  spyTargets.sort(inDocumentOrder);

  /* ---- accept "#CL.4" style hashes pasted from tool output ------------- */

  function normalizeHash() {
    var raw = window.location.hash;
    if (!raw || raw.length < 2) {
      return;
    }
    var id = safeDecode(raw.slice(1)).trim();
    if (document.getElementById(id)) {
      return;
    }
    var match = /^([A-Za-z]{2})[.\-_ ]?(\d+)$/.exec(id);
    if (!match) {
      return;
    }
    var canonical = (match[1] + match[2]).toLowerCase();
    if (document.getElementById(canonical)) {
      window.location.replace("#" + canonical);
    }
  }

  normalizeHash();
  window.addEventListener("hashchange", normalizeHash);

  /* ---- "On this page" for pages without generated section data --------- */

  var pageSections = document.getElementById("sccg-page-sections");
  var main = document.getElementById("content");
  if (pageSections && main) {
    var headings = Array.prototype.slice.call(main.querySelectorAll("h2[id]"));
    if (headings.length) {
      var groupHeading = document.createElement("p");
      groupHeading.className = "sccg-nav-heading";
      groupHeading.textContent = "On this page";
      var list = document.createElement("ul");
      list.className = "sccg-nav-list sccg-nav-sections";
      headings.forEach(function (element) {
        var item = document.createElement("li");
        var link = document.createElement("a");
        link.href = "#" + element.id;
        link.textContent = element.textContent;
        item.appendChild(link);
        list.appendChild(item);
        spyTargets.push({ link: link, target: element });
      });
      pageSections.appendChild(groupHeading);
      pageSections.appendChild(list);
      spyTargets.sort(inDocumentOrder);
    }
  }

  /* ---- narrow screens: collapse the sidebar behind a toggle ------------ */

  var toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "sccg-nav-toggle";
  toggle.setAttribute("aria-controls", "sccg-nav");
  toggle.textContent = "☰  Guideline navigation";
  layout.insertBefore(toggle, nav);

  function setNavVisible(visible) {
    nav.hidden = !visible;
    toggle.setAttribute("aria-expanded", visible ? "true" : "false");
  }

  function applyBreakpoint() {
    if (narrow.matches) {
      setNavVisible(false);
    } else {
      nav.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
    }
  }

  toggle.addEventListener("click", function () {
    setNavVisible(nav.hidden);
  });

  if (typeof narrow.addEventListener === "function") {
    narrow.addEventListener("change", applyBreakpoint);
  } else if (typeof narrow.addListener === "function") {
    narrow.addListener(applyBreakpoint);
  }
  applyBreakpoint();

  nav.addEventListener("click", function (event) {
    var link = event.target.closest ? event.target.closest("a") : null;
    if (link && narrow.matches) {
      setNavVisible(false);
    }
  });

  /* ---- filter ---------------------------------------------------------- */

  var ruleLinks = Array.prototype.slice.call(nav.querySelectorAll(".sccg-nav-rules a"));
  var sectionItems = Array.prototype.slice.call(nav.querySelectorAll(".sccg-nav-sections li"));

  ruleLinks.forEach(function (link) {
    var id = (link.getAttribute("data-rule-id") || "").toLowerCase();
    var title = link.textContent.toLowerCase();
    link.setAttribute("data-search", id + " " + id.replace(/\./g, "") + " " + title);
  });

  function clearFilter() {
    nav.classList.remove("is-filtering");
    ruleLinks.forEach(function (link) {
      link.parentNode.hidden = false;
    });
    sectionItems.forEach(function (item) {
      item.hidden = false;
    });
    var state = readStoredState();
    categories.forEach(function (details) {
      details.hidden = false;
      var id = details.getAttribute("data-category");
      details.open = Object.prototype.hasOwnProperty.call(state, id) ? Boolean(state[id]) : true;
    });
    if (noMatch) {
      noMatch.hidden = true;
    }
  }

  function applyFilter(rawQuery) {
    var query = rawQuery.trim().toLowerCase();
    if (!query) {
      clearFilter();
      return;
    }
    nav.classList.add("is-filtering");
    var compact = query.replace(/[\s.]/g, "");
    var matches = 0;
    categories.forEach(function (details) {
      var categoryMatches = 0;
      var links = Array.prototype.slice.call(details.querySelectorAll(".sccg-nav-rules a"));
      links.forEach(function (link) {
        var haystack = link.getAttribute("data-search") || "";
        var hit = haystack.indexOf(query) >= 0 || haystack.indexOf(compact) >= 0;
        link.parentNode.hidden = !hit;
        if (hit) {
          categoryMatches += 1;
        }
      });
      details.hidden = categoryMatches === 0;
      details.open = categoryMatches > 0;
      matches += categoryMatches;
    });
    sectionItems.forEach(function (item) {
      var hit = item.textContent.toLowerCase().indexOf(query) >= 0;
      item.hidden = !hit;
      if (hit) {
        matches += 1;
      }
    });
    if (noMatch) {
      noMatch.hidden = matches > 0;
    }
  }

  if (filterInput) {
    filterInput.addEventListener("input", function () {
      applyFilter(filterInput.value);
    });

    filterInput.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        filterInput.value = "";
        clearFilter();
        return;
      }
      if (event.key !== "Enter") {
        return;
      }
      event.preventDefault();
      var first = ruleLinks.filter(function (link) {
        var category = link.closest(".sccg-nav-category");
        return !link.parentNode.hidden && !(category && category.hidden);
      })[0];
      if (first) {
        first.click();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) {
        return;
      }
      var active = document.activeElement;
      var tag = active ? active.tagName : "";
      if (tag === "INPUT" || tag === "TEXTAREA" || (active && active.isContentEditable)) {
        return;
      }
      event.preventDefault();
      if (narrow.matches) {
        setNavVisible(true);
      }
      filterInput.focus();
      filterInput.select();
    });
  }

  /* ---- highlight the section currently in view ------------------------- */

  if (!spyTargets.length) {
    return;
  }

  var activeLink = null;
  var queued = false;

  function keepInView(link) {
    if (narrow.matches || nav.scrollHeight <= nav.clientHeight) {
      return;
    }
    var linkTop = link.offsetTop;
    var linkBottom = linkTop + link.offsetHeight;
    if (linkTop < nav.scrollTop + 40) {
      nav.scrollTop = Math.max(0, linkTop - 80);
    } else if (linkBottom > nav.scrollTop + nav.clientHeight - 20) {
      nav.scrollTop = linkBottom - nav.clientHeight + 60;
    }
  }

  function updateActive() {
    queued = false;
    var current = spyTargets[0];
    for (var index = 0; index < spyTargets.length; index += 1) {
      if (spyTargets[index].target.getBoundingClientRect().top <= 120) {
        current = spyTargets[index];
      } else {
        break;
      }
    }
    if (!current || current.link === activeLink) {
      return;
    }
    if (activeLink) {
      activeLink.classList.remove("is-active");
    }
    activeLink = current.link;
    activeLink.classList.add("is-active");
    keepInView(activeLink);
  }

  function requestUpdate() {
    if (queued) {
      return;
    }
    queued = true;
    window.requestAnimationFrame(updateActive);
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
  requestUpdate();
})();
