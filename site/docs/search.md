# Glossary Search

Use the interactive search below to scan terms, aliases, categories, roles, and
statuses. Layer filters to narrow the glossary down to the exact concepts your
team needs.

<div class="search-panel">
  <div class="search-field search-field--chips">
    <span>Quick filters</span>
    <div class="search-chips" role="group" aria-label="Quick filters">
      <button type="button" data-chip data-role="product">Product</button>
      <button type="button" data-chip data-role="engineering">Engineering</button>
      <button type="button" data-chip data-role="policy">Policy &amp; Risk</button>
      <button type="button" data-chip data-role="legal">Legal &amp; Compliance</button>
      <button type="button" data-chip data-category="Governance &amp; Risk">Governance &amp; Risk</button>
      <button type="button" data-chip data-category="LLM Core">LLM Core</button>
      <button type="button" data-chip data-category="Operations &amp; Monitoring">Operations &amp; Monitoring</button>
      <button type="button" data-chip data-status="draft">Draft</button>
      <button type="button" data-chip data-status="reviewed">Reviewed</button>
      <button type="button" data-chip data-status="approved">Approved</button>
    </div>
    <button type="button" class="search-reset" id="glossary-reset-filters">Clear filters</button>
    <p class="search-tip">Tip: combine a role with a category to see the vocabulary most relevant to your current project.</p>
  </div>
  <label class="search-field">
    <span>Search</span>
    <input id="glossary-search-input" type="search" placeholder="Try retrieval, token, risk..." />
  </label>
  <label class="search-field">
    <span>Category</span>
    <select id="glossary-category-select">
      <option value="">All categories</option>
    </select>
  </label>
  <label class="search-field">
    <span>Status</span>
    <select id="glossary-status-select">
      <option value="">All statuses</option>
    </select>
  </label>
  <label class="search-field">
    <span>Role</span>
    <select id="glossary-role-select">
      <option value="">All roles</option>
    </select>
  </label>
  <label class="search-field">
    <span>Sort by</span>
    <select id="glossary-sort-select">
      <option value="recent">Last reviewed (newest)</option>
      <option value="title">A → Z</option>
      <option value="category">Category</option>
    </select>
  </label>
</div>

<div class="search-metrics" id="glossary-health" aria-live="polite"></div>
<div class="search-summary" data-filter-summary aria-live="polite">Showing glossary results.</div>
<p class="search-tip search-tip--inline">Tip: copy the page URL after selecting filters to share a saved view with your team.</p>

<div id="glossary-search-results" class="search-results"></div>

