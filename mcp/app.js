(() => {
  "use strict";

  const root = document.documentElement;
  const body = document.body;

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const json = (value) => escapeHtml(JSON.stringify(value, null, 2));

  function setTheme(theme) {
    root.dataset.theme = theme;
    try { localStorage.setItem("mcp-manual-theme", theme); } catch (_) {}
    document.querySelectorAll(".theme-toggle").forEach((button) => {
      button.setAttribute("aria-label", `Switch to ${theme === "dark" ? "light" : "dark"} theme`);
      button.title = `Switch to ${theme === "dark" ? "light" : "dark"} theme`;
    });
  }

  function initTheme() {
    let saved = null;
    try { saved = localStorage.getItem("mcp-manual-theme"); } catch (_) {}
    const preferred = window.matchMedia?.("(prefers-color-scheme: light)").matches ? "light" : "dark";
    setTheme(saved === "light" || saved === "dark" ? saved : preferred);
  }

  function codeBlock(label, value) {
    return `<div class="code-shell">
      <div class="code-label"><span>${escapeHtml(label)}</span><button class="copy-button" type="button">Copy</button></div>
      <pre><code>${json(value)}</code></pre>
    </div>`;
  }

  function constraintText(spec) {
    const parts = [];
    if (Object.hasOwn(spec, "default")) parts.push(`default ${JSON.stringify(spec.default)}`);
    if (Object.hasOwn(spec, "minimum")) parts.push(`minimum ${spec.minimum}`);
    if (Object.hasOwn(spec, "maximum")) parts.push(`maximum ${spec.maximum}`);
    if (spec.enum) parts.push(spec.enum.join(" | "));
    return parts.length ? parts.join(" · ") : "—";
  }

  function inputTable(tool) {
    const properties = Object.entries(tool.schema.properties || {});
    if (!properties.length) {
      return `<div class="empty-schema"><strong>No arguments</strong><span>Send an empty JSON object: <code>{}</code>.</span></div>`;
    }
    const required = new Set(tool.schema.required || []);
    const rows = properties.map(([name, spec]) => `<tr>
      <td><code>${escapeHtml(name)}</code>${required.has(name) ? '<span class="required-dot" title="Required">required</span>' : ""}</td>
      <td><code>${escapeHtml(spec.type)}</code></td>
      <td>${escapeHtml(constraintText(spec))}</td>
      <td>${escapeHtml(spec.description || "")}</td>
    </tr>`).join("");
    return `<div class="table-wrap"><table>
      <thead><tr><th>Field</th><th>Type</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>`;
  }

  function riskLabel(risk) {
    return { safe: "Read-only", stateful: "Session state", danger: "Mutating" }[risk] || risk;
  }

  function renderOperation(tool, family) {
    const searchText = `${tool.name} ${tool.summary} ${tool.description} ${family.label} ${Object.keys(tool.schema.properties || {}).join(" ")}`.toLowerCase();
    const manual = tool.manual.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
    const gaps = tool.gaps?.length
      ? `<div class="gap-stack">${tool.gaps.map((gap) => `<div class="callout warning"><strong>Known gap</strong><span>${escapeHtml(gap)}</span></div>`).join("")}</div>`
      : "";
    const request = {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: { name: tool.name, arguments: tool.request }
    };
    const response = {
      result: {
        content: [{ type: "text", text: "…" }],
        structuredContent: tool.output,
        isError: false
      }
    };
    return `<article class="operation-card" id="${escapeHtml(tool.name)}" data-family="${escapeHtml(family.id)}" data-search="${escapeHtml(searchText)}">
      <header class="operation-header">
        <div>
          <div class="operation-meta"><span class="risk-badge ${escapeHtml(tool.risk)}">${escapeHtml(riskLabel(tool.risk))}</span><span>${escapeHtml(family.label)}</span></div>
          <h3><a href="#${escapeHtml(tool.name)}"><code>${escapeHtml(tool.name)}</code></a></h3>
          <p class="operation-summary">${escapeHtml(tool.summary)}</p>
        </div>
        <a class="anchor-link" href="#${escapeHtml(tool.name)}" aria-label="Link to ${escapeHtml(tool.name)}">#</a>
      </header>
      <div class="catalog-description"><span>Catalog description</span><p>${escapeHtml(tool.description)}</p></div>
      ${gaps}
      <div class="operation-tabs" role="tablist" aria-label="${escapeHtml(tool.name)} reference sections">
        <button type="button" role="tab" aria-selected="true" data-tab="manual">Manual</button>
        <button type="button" role="tab" aria-selected="false" data-tab="input">Input</button>
        <button type="button" role="tab" aria-selected="false" data-tab="output">Output</button>
      </div>
      <section class="operation-panel active" role="tabpanel" data-panel="manual">
        <ol class="manual-steps">${manual}</ol>
      </section>
      <section class="operation-panel" role="tabpanel" data-panel="input" hidden>
        <h4>Arguments</h4>
        <p class="panel-intro">Send these fields in <code>params.arguments</code>. The catalog rejects additional properties.</p>
        ${inputTable(tool)}
        ${codeBlock("Example tools/call request", request)}
        <details class="schema-details"><summary>Exact published input schema</summary>${codeBlock("inputSchema", tool.schema)}</details>
      </section>
      <section class="operation-panel" role="tabpanel" data-panel="output" hidden>
        <h4>Structured result</h4>
        <p class="panel-intro">Read operation data from <code>result.structuredContent</code> and check <code>result.isError</code>.</p>
        ${codeBlock("Representative success response", response)}
        <div class="output-note"><strong>Shape note</strong><span>${escapeHtml(tool.outputNote)}</span></div>
      </section>
    </article>`;
  }

  function renderCatalog(catalog) {
    const total = catalog.families.reduce((sum, family) => sum + family.tools.length, 0);
    const familyButtons = [
      `<button class="family-filter active" type="button" data-family-filter="all" aria-pressed="true">All <span>${total}</span></button>`,
      ...catalog.families.map((family) => `<button class="family-filter" type="button" data-family-filter="${escapeHtml(family.id)}" aria-pressed="false">${escapeHtml(family.label)} <span>${family.tools.length}</span></button>`)
    ].join("");
    const families = catalog.families.map((family) => `<section class="operation-family" id="family-${escapeHtml(family.id)}" data-family-section="${escapeHtml(family.id)}">
      <div class="family-heading"><span class="family-index">${String(catalog.families.indexOf(family) + 1).padStart(2, "0")}</span><div><h2>${escapeHtml(family.label)}</h2><p>${escapeHtml(family.description)}</p></div></div>
      <div class="operation-list">${family.tools.map((tool) => renderOperation(tool, family)).join("")}</div>
    </section>`).join("");
    const guide = catalog.guidance.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
    document.getElementById("catalog-content").innerHTML = `
      <section class="catalog-hero ${escapeHtml(catalog.accent)}">
        <div class="eyebrow"><span class="status-dot"></span>${escapeHtml(catalog.eyebrow)} · ${total} tools</div>
        <h1>${escapeHtml(catalog.label)}<br><span>catalog</span></h1>
        <p>${escapeHtml(catalog.summary)}</p>
        <div class="server-chip"><span>Registration</span><code>${escapeHtml(catalog.server)}</code><span class="arrow">→</span><code>${escapeHtml(catalog.command)}</code></div>
      </section>
      <section class="catalog-guide" aria-labelledby="catalog-guide-heading">
        <div><span class="kicker">Catalog manual</span><h2 id="catalog-guide-heading">Before you call</h2></div>
        <ul>${guide}</ul>
      </section>
      <section class="catalog-toolbar" aria-label="Filter operations">
        <label class="search-box"><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><span class="sr-only">Search operations</span><input id="tool-search" type="search" autocomplete="off" placeholder="Search ${escapeHtml(catalog.label.toLowerCase())} tools…"></label>
        <div class="family-filters" role="group" aria-label="Operation family">${familyButtons}</div>
        <span id="result-count" class="result-count" aria-live="polite">${total} operations</span>
      </section>
      <div id="no-results" class="no-results" hidden><strong>No matching operation</strong><span>Try a tool name, field, or another family.</span></div>
      <div class="families">${families}</div>
      <section class="common-errors">
        <div><span class="kicker">Error contract</span><h2>One failure envelope</h2><p>Validation failures stop before gateway dispatch. Gateway or operation failures return a structured error and set <code>isError</code> true.</p></div>
        ${codeBlock("Representative error response", { result: { content: [{ type: "text", text: "invalid_request: …" }], structuredContent: { error: { kind: "invalid_request", message: "…", details: {} } }, isError: true } })}
      </section>`;
  }

  function renderSidebar(catalog) {
    const families = catalog.families.map((family) => `<section class="sidebar-family">
      <a class="sidebar-family-link" href="#family-${escapeHtml(family.id)}">${escapeHtml(family.label)}</a>
      <ul>${family.tools.map((tool) => `<li><a href="#${escapeHtml(tool.name)}"><code>${escapeHtml(tool.name)}</code></a></li>`).join("")}</ul>
    </section>`).join("");
    document.getElementById("sidebar-content").innerHTML = `
      <div class="sidebar-top"><a href="index.html">← Manual home</a><span>${escapeHtml(catalog.label)} catalog</span></div>
      <nav>${families}</nav>
      <div class="sidebar-foot"><span class="status-dot"></span><span>stdio · MCP 2025-06-18</span></div>`;
  }

  function initTabs() {
    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-tab]");
      if (!button) return;
      const card = button.closest(".operation-card");
      const tab = button.dataset.tab;
      card.querySelectorAll("[data-tab]").forEach((item) => item.setAttribute("aria-selected", String(item === button)));
      card.querySelectorAll("[data-panel]").forEach((panel) => {
        const active = panel.dataset.panel === tab;
        panel.hidden = !active;
        panel.classList.toggle("active", active);
      });
    });
  }

  function initFilters(catalog) {
    const input = document.getElementById("tool-search");
    const filters = [...document.querySelectorAll(".family-filter")];
    const cards = [...document.querySelectorAll(".operation-card")];
    let family = "all";
    const apply = () => {
      const query = input.value.trim().toLowerCase();
      let visible = 0;
      cards.forEach((card) => {
        const matchesFamily = family === "all" || card.dataset.family === family;
        const matchesQuery = !query || card.dataset.search.includes(query);
        const show = matchesFamily && matchesQuery;
        card.hidden = !show;
        if (show) visible += 1;
      });
      document.querySelectorAll("[data-family-section]").forEach((section) => {
        section.hidden = ![...section.querySelectorAll(".operation-card")].some((card) => !card.hidden);
      });
      document.getElementById("result-count").textContent = `${visible} operation${visible === 1 ? "" : "s"}`;
      document.getElementById("no-results").hidden = visible !== 0;
    };
    input.addEventListener("input", apply);
    filters.forEach((button) => button.addEventListener("click", () => {
      family = button.dataset.familyFilter;
      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      apply();
    }));
  }

  function initSidebarObserver() {
    if (!("IntersectionObserver" in window)) return;
    const links = new Map([...document.querySelectorAll(".docs-sidebar a[href^='#']")].map((link) => [link.hash.slice(1), link]));
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (!visible) return;
      links.forEach((link) => link.classList.remove("current"));
      links.get(visible.target.id)?.classList.add("current");
    }, { rootMargin: "-18% 0px -72% 0px" });
    document.querySelectorAll(".operation-card, .operation-family").forEach((section) => observer.observe(section));
  }

  function initGlobalActions() {
    document.addEventListener("click", async (event) => {
      const theme = event.target.closest(".theme-toggle");
      if (theme) setTheme(root.dataset.theme === "dark" ? "light" : "dark");

      const copy = event.target.closest(".copy-button");
      if (copy) {
        const text = copy.closest(".code-shell")?.querySelector("pre code")?.textContent || "";
        try {
          await navigator.clipboard.writeText(text);
          copy.textContent = "Copied";
          window.setTimeout(() => { copy.textContent = "Copy"; }, 1400);
        } catch (_) {
          copy.textContent = "Select text";
        }
      }

      const mobile = event.target.closest(".mobile-nav-toggle");
      if (mobile) {
        const open = body.classList.toggle("sidebar-open");
        mobile.setAttribute("aria-label", open ? "Close operation navigation" : "Open operation navigation");
        mobile.setAttribute("aria-expanded", String(open));
      }

      if (event.target.closest(".docs-sidebar a")) {
        body.classList.remove("sidebar-open");
        const toggle = document.querySelector(".mobile-nav-toggle");
        toggle?.setAttribute("aria-label", "Open operation navigation");
        toggle?.setAttribute("aria-expanded", "false");
      }
    });
  }

  function initCatalogPage() {
    const key = body.dataset.catalog;
    const catalog = window.MCP_CATALOGS?.[key];
    if (!catalog) return;
    renderSidebar(catalog);
    renderCatalog(catalog);
    initTabs();
    initFilters(catalog);
    initSidebarObserver();
  }

  initTheme();
  initGlobalActions();
  if (body.dataset.page === "catalog") initCatalogPage();
})();
