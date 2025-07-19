<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Book Loan Admin Panel</h1>
    <div v-if="loading" class="text-center py-4">Loading...</div>
    <div v-else-if="error" class="text-red-500 p-4 bg-red-100 border border-red-400 rounded">
      {{ error }}
    </div>
    <loan-list
      v-else
      :key="loanListKey"
      @open-create-modal="openCreateModal"
      @open-edit-modal="openEditModal"
      @delete-loan="deleteLoan"
    ></loan-list>
    <loan-form
      v-if="showCreateModal"
      :students="students"
      :books="books"
      :create-loan="createLoan"
      @save="createLoan"
      @cancel="showCreateModal = false"
    ></loan-form>
    <loan-form
      v-if="showEditModal"
      :editLoan="editLoan"
      :students="students"
      :books="books"
      @save="updateLoan"
      @cancel="showEditModal = false"
    ></loan-form>
  </div>
</template>

<script>
const component = {
  components: {
    'loan-list': Vue.defineAsyncComponent(() =>
      fetch('/static/pages/LoanList.vue')
        .then(response => {
          if (!response.ok) throw new Error('Failed to load LoanList.vue');
          return response.text();
        })
        .then(text => {
          const templateMatch = text.match(/<template>([\s\S]*?)<\/template>/);
          const scriptMatch = text.match(/<script>([\s\S]*?)<\/script>/);
          if (!templateMatch || !scriptMatch) throw new Error('Invalid .vue file format');
          const template = templateMatch[1];
          const scriptContent = scriptMatch[1];
          const component = eval(`(() => {${scriptContent}; return component;})()`);
          component.template = template;
          return component;
        })
        .catch(error => {
          console.error('Error loading LoanList.vue:', error);
          throw error;
        })
    ),
    'loan-form': Vue.defineAsyncComponent(() =>
      fetch('/static/pages/LoanForm.vue')
        .then(response => {
          if (!response.ok) throw new Error('Failed to load LoanForm.vue');
          return response.text();
        })
        .then(text => {
          const templateMatch = text.match(/<template>([\s\S]*?)<\/template>/);
          const scriptMatch = text.match(/<script>([\s\S]*?)<\/script>/);
          if (!templateMatch || !scriptMatch) throw new Error('Invalid .vue file format');
          const template = templateMatch[1];
          const scriptContent = scriptMatch[1];
          const component = eval(`(() => {${scriptContent}; return component;})()`);
          component.template = template;
          return component;
        })
        .catch(error => {
          console.error('Error loading LoanForm.vue:', error);
          throw error;
        })
    )
  },
  data() {
    return {
      students: [],
      books: [],
      showCreateModal: false,
      showEditModal: false,
      editLoan: null,
      loading: true,
      error: null,
      loanListKey: 0 // Key to force re-render of loan-list after CRUD operations
    };
  },
  async mounted() {
    try {
      await Promise.all([this.fetchStudents(), this.fetchBooks()]);
      this.loading = false;
    } catch (error) {
      this.loading = false;
      this.error = this.getErrorMessage(error);
    }
  },
  methods: {
    async fetchStudents() {
      const response = await window.axios.get('/api/students/');
      this.students = response.data.results || [];
    },
    async fetchBooks() {
      const response = await window.axios.get('/api/books/');
      this.books = response.data.results || [];
    },
    openCreateModal() {
      console.log('Opening create modal');
      this.error = null;
      this.showCreateModal = true;
      this.showEditModal = false;
      this.editLoan = null;
    },
    openEditModal(loan) {
      console.log('Opening edit modal with loan:', loan);
      this.error = null;
      this.editLoan = { ...loan }; // Ensure a deep copy to avoid mutating original
      this.showEditModal = true;
      this.showCreateModal = false;
    },
    async createLoan(form) {
      this.error = null;
      try {
        await window.axios.post('/api/bookloans/', {
          student_id: form.student_id,
          book_id: form.book_id,
          loan_date: form.loan_date,
          due_date: form.due_date,
          return_date: form.return_date || null
        });
        this.showCreateModal = false;
        this.loanListKey += 1; // Force re-render of loan-list
        await this.fetchBooks(); // Refresh books to update available_copies
      } catch (error) {
        console.error('Error creating loan:', error);
        this.error = this.getErrorMessage(error);
        throw error; // Re-throw to let LoanForm handle error display
      }
    },
    async updateLoan(form) {
      this.error = null;
      try {
        await window.axios.put(`/api/bookloans/${this.editLoan.id}/`, {
          student_id: form.student_id,
          book_id: form.book_id,
          loan_date: form.loan_date,
          due_date: form.due_date,
          return_date: form.return_date || null
        });
        this.showEditModal = false;
        this.loanListKey += 1; // Force re-render of loan-list
        await this.fetchBooks(); // Refresh books to update available_copies
      } catch (error) {
        console.error('Error updating loan:', error);
        this.error = this.getErrorMessage(error);
        throw error; // Re-throw to let LoanForm handle error display
      }
    },
    async deleteLoan(loanId) {
      this.error = null;
      try {
        await window.axios.delete(`/api/bookloans/${loanId}/`);
        this.loanListKey += 1; // Force re-render of loan-list
        await this.fetchBooks(); // Refresh books to update available_copies
      } catch (error) {
        console.error('Error deleting loan:', error);
        this.error = this.getErrorMessage(error);
      }
    },
    getErrorMessage(error) {
      return (
        error.response?.data?.non_field_errors?.[0] ||
        error.response?.data?.book ||
        error.response?.data?.due_date ||
        error.response?.data?.return_date ||
        error.response?.data?.detail ||
        'An unexpected error occurred'
      );
    }
  }
};
</script>