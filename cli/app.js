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
  const pretty = (value) => escapeHtml(JSON.stringify(value, null, 2));

  function setTheme(theme) {
    root.dataset.theme = theme;
    try { localStorage.setItem("cli-manual-theme", theme); } catch (_) {}
    document.querySelectorAll(".theme-toggle").forEach((button) => {
      const next = theme === "dark" ? "light" : "dark";
      button.setAttribute("aria-label", `Switch to ${next} theme`);
      button.title = `Switch to ${next} theme`;
    });
  }

  function initTheme() {
    let saved = null;
    try { saved = localStorage.getItem("cli-manual-theme"); } catch (_) {}
    const preferred = window.matchMedia?.("(prefers-color-scheme: light)").matches ? "light" : "dark";
    setTheme(saved === "light" || saved === "dark" ? saved : preferred);
  }

  function codeBlock(label, value, json = false) {
    const content = json ? pretty(value) : escapeHtml(value);
    return `<div class="code-shell">
      <div class="code-label"><span>${escapeHtml(label)}</span><button class="copy-button" type="button">Copy</button></div>
      <pre><code>${content}</code></pre>
    </div>`;
  }

  function riskLabel(risk) {
    return { safe: "Read-only", stateful: "Session state", danger: "Mutating" }[risk] || risk;
  }

  function bindingFor(fieldName, operation) {
    if (operation.bindings[fieldName]) return operation.bindings[fieldName];
    return `--${fieldName.replaceAll("_", "-")} VALUE`;
  }

  function constraintText(spec) {
    const constraints = [];
    if (Object.hasOwn(spec, "default")) constraints.push(`default ${JSON.stringify(spec.default)}`);
    if (Object.hasOwn(spec, "minimum")) constraints.push(`minimum ${spec.minimum}`);
    if (Object.hasOwn(spec, "maximum")) constraints.push(`maximum ${spec.maximum}`);
    if (spec.enum) constraints.push(spec.enum.join(" | "));
    return constraints.join(" · ") || "—";
  }

  function argumentTable(tool, operation) {
    const properties = Object.entries(tool.schema.properties || {});
    if (!properties.length) {
      return `<div class="empty-schema"><strong>No operation arguments</strong><span>Run the operation name without additional operation flags.</span></div>`;
    }
    const required = new Set(tool.schema.required || []);
    const rows = properties.map(([name, spec]) => `<tr>
      <td><code class="argument-syntax">${escapeHtml(bindingFor(name, operation))}</code>${required.has(name) ? '<span class="required-dot">required</span>' : ""}</td>
      <td><code>${escapeHtml(spec.type)}</code></td>
      <td>${escapeHtml(constraintText(spec))}</td>
      <td>${escapeHtml(spec.description || "")}</td>
    </tr>`).join("");
    return `<div class="table-wrap"><table>
      <thead><tr><th>CLI syntax</th><th>Value</th><th>Constraints</th><th>Description</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>`;
  }

  function renderOperation(tool, family, projection) {
    const searchText = `${tool.name} ${tool.summary} ${tool.description} ${family.label} ${projection.usage} ${Object.keys(tool.schema.properties || {}).join(" ")}`.toLowerCase();
    const manual = tool.manual.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
    const gaps = (tool.gaps || []).filter((gap) => !gap.includes("MCP clients"));
    const gapHtml = gaps.length
      ? `<div class="gap-stack">${gaps.map((gap) => `<div class="callout warning"><strong>Known gap</strong><span>${escapeHtml(gap)}</span></div>`).join("")}</div>`
      : "";
    return `<article class="operation-card" id="${escapeHtml(tool.name)}" data-family="${escapeHtml(family.id)}" data-search="${escapeHtml(searchText)}">
      <header class="operation-header">
        <div>
          <div class="operation-meta"><span class="risk-badge ${escapeHtml(tool.risk)}">${escapeHtml(riskLabel(tool.risk))}</span><span>${escapeHtml(family.label)}</span></div>
          <h3><a href="#${escapeHtml(tool.name)}"><code>${escapeHtml(tool.name)}</code></a></h3>
          <p class="operation-summary">${escapeHtml(tool.summary)}</p>
        </div>
        <a class="anchor-link" href="#${escapeHtml(tool.name)}" aria-label="Link to ${escapeHtml(tool.name)}">#</a>
      </header>
      <div class="catalog-description"><span>Description</span><p>${escapeHtml(tool.description)}</p></div>
      ${gapHtml}
      <div class="operation-tabs" role="tablist" aria-label="${escapeHtml(tool.name)} reference sections">
        <button type="button" role="tab" aria-selected="true" data-tab="manual">Manual</button>
        <button type="button" role="tab" aria-selected="false" data-tab="arguments">Arguments</button>
        <button type="button" role="tab" aria-selected="false" data-tab="output">Output</button>
      </div>
      <section class="operation-panel active" role="tabpanel" data-panel="manual">
        ${codeBlock("Usage", projection.usage)}
        <ol class="manual-steps">${manual}</ol>
        <div class="command-stack">${projection.examples.map((example) => codeBlock("Example", example)).join("")}</div>
      </section>
      <section class="operation-panel" role="tabpanel" data-panel="arguments" hidden>
        <h4>Flags and positionals</h4>
        <p class="panel-intro">Required values are validated locally before gateway I/O.</p>
        ${argumentTable(tool, projection)}
      </section>
      <section class="operation-panel" role="tabpanel" data-panel="output" hidden>
        <h4>JSON result</h4>
        <p class="panel-intro">Success writes one compact JSON line to stdout and exits 0. The formatted sample below is expanded for readability.</p>
        ${codeBlock("Representative stdout", tool.output, true)}
        <div class="output-note"><strong>Shape note</strong><span>${escapeHtml(tool.outputNote)}</span></div>
      </section>
    </article>`;
  }

  function renderCatalog(semantic, cli) {
    const total = semantic.families.reduce((sum, family) => sum + family.tools.length, 0);
    const familyButtons = [
      `<button class="family-filter active" type="button" data-family-filter="all" aria-pressed="true">All <span>${total}</span></button>`,
      ...semantic.families.map((family) => `<button class="family-filter" type="button" data-family-filter="${escapeHtml(family.id)}" aria-pressed="false">${escapeHtml(family.label)} <span>${family.tools.length}</span></button>`)
    ].join("");
    const families = semantic.families.map((family, index) => `<section class="operation-family" id="family-${escapeHtml(family.id)}" data-family-section="${escapeHtml(family.id)}">
      <div class="family-heading"><span class="family-index">${String(index + 1).padStart(2, "0")}</span><div><h2>${escapeHtml(family.label)}</h2><p>${escapeHtml(family.description)}</p></div></div>
      <div class="operation-list">${family.tools.map((tool) => renderOperation(tool, family, cli.operations[tool.name])).join("")}</div>
    </section>`).join("");
    document.getElementById("catalog-content").innerHTML = `
      <section class="catalog-hero ${escapeHtml(semantic.accent)}">
        <div class="eyebrow"><span class="status-dot"></span>${escapeHtml(cli.eyebrow)} · ${total} operations</div>
        <h1>${escapeHtml(semantic.label)}<br><span>CLI</span></h1>
        <p>${escapeHtml(semantic.summary)}</p>
        <div class="server-chip"><span>Executable</span><code>${escapeHtml(cli.binary)}</code><span class="arrow">→</span><code>127.0.0.1:7878</code></div>
      </section>
      <section class="catalog-guide" aria-labelledby="catalog-guide-heading">
        <div><span class="kicker">${escapeHtml(cli.scope)}</span><h2 id="catalog-guide-heading">Before you run</h2></div>
        <ul>${cli.guidance.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      </section>
      <section class="catalog-toolbar" aria-label="Filter operations">
        <label class="search-box"><svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><span class="sr-only">Search operations</span><input id="tool-search" type="search" autocomplete="off" placeholder="Search ${escapeHtml(semantic.label.toLowerCase())} operations…"></label>
        <div class="family-filters" role="group" aria-label="Operation family">${familyButtons}</div>
        <span id="result-count" class="result-count" aria-live="polite">${total} operations</span>
      </section>
      <div id="no-results" class="no-results" hidden><strong>No matching operation</strong><span>Try an operation name, flag, or another family.</span></div>
      <div class="families">${families}</div>
      <section class="common-errors">
        <div><span class="kicker">Process contract</span><h2>JSON and exit codes</h2><p>Success writes JSON to stdout and exits 0. Gateway or transport failures write JSON to stderr and exit 1. Local usage or configuration errors write JSON to stderr and exit 2.</p></div>
        ${codeBlock("Representative stderr · exit 2", JSON.stringify({ error: { kind: "invalid_request", message: "…", details: {} } }))}
      </section>`;
  }

  function renderSidebar(semantic, cli) {
    const families = semantic.families.map((family) => `<section class="sidebar-family">
      <a class="sidebar-family-link" href="#family-${escapeHtml(family.id)}">${escapeHtml(family.label)}</a>
      <ul>${family.tools.map((tool) => `<li><a href="#${escapeHtml(tool.name)}"><code>${escapeHtml(tool.name)}</code></a></li>`).join("")}</ul>
    </section>`).join("");
    document.getElementById("sidebar-content").innerHTML = `
      <div class="sidebar-top"><a href="index.html">← Manual home</a><span>${escapeHtml(semantic.label)} CLI</span></div>
      <nav>${families}</nav>
      <div class="sidebar-foot"><span class="status-dot"></span><span>JSON lines · exits 0/1/2</span></div>`;
  }

  function initTabs() {
    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-tab]");
      if (!button) return;
      const card = button.closest(".operation-card");
      card.querySelectorAll("[data-tab]").forEach((item) => item.setAttribute("aria-selected", String(item === button)));
      card.querySelectorAll("[data-panel]").forEach((panel) => {
        const active = panel.dataset.panel === button.dataset.tab;
        panel.hidden = !active;
        panel.classList.toggle("active", active);
      });
    });
  }

  function initFilters() {
    const input = document.getElementById("tool-search");
    const filters = [...document.querySelectorAll(".family-filter")];
    const cards = [...document.querySelectorAll(".operation-card")];
    let family = "all";
    const apply = () => {
      const query = input.value.trim().toLowerCase();
      let visible = 0;
      cards.forEach((card) => {
        const show = (family === "all" || card.dataset.family === family) && (!query || card.dataset.search.includes(query));
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
      if (event.target.closest(".theme-toggle")) setTheme(root.dataset.theme === "dark" ? "light" : "dark");
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
      if (event.target.closest(".docs-sidebar a")) body.classList.remove("sidebar-open");
    });
  }

  function initCatalogPage() {
    const key = body.dataset.catalog;
    const semantic = window.MCP_CATALOGS?.[key];
    const cli = window.CLI_CATALOGS?.[key];
    if (!semantic || !cli) return;
    renderSidebar(semantic, cli);
    renderCatalog(semantic, cli);
    initTabs();
    initFilters();
    initSidebarObserver();
  }

  initTheme();
  initGlobalActions();
  if (body.dataset.page === "catalog") initCatalogPage();
})();

