"use strict";
document.body.classList.add("js");
const menu = document.querySelector(".menu-toggle");
menu?.addEventListener("click", () => {
  const expanded = menu.getAttribute("aria-expanded") !== "true";
  menu.setAttribute("aria-expanded", String(expanded));
  document.querySelector("#global-nav").classList.toggle("open", expanded);
});
document.querySelectorAll("main table").forEach(table => {
  const wrap = document.createElement("div");
  wrap.className = "table-wrap";
  wrap.tabIndex = 0;
  wrap.setAttribute("role", "region");
  wrap.setAttribute("aria-label", "Scrollable research table");
  table.before(wrap); wrap.append(table);
});
const registry = document.querySelector("#registry");
if (registry) {
  const rows = [...registry.querySelectorAll("tbody tr")];
  const query = document.querySelector("#query");
  const filters = ["tool", "system", "dataset"].map(key => [key, document.querySelector(`#filter-${key}`)]);
  for (const [key, select] of filters) {
    [...new Set(rows.map(row => row.dataset[key]))].sort().forEach(value => {
      const option = document.createElement("option"); option.value = value; option.textContent = value; select.append(option);
    });
  }
  const update = () => {
    const terms = query.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const row of rows) {
      row.hidden = !terms.every(term => row.dataset.search.includes(term)) || !filters.every(([key, select]) => !select.value || row.dataset[key] === select.value);
      if (!row.hidden) count++;
    }
    document.querySelector("#result-count").textContent = `${count} of ${rows.length} experiments`;
    document.querySelector("#empty-state").hidden = count !== 0;
  };
  query.addEventListener("input", update);
  filters.forEach(([,select]) => select.addEventListener("change", update));
  document.querySelector("#reset-filters").addEventListener("click", () => {query.value = ""; filters.forEach(([,s]) => s.value = ""); update(); query.focus();});
  document.querySelector("#registry-controls").hidden = false;
  update();
}
