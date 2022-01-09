const deleteModalButtons = document.getElementsByClassName('delete-modal-button');
const deleteForm = document.getElementById('delete-form');
const deleteDate = document.getElementById('delete-date')
const deleteCategory = document.getElementById('delete-category')
const deleteAmount = document.getElementById('delete-amount')
const deleteDescription = document.getElementById('delete-description')

for (const button of deleteModalButtons) {
  button.addEventListener('click', () => {
    deleteForm.action = button.dataset.deleteurl;
    deleteDate.textContent = `Date : ${button.dataset.date}`;
    deleteCategory.textContent = `Category : ${button.dataset.category}`;
    deleteAmount.textContent = `Amount : ${button.dataset.amount}`;
    deleteDescription.textContent = `Description : ${button.dataset.description}`;
  });
}