<script>
  (function () {
    const dataUrl = '../assets/glossary-search.json';
    const searchInput = document.getElementById('glossary-search-input');
    const categorySelect = document.getElementById('glossary-category-select');
    const statusSelect = document.getElementById('glossary-status-select');
    const roleSelect = document.getElementById('glossary-role-select');
    const sortSelect = document.getElementById('glossary-sort-select');
    const resultsContainer = document.getElementById('glossary-search-results');
    const chipElements = Array.from(document.querySelectorAll('[data-chip]'));
    const resetButton = document.getElementById('glossary-reset-filters');
    const filterSummary = document.querySelector('[data-filter-summary]');
    const metricsContainer = document.getElementById('glossary-health');

    let terms = [];

    const ROLE_LABELS = {
      product: 'Product & Program Managers',
      engineering: 'Engineering & Platform',
      data_science: 'Data Science & Research',
      policy: 'Policy & Risk',
      legal: 'Legal & Compliance',
      security: 'Security & Trust',
      communications: 'Communications & Enablement',
    };

    const SORT_LABELS = {
      recent: 'Last reviewed (newest)',
      title: 'A → Z',
      category: 'Category',
    };

    const SORTERS = {
      recent: (a, b) => {
        const aTime = toTimestamp(a.last_reviewed);
        const bTime = toTimestamp(b.last_reviewed);
        if (aTime !== bTime) {
          return (bTime ?? 0) - (aTime ?? 0);
        }
        return a.term.localeCompare(b.term);
      },
      title: (a, b) => a.term.localeCompare(b.term),
      category: (a, b) => {
        const aCategory = (a.categories && a.categories[0]) || '';
        const bCategory = (b.categories && b.categories[0]) || '';
        const categoryDiff = aCategory.localeCompare(bCategory);
        if (categoryDiff !== 0) {
          return categoryDiff;
        }
        return a.term.localeCompare(b.term);
      },
    };

    function toTimestamp(value) {
      if (!value) {
        return null;
      }
      const parsed = Date.parse(value);
      return Number.isNaN(parsed) ? null : parsed;
    }

    function normalise(value) {
      return (value || '').toLowerCase();
    }

    function titleCase(value) {
      if (!value) {
        return value;
      }
      const clean = value.replace(/[_-]/g, ' ');
      return clean.replace(/\b([a-z])/g, (match) => match.toUpperCase());
    }

    function formatDate(value) {
      if (!value) {
        return value;
      }
      const parsed = new Date(value + 'T00:00:00Z');
      if (Number.isNaN(parsed.getTime())) {
        return value;
      }
      return parsed.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    }

    function highlightMatch(text, query) {
      if (!query) {
        return text;
      }
      const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`(${escaped})`, 'ig');
      return text.replace(regex, '<mark>$1</mark>');
    }

    function matches(term, query) {
      if (!query) {
        return true;
      }
      const haystack = [
        term.term,
        ...(term.aliases || []),
        term.short_def || '',
        ...(term.categories || []),
      ]
        .join(' \n ')
        .toLowerCase();
      return haystack.includes(query.toLowerCase());
    }

    function matchesCategory(term, category) {
      if (!category) {
        return true;
      }
      return (term.categories || []).some(
        (item) => normalise(item) === normalise(category)
      );
    }

    function matchesStatus(term, status) {
      if (!status) {
        return true;
      }
      return normalise(term.status) === normalise(status);
    }

    function matchesRole(term, role) {
      if (!role) {
        return true;
      }
      return (term.roles || []).some((item) => normalise(item) === normalise(role));
    }

    function renderFilterSummary(resultCount, query, category, status, role, sortKey) {
      if (!filterSummary) {
        return;
      }
      const parts = [];
      if (query) {
        parts.push(`Query: “${query}”`);
      }
      if (category) {
        parts.push(`Category: ${category}`);
      }
      if (status) {
        parts.push(`Status: ${titleCase(status)}`);
      }
      if (role) {
        parts.push(`Role: ${ROLE_LABELS[role] || role}`);
      }
      if (sortKey && sortKey !== 'recent') {
        parts.push(`Sort: ${SORT_LABELS[sortKey] || sortKey}`);
      }
      const prefix = parts.length ? `<strong>Active filters:</strong> ${parts.join(' · ')}` : 'Showing all terms.';
      filterSummary.innerHTML = `${prefix} <span class="search-summary-count">${resultCount} result${resultCount === 1 ? '' : 's'}</span>`;
    }

    function syncChips() {
      chipElements.forEach((chip) => {
        const category = chip.getAttribute('data-category');
        const role = chip.getAttribute('data-role');
        const status = chip.getAttribute('data-status');
        const isActive =
          (category && categorySelect.value === category) ||
          (role && roleSelect.value === role) ||
          (status && statusSelect.value === status);
        chip.classList.toggle('active', Boolean(isActive));
        chip.setAttribute('aria-pressed', isActive ? 'true' : 'false');
      });
    }

    function renderMetrics(entries) {
      if (!metricsContainer) {
        return;
      }
      if (!entries.length) {
        metricsContainer.textContent = 'No entries to summarise yet.';
        return;
      }
      const total = entries.length;
      const statusCounts = entries.reduce((acc, item) => {
        const status = item.status || 'unspecified';
        acc[status] = (acc[status] || 0) + 1;
        return acc;
      }, {});
      const latestTimestamp = entries.reduce((max, item) => {
        const ts = toTimestamp(item.last_reviewed);
        return ts !== null && ts > max ? ts : max;
      }, 0);
      const latestDate = latestTimestamp
        ? formatDate(new Date(latestTimestamp).toISOString().slice(0, 10))
        : '—';
      const statusMarkup = Object.entries(statusCounts)
        .sort((a, b) => b[1] - a[1])
        .map(([status, count]) => `<span class="metric-chip">${titleCase(status)}: <strong>${count}</strong></span>`)
        .join('');
      metricsContainer.innerHTML = `
        <span class="metric-chip total">Total terms: <strong>${total}</strong></span>
        ${statusMarkup}
        <span class="metric-chip">Latest review: <strong>${latestDate}</strong></span>
      `;
    }

    function renderResults() {
      const query = searchInput.value.trim();
      const category = categorySelect.value;
      const status = statusSelect.value;
      const role = roleSelect.value;
      const sortKey = sortSelect.value || 'recent';
      const sorter = SORTERS[sortKey] || SORTERS.recent;

      const filtered = terms.filter(
        (item) =>
          matches(item, query) &&
          matchesCategory(item, category) &&
          matchesStatus(item, status) &&
          matchesRole(item, role)
      );

      if (!filtered.length) {
        resultsContainer.innerHTML = '<p class="search-empty">No matching entries yet. Try clearing a filter or using a broader term.</p>';
        renderFilterSummary(0, query, category, status, role, sortKey);
        syncChips();
        return;
      }

      const list = document.createElement('ul');
      list.className = 'search-list';

      filtered
        .slice()
        .sort(sorter)
        .forEach((item) => {
          const li = document.createElement('li');
          li.className = 'search-item';
          const aliases = item.aliases && item.aliases.length
            ? ` <span class="search-aliases">(Aliases: ${item.aliases.join(', ')})</span>`
            : '';
          const categories = item.categories && item.categories.length
            ? `<span class="search-categories"><span class="meta-label">Categories</span>${item.categories.map((value) => `<span class=\"badge\">${value}</span>`).join(' ')}</span>`
            : '';
          const statusMarkup = item.status
            ? `<span class="search-status"><span class="meta-label">Status</span><span class="badge status status-${item.status}">${titleCase(item.status)}</span></span>`
            : '';
          const rolesMarkup = item.roles && item.roles.length
            ? `<span class="search-roles"><span class="meta-label">Roles</span>${item.roles.map((value) => `<span class=\"badge role\">${ROLE_LABELS[value] || value}</span>`).join(' ')}</span>`
            : '';
          const lastReviewedMarkup = item.last_reviewed
            ? `<span class="search-reviewed"><span class="meta-label">Last reviewed</span>${formatDate(item.last_reviewed)}</span>`
            : '';
          const href = item.slug ? `../terms/${item.slug}/` : '#';
          const highlightedTerm = highlightMatch(item.term, query);
          const highlightedSummary = highlightMatch(item.short_def || '', query);
          li.innerHTML = `
            <a data-term-link>${highlightedTerm}</a>
            ${aliases}
            <div class="search-meta">${categories} ${statusMarkup} ${rolesMarkup} ${lastReviewedMarkup}</div>
            <p>${highlightedSummary}</p>
          `;
          const link = li.querySelector('[data-term-link]');
          if (link) {
            link.setAttribute('href', href);
          }
          list.appendChild(li);
        });

      resultsContainer.innerHTML = '';
      resultsContainer.appendChild(list);
      renderFilterSummary(filtered.length, query, category, status, role, sortKey);
      syncChips();
    }

    function populateFilters() {
      const categoryValues = new Set();
      const statusValues = new Set();
      const roleValues = new Set();

      terms.forEach((item) => {
        (item.categories || []).forEach((value) => categoryValues.add(value));
        if (item.status) {
          statusValues.add(item.status);
        }
        (item.roles || []).forEach((value) => roleValues.add(value));
      });

      Array.from(categoryValues)
        .sort()
        .forEach((value) => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = value;
          categorySelect.appendChild(option);
        });

      Array.from(statusValues)
        .sort()
        .forEach((value) => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = titleCase(value);
          statusSelect.appendChild(option);
        });

      Array.from(roleValues)
        .sort()
        .forEach((value) => {
          const option = document.createElement('option');
          option.value = value;
          option.textContent = ROLE_LABELS[value] || value;
          roleSelect.appendChild(option);
        });
    }

    function attachListeners() {
      [searchInput, categorySelect, statusSelect, roleSelect, sortSelect].forEach((element) => {
        element.addEventListener('input', renderResults);
        element.addEventListener('change', renderResults);
      });

      chipElements.forEach((chip) => {
        chip.addEventListener('click', () => {
          const category = chip.getAttribute('data-category');
          const role = chip.getAttribute('data-role');
          const status = chip.getAttribute('data-status');

          if (category) {
            categorySelect.value = categorySelect.value === category ? '' : category;
          }
          if (role) {
            roleSelect.value = roleSelect.value === role ? '' : role;
          }
          if (status) {
            statusSelect.value = statusSelect.value === status ? '' : status;
          }
          renderResults();
        });
      });

      if (resetButton) {
        resetButton.addEventListener('click', () => {
          searchInput.value = '';
          categorySelect.value = '';
          statusSelect.value = '';
          roleSelect.value = '';
          sortSelect.value = 'recent';
          renderResults();
        });
      }
    }

    fetch(dataUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to load search index.');
        }
        return response.json();
      })
      .then((json) => {
        terms = json || [];
        populateFilters();
        renderMetrics(terms);
        attachListeners();
        renderResults();
      })
      .catch((error) => {
        resultsContainer.innerHTML = `<p class="search-error">${error.message}</p>`;
        if (filterSummary) {
          filterSummary.textContent = 'Search is temporarily unavailable.';
        }
        if (metricsContainer) {
          metricsContainer.textContent = 'Unable to load glossary metrics right now.';
        }
      });
  })();
