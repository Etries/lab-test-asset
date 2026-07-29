/* filters.js  -  the "add filter" bar on the batteries page.
   You start with no filters; click "+ Add filter", choose a field, and a row
   appears with the right control (searchable dropdown for sites/brands,
   checkboxes-as-a-select for health/status). Each row has a remove (×) button.
   On "Apply", every active row is submitted as a query parameter the server
   already understands (site=, health=, status=, brand=). */

(function () {
  // Filterable fields and where their options come from (injected by the page).
  const FIELDS = window.FILTER_FIELDS;      // [{key,label,type,options?}]
  const ACTIVE = window.ACTIVE_FILTERS;     // {site:[...], health:[...], ...}

  const container = document.getElementById("filter-rows");
  const addBtn = document.getElementById("add-filter-btn");
  const form = document.getElementById("filter-form");

  function fieldByKey(key) { return FIELDS.find(f => f.key === key); }

  // Which filter keys are already shown, so "Add filter" won't offer duplicates.
  function usedKeys() {
    return Array.from(container.querySelectorAll("[data-filter-key]"))
      .map(el => el.getAttribute("data-filter-key"));
  }

  function makeRow(fieldKey, selectedValues) {
    const field = fieldByKey(fieldKey);
    const row = document.createElement("div");
    row.className = "filter-chip";
    row.setAttribute("data-filter-key", fieldKey);

    const label = document.createElement("span");
    label.className = "filter-chip-label";
    label.textContent = field.label;
    row.appendChild(label);

    let control;
    if (field.type === "search-select") {
      // typeable single-select via <input list=...> (native, no library)
      control = document.createElement("input");
      control.setAttribute("list", "datalist-" + field.key);
      control.name = field.key;
      control.placeholder = "Type to search " + field.label.toLowerCase() + "…";
      control.className = "chip-input";
      control.value = (selectedValues && selectedValues[0]) || "";
      const dl = document.createElement("datalist");
      dl.id = "datalist-" + field.key;
      field.options.forEach(opt => {
        const o = document.createElement("option");
        o.value = opt; dl.appendChild(o);
      });
      row.appendChild(control);
      row.appendChild(dl);
    } else {
      // multi-select as a compact checklist inside the chip
      control = document.createElement("div");
      control.className = "chip-checks";
      field.options.forEach(opt => {
        const id = field.key + "-" + opt.value;
        const wrap = document.createElement("label");
        const cb = document.createElement("input");
        cb.type = "checkbox"; cb.name = field.key; cb.value = opt.value;
        if (selectedValues && selectedValues.includes(opt.value)) cb.checked = true;
        wrap.appendChild(cb);
        if (opt.colour) {
          const dot = document.createElement("span");
          dot.className = "dot"; dot.style.background = opt.colour;
          wrap.appendChild(dot);
        }
        wrap.appendChild(document.createTextNode(opt.label));
        control.appendChild(wrap);
      });
      row.appendChild(control);
    }

    const rm = document.createElement("button");
    rm.type = "button"; rm.className = "chip-remove"; rm.textContent = "×";
    rm.title = "Remove filter";
    rm.onclick = () => { row.remove(); refreshAddMenu(); };
    row.appendChild(rm);

    return row;
  }

  // Build the "+ Add filter" menu listing fields not already added.
  function refreshAddMenu() {
    const menu = document.getElementById("add-filter-menu");
    menu.innerHTML = "";
    const used = usedKeys();
    const available = FIELDS.filter(f => !used.includes(f.key));
    if (available.length === 0) {
      const none = document.createElement("div");
      none.className = "menu-empty"; none.textContent = "All filters added";
      menu.appendChild(none);
      return;
    }
    available.forEach(f => {
      const item = document.createElement("button");
      item.type = "button"; item.className = "menu-item"; item.textContent = f.label;
      item.onclick = () => {
        container.appendChild(makeRow(f.key, []));
        menu.classList.remove("open");
        refreshAddMenu();
      };
      menu.appendChild(item);
    });
  }

  addBtn.onclick = (e) => {
    e.stopPropagation();
    document.getElementById("add-filter-menu").classList.toggle("open");
  };
  document.addEventListener("click", () => {
    document.getElementById("add-filter-menu").classList.remove("open");
  });
  document.getElementById("add-filter-menu").onclick = (e) => e.stopPropagation();

  // Restore any filters that were active on page load (so Apply keeps them).
  Object.keys(ACTIVE).forEach(key => {
    if (fieldByKey(key) && ACTIVE[key].length) {
      container.appendChild(makeRow(key, ACTIVE[key]));
    }
  });
  refreshAddMenu();
})();
