# Glossary Search

Use the interactive search below to scan terms, aliases, categories, and
statuses. Results update as you type.

<div class="search-panel">
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
</div>

<div id="glossary-search-results" class="search-results"></div>

<script>
  (function () {
    const dataUrl = '../assets/glossary-search.json';
    const searchInput = document.getElementById('glossary-search-input');
    const categorySelect = document.getElementById('glossary-category-select');
    const statusSelect = document.getElementById('glossary-status-select');
    const roleSelect = document.getElementById('glossary-role-select');
    const resultsContainer = document.getElementById('glossary-search-results');

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

    function normalise(value) {
      return (value || '').toLowerCase();
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

    function renderResults() {
      const query = searchInput.value.trim();
      const category = categorySelect.value;
      const status = statusSelect.value;
      const role = roleSelect.value;

      const filtered = terms.filter(
        (item) =>
          matches(item, query) &&
          matchesCategory(item, category) &&
          matchesStatus(item, status) &&
          matchesRole(item, role)
      );

      if (!filtered.length) {
        resultsContainer.innerHTML = '<p class="search-empty">No matching entries yet.</p>';
        return;
      }

      const list = document.createElement('ul');
      list.className = 'search-list';

      filtered.forEach((item) => {
        const li = document.createElement('li');
        li.className = 'search-item';
        const aliases = item.aliases && item.aliases.length
          ? ` <span class="search-aliases">(Aliases: ${item.aliases.join(', ')})</span>`
          : '';
        const categories = item.categories && item.categories.length
          ? `<span class="search-categories">${item.categories.join(', ')}</span>`
          : '';
        const status = item.status ? `<span class="search-status">${item.status}</span>` : '';
        const roles = item.roles && item.roles.length
          ? `<span class="search-roles">${item.roles.map((value) => ROLE_LABELS[value] || value).join(', ')}</span>`
          : '';
        const href = item.slug ? `../terms/${item.slug}/` : '#';
        li.innerHTML = `
          <a href="${href}">${item.term}</a>
          ${aliases}
          <div class="search-meta">${categories} ${status} ${roles}</div>
          <p>${item.short_def || ''}</p>
        `;
        list.appendChild(li);
      });

      resultsContainer.innerHTML = '';
      resultsContainer.appendChild(list);
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
          option.textContent = value;
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
      [searchInput, categorySelect, statusSelect, roleSelect].forEach((element) => {
        element.addEventListener('input', renderResults);
        element.addEventListener('change', renderResults);
      });
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
        attachListeners();
        renderResults();
      })
      .catch((error) => {
        resultsContainer.innerHTML = `<p class="search-error">${error.message}</p>`;
      });
  })();
</script>

<style>
  .search-panel {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .search-field {
    display: flex;
    flex-direction: column;
    min-width: 200px;
    font-weight: 600;
  }
  .search-field input,
  .search-field select {
    margin-top: 0.25rem;
    padding: 0.5rem;
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
  .search-meta {
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light, #555);
    margin: 0.25rem 0;
  }
  .search-categories::before {
    content: 'Categories: ';
    font-weight: 600;
  }
  .search-status::before {
    content: 'Status: ';
    font-weight: 600;
    margin-left: 0.75rem;
  }
  .search-roles::before {
    content: 'Roles: ';
    font-weight: 600;
    margin-left: 0.75rem;
  }
  .search-aliases {
    font-size: 0.85rem;
    color: var(--md-default-fg-color--light, #555);
  }
  .search-empty,
  .search-error {
    color: var(--md-accent-fg-color, #d35400);
    font-weight: 600;
  }
</style>