</script>

<style>
  .search-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.25rem;
    border: 1px solid rgba(95, 46, 234, 0.15);
    border-radius: 12px;
    padding: 1.25rem;
    background: linear-gradient(135deg, rgba(95, 46, 234, 0.12), rgba(14, 165, 233, 0.08));
  }
  .search-field {
    display: flex;
    flex-direction: column;
    min-width: 200px;
    font-weight: 600;
  }
  .search-field--chips {
    flex: 1 1 100%;
  }
  .search-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.35rem;
  }
  .search-chips button {
    border: 1px solid var(--brand-primary);
    background: transparent;
    color: var(--brand-primary);
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-weight: 600;
    cursor: pointer;
  }
  .search-chips button.active,
  .search-chips button:hover {
    background: var(--brand-primary);
    color: var(--md-primary-bg-color, #fff);
  }
  .search-field input,
  .search-field select {
    margin-top: 0.25rem;
    padding: 0.5rem;
  }
  .search-reset {
    margin-top: 0.75rem;
    align-self: flex-start;
    background: transparent;
    border: none;
    color: var(--brand-primary);
    font-weight: 600;
    text-decoration: underline;
    cursor: pointer;
  }
  .search-tip {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light, #555);
  }
  .search-tip--inline {
    margin-top: 0;
  }
  .search-metrics {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light, #555);
  }
  .metric-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    background: rgba(95, 46, 234, 0.14);
    color: var(--brand-primary);
    font-weight: 600;
  }
  .metric-chip.total {
    background: rgba(103, 58, 183, 0.1);
    color: var(--brand-secondary);
  }
  .metric-chip strong {
    color: inherit;
  }
  .search-summary {
    margin-bottom: 1rem;
    font-weight: 600;
  }
  .search-summary-count {
    margin-left: 0.35rem;
    color: var(--md-default-fg-color--light, #555);
    font-weight: 500;
  }
  .search-results .search-list {
    list-style: none;
    padding: 0;
  }
  .search-results .search-item {
    border-bottom: 1px solid var(--md-default-fg-color--lightest, #ddd);
    padding: 1rem 0;
  }
  .search-results .search-item a {
    font-weight: 700;
  }
  .search-results mark {
    background: rgba(255, 235, 59, 0.45);
    padding: 0 0.1rem;
  }
  .search-meta {
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light, #555);
    margin: 0.35rem 0 0.45rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .meta-label {
    font-weight: 700;
    margin-right: 0.35rem;
  }
  .badge {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    background: rgba(95, 46, 234, 0.14);
    color: var(--brand-primary);
    margin-right: 0.25rem;
    font-weight: 600;
    font-size: 0.75rem;
  }
  .badge.role {
    background: rgba(14, 165, 233, 0.14);
    color: var(--brand-secondary);
  }
  .badge.status {
    background: rgba(76, 175, 80, 0.12);
    color: #1c7c54;
  }
  .badge.status.status-reviewed {
    background: rgba(76, 175, 80, 0.18);
    color: #1c7c54;
  }
  .badge.status.status-approved {
    background: rgba(33, 150, 243, 0.18);
    color: var(--brand-primary);
  }
  .badge.status.status-deprecated {
    background: rgba(244, 67, 54, 0.18);
    color: #c62828;
  }
  .search-aliases {
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light, #555);
  }
  .search-reviewed {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }
  .search-empty,
  .search-error {
    color: var(--md-accent-fg-color, #d35400);
    font-weight: 600;
  }
  @media (max-width: 720px) {
    .search-panel {
      padding: 1rem;
    }
    .search-field {
      min-width: 140px;
      flex: 1 1 calc(50% - 1rem);
    }
    .search-field--chips {
      flex: 1 1 100%;
    }
    .search-metrics {
      flex-direction: column;
    }
  }
</style>
