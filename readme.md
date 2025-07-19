# 🛠️ Dev Test Task: Migrate Django Admin to DRF + Vue Admin Panel

## 🔍 Overview

Your task is to migrate the existing Django admin interface for the `BookLoan` model to a custom admin solution using **Django REST Framework (DRF)** and a **Vue.js-based admin panel**.

You’ll implement backend APIs to manage `BookLoan` entries and build a frontend admin page that supports full CRUD operations.

---

## 📁 References

- Review the logic in `library/admin.py` to understand how `BookLoan` is currently managed in the classic Django admin.
- Use the provided **skeleton files** as a starting point for your implementation.

---

## ✅ Requirements

### Backend (Django + DRF)

- Move the admin logic for `BookLoan` into **`core/admin.py`** using Django REST Framework.
- Define all required models for `BookLoan` in **`library/models.py`**.
- Implement:
  - **Serializers**
  - **Views**
  - **URLs**
  - To support full CRUD operations via API.

### Frontend (Vue.js)

- Build the Vue.js admin page that allows:
  - Viewing all book loans
  - Creating a new loan
  - Editing existing entries
  - Deleting entries
- Use the provided UI skeleton as a base.

---

## ⚙️ Project Setup & Testing

- Add any essential files and classes needed to complete the task.
- Run the following to apply DB changes:

  ```bash
  python manage.py makemigrations
  python manage.py migrate


📝 Documentation
Please include:
- A clear explanation of what you implemented
- Why you made specific design decisions
- How to run or test your code:
- Setup instructions
- Example usage or behavior

💡 Your code and documentation will be the sole basis for evaluation — you do not need to deploy or demonstrate the project running.


📌 Notes
You may consult AI tools (e.g. ChatGPT) for guidance, but do not copy AI-generated code directly.
Focus on:
- Code quality
- Maintainability
- Readability
- Proper use of Django and Vue best practices

Treat this as a real-world professional submission for code review.
