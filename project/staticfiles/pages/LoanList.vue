<template>
  <div>
    <div class="mb-4 flex gap-4">
      <input
        v-model="searchQuery"
        placeholder="Search by student or book..."
        class="border p-2 rounded w-1/3 focus:ring-2 focus:ring-blue-500"
      />
      <button
        @click="$emit('open-create-modal')"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:ring-2 focus:ring-blue-500"
      >
        Create Loan
      </button>
    </div>
    <div v-if="error" class="text-red-500 p-4 bg-red-100 border border-red-400 rounded mb-4">
      {{ error }}
    </div>
    <loan-table
      :loans="loans"
      :previousPage="previousPage"
      :nextPage="nextPage"
      :sortColumn="sortColumn"
      :sortDirection="sortDirection"
      @fetch-loans="fetchLoans"
      @open-modal="handleEditModal"
      @delete-loan="handleDeleteLoan"
      @sort="handleSort"
    ></loan-table>
  </div>
</template>

<script>
const component = {
  components: {
    'loan-table': Vue.defineAsyncComponent(() =>
      fetch('/static/pages/LoanTable.vue')
        .then(response => {
          if (!response.ok) throw new Error('Failed to load LoanTable.vue');
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
          console.error('Error loading LoanTable.vue:', error);
          throw error;
        })
    )
  },
  data() {
    return {
      loans: [],
      searchQuery: '',
      loanDateFilter: '',
      previousPage: null,
      nextPage: null,
      error: null,
      sortColumn: '',
      sortDirection: 'asc'
    };
  },
  watch: {
    searchQuery() {
      this.fetchLoans();
    },
    loanDateFilter() {
      this.fetchLoans();
    }
  },
  mounted() {
    this.fetchLoans();
  },
  methods: {
    async fetchLoans(url = '/api/bookloans/') {
      try {
        const params = {};
        if (this.searchQuery) params.search = this.searchQuery;
        if (this.loanDateFilter) params.loan_date = this.loanDateFilter;
        const response = await window.axios.get(url, { params });
        this.loans = response.data.results || [];
        this.previousPage = response.data.previous;
        this.nextPage = response.data.next;
        this.error = null;
        // Apply sorting after fetching
        if (this.sortColumn) {
          this.sortLoans();
        }
      } catch (error) {
        console.error('Error fetching loans:', error);
        this.error = 'Error fetching loans: ' + (error.response?.data?.detail || error.message);
        this.loans = [];
      }
    },
    handleDeleteLoan(loanId) {
      this.$emit('delete-loan', loanId); // Propagate delete event to parent
    },
    handleEditModal(loan) {
      console.log('Emitting open-edit-modal with loan:', loan);
      this.$emit('open-edit-modal', loan);
    },
    handleSort({ column, direction }) {
      this.sortColumn = column;
      this.sortDirection = direction;
      this.sortLoans();
    },
    sortLoans() {
      if (!this.sortColumn) return;
      const direction = this.sortDirection === 'asc' ? 1 : -1;
      this.loans.sort((a, b) => {
        let valueA, valueB;
        switch (this.sortColumn) {
          case 'student':
            valueA = a.student.full_name.toLowerCase();
            valueB = b.student.full_name.toLowerCase();
            break;
          case 'book':
            valueA = a.book.title.toLowerCase();
            valueB = b.book.title.toLowerCase();
            break;
          case 'loan_date':
            valueA = new Date(a.loan_date);
            valueB = new Date(b.loan_date);
            break;
          case 'due_date':
            valueA = new Date(a.due_date);
            valueB = new Date(b.due_date);
            break;
          case 'return_date':
            valueA = a.return_date ? new Date(a.return_date) : null;
            valueB = b.return_date ? new Date(b.return_date) : null;
            // Handle null return dates
            if (!valueA && !valueB) return 0;
            if (!valueA) return direction * -1;
            if (!valueB) return direction * 1;
            break;
          case 'overdue':
            valueA = this.isOverdue(a) ? 1 : 0;
            valueB = this.isOverdue(b) ? 1 : 0;
            break;
          default:
            return 0;
        }
        if (valueA < valueB) return -1 * direction;
        if (valueA > valueB) return 1 * direction;
        return 0;
      });
    },
    isOverdue(loan) {
      return !loan.return_date && new Date() > new Date(loan.due_date);
    }
  }
};
</script>