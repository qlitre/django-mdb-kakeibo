document.addEventListener('DOMContentLoaded', e => {
  const searchForm = document.getElementById('search-form');

  for (const check of document.getElementsByName('payment_category')) {
    check.addEventListener('change', () => {
      searchForm.submit();
    });
  }
  for (const check of document.getElementsByName('income_category')) {
    check.addEventListener('change', () => {
      searchForm.submit();
    });
  }

  for (const check of document.getElementsByName('graph_visible')) {
    check.addEventListener('change', () => {
      searchForm.submit();
    })
  }
});
