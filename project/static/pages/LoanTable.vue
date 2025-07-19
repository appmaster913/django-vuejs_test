<template>
  <div>
    <table class="w-full border-collapse bg-white shadow-md">
      <thead>
        <tr class="bg-gray-200">
          <th
            class="border p-2 text-center cursor-pointer hover:bg-gray-300"
            @click="sortBy('student')"
          >
            Student
            <span v-if="sortColumn === 'student'">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th
            class="border p-2 text-center cursor-pointer hover:bg-gray-300"
            @click="sortBy('book')"
          >
            Book
            <span v-if="sortColumn === 'book'">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th
            class="border p-2 text-center cursor-pointer hover:bg-gray-300"
            @click="sortBy('loan_date')"
          >
            Loan Date
            <span v-if="sortColumn === 'loan_date'">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th
            class="border p-2 text-center cursor-pointer hover:bg-gray-300"
            @click="sortBy('due_date')"
          >
            Due Date
            <span v-if="sortColumn === 'due_date'">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th
            class="border p-2 text-center cursor-pointer hover:bg-gray-300"
            @click="sortBy('return_date')"
          >
            Return Date
            <span v-if="sortColumn === 'return_date'">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th
            class="border p-2 text-center cursor-pointer hover:bg-gray-300"
            @click="sortBy('overdue')"
          >
            Overdue
            <span v-if="sortColumn === 'overdue'">
              {{ sortDirection === 'asc' ? '↑' : '↓' }}
            </span>
          </th>
          <th class="border p-2 text-center">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in loans" :key="loan.id" class="hover:bg-gray-50">
          <td class="border p-2 text-center">{{ loan.student.full_name }}</td>
          <td class="border p-2 text-center">{{ loan.book.title }}</td>
          <td class="border p-2 text-center">{{ loan.loan_date }}</td>
          <td class="border p-2 text-center">{{ loan.due_date }}</td>
          <td class="border p-2 text-center">{{ loan.return_date || '-' }}</td>
          <td class="border p-2 text-center">
            <span :class="{ 'text-red-500': isOverdue(loan) }">{{ isOverdue(loan) ? 'Yes' : 'No' }}</span>
          </td>
          <td class="border p-2 text-center">
            <button
              @click="openEditModal(loan)"
              class="bg-yellow-500 text-white px-2 py-1 rounded mr-2 hover:bg-yellow-600 focus:ring-2 focus:ring-yellow-500"
            >
              Edit
            </button>
            <button
              @click="confirmDelete(loan.id)"
              class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600 focus:ring-2 focus:ring-red-500"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="mt-4 flex justify-between">
      <button
        v-if="previousPage"
        @click="fetchLoans(previousPage)"
        class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 focus:ring-2 focus:ring-gray-500"
      >
        Previous
      </button>
      <button
        v-if="nextPage"
        @click="fetchLoans(nextPage)"
        class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 focus:ring-2 focus:ring-gray-500"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
const component = {
  props: {
    loans: {
      type: Array,
      required: true
    },
    previousPage: {
      type: String,
      default: null
    },
    nextPage: {
      type: String,
      default: null
    },
    sortColumn: {
      type: String,
      default: ''
    },
    sortDirection: {
      type: String,
      default: 'asc'
    }
  },
  emits: ['open-modal', 'fetch-loans', 'delete-loan', 'sort'],
  methods: {
    async fetchLoans(url) {
      this.$emit('fetch-loans', url);
    },
    confirmDelete(id) {
      if (confirm('Are you sure you want to delete this loan?')) {
        this.$emit('delete-loan', id);
      }
    },
    isOverdue(loan) {
      return !loan.return_date && new Date() > new Date(loan.due_date);
    },
    sortBy(column) {
      const direction = this.sortColumn === column && this.sortDirection === 'asc' ? 'desc' : 'asc';
      this.$emit('sort', { column, direction });
    },
    openEditModal(loan) {
      console.log('Emitting open-modal from LoanTable with loan:', loan);
      this.$emit('open-modal', loan);
    }
  }
};
</script>