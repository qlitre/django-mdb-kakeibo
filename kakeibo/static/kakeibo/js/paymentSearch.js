document.addEventListener('DOMContentLoaded', e => {
  const searchForm = document.getElementById('search-form');

  for (const check of document.getElementsByName('search_category')) {
    check.addEventListener('change', () => {
      searchForm.submit();
    });
  }

  for (const check of document.getElementsByName('year')) {
    check.addEventListener('change', () => {
      searchForm.submit();
    });
  }

  for (const check of document.getElementsByName('month')) {
    check.addEventListener('change', () => {
      searchForm.submit();
    });
  }
});
