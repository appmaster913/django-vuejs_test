<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">{{ editLoan ? 'Edit Loan' : 'Create Loan' }}</h2>
      <div v-if="errors.length" class="mb-4 p-4 bg-red-100 text-red-700 border border-red-400 rounded">
        <ul>
          <li v-for="error in errors" :key="error" class="mb-1">{{ error }}</li>
        </ul>
      </div>
      <form @submit.prevent="save" aria-label="Loan Form">
        <div class="mb-4">
          <label for="student-select" class="block text-sm font-medium">Student</label>
          <select
            id="student-select"
            v-model="form.student_id"
            class="border p-2 w-full rounded focus:ring-2 focus:ring-blue-500"
            required
            aria-required="true"
            :disabled="isSubmitting"
            @change="validateStudentAndBook"
          >
            <option value="" disabled>Select a student</option>
            <option v-if="students.length === 0" disabled>No students available</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.full_name }} ({{ student.student_id }})
            </option>
          </select>
        </div>
        <div class="mb-4">
          <label for="book-select" class="block text-sm font-medium">Book</label>
          <select
            id="book-select"
            v-model="form.book_id"
            class="border p-2 w-full rounded focus:ring-2 focus:ring-blue-500"
            required
            aria-required="true"
            :disabled="isSubmitting"
            @change="validateStudentAndBook"
          >
            <option value="" disabled>Select a book</option>
            <option v-if="books.length === 0" disabled>No books available</option>
            <option
              v-for="book in availableBooks"
              :key="book.id"
              :value="book.id"
              :disabled="book.available_copies <= 0 && (!editLoan || editLoan.book.id !== book.id)"
            >
              {{ book.title }} by {{ book.author }} (Total: {{ book.total_copies }}, Available: {{ book.available_copies }})
            </option>
          </select>
        </div>
        <div class="mb-4">
          <label for="loan-date" class="block text-sm font-medium">Loan Date</label>
          <input
            id="loan-date"
            v-model="form.loan_date"
            type="date"
            class="border p-2 w-full rounded focus:ring-2 focus:ring-blue-500"
            required
            aria-required="true"
            :disabled="isSubmitting"
            @change="validateDates"
          />
        </div>
        <div class="mb-4">
          <label for="due-date" class="block text-sm font-medium">Due Date</label>
          <input
            id="due-date"
            v-model="form.due_date"
            type="date"
            class="border p-2 w-full rounded focus:ring-2 focus:ring-blue-500"
            required
            aria-required="true"
            :disabled="isSubmitting"
            @change="validateDates"
          />
        </div>
        <div class="mb-4">
          <label for="return-date" class="block text-sm font-medium">Return Date</label>
          <input
            id="return-date"
            v-model="form.return_date"
            type="date"
            class="border p-2 w-full rounded focus:ring-2 focus:ring-blue-500"
            :disabled="isSubmitting"
            @change="validateDates"
          />
        </div>
        <div class="flex justify-end gap-2">
          <button
            type="button"
            @click="cancel"
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 focus:ring-2 focus:ring-gray-500"
            :disabled="isSubmitting"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="isSubmitting || errors.length > 0 || !form.student_id || !form.book_id"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 disabled:bg-blue-300"
          >
            {{ isSubmitting ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
const component = {
  props: {
    editLoan: {
      type: Object,
      default: null
    },
    students: {
      type: Array,
      required: true
    },
    books: {
      type: Array,
      required: true
    },
    createLoan: {
      type: Function,
      default: null
    }
  },
  emits: ['save', 'cancel'],
  data() {
    const today = new Date();
    const defaultDueDate = new Date(today.setDate(today.getDate() + 14)).toISOString().split('T')[0];
    return {
      form: this.editLoan
        ? this.initializeEditForm(this.editLoan)
        : {
            student_id: null,
            book_id: null,
            loan_date: today.toISOString().split('T')[0],
            due_date: defaultDueDate,
            return_date: null
          },
      errors: [],
      isSubmitting: false,
      lastSubmissionTime: 0
    };
  },
  computed: {
    availableBooks() {
      return this.books.map(book => ({
        ...book,
        disabled: book.available_copies <= 0 && (!this.editLoan || this.editLoan.book.id !== book.id)
      }));
    }
  },
  watch: {
    editLoan(newLoan) {
      console.log('editLoan changed:', newLoan);
      const today = new Date();
      const defaultDueDate = new Date(today.setDate(today.getDate() + 14)).toISOString().split('T')[0];
      this.form = newLoan
        ? this.initializeEditForm(newLoan)
        : {
            student_id: null,
            book_id: null,
            loan_date: today.toISOString().split('T')[0],
            due_date: defaultDueDate,
            return_date: null
          };
      this.errors = [];
      this.validateForm();
    }
  },
  methods: {
    initializeEditForm(loan) {
      console.log('Initializing edit form with loan:', loan);
      if (!loan || !loan.student || !loan.book) {
        console.error('Invalid editLoan data:', loan);
        return {
          student_id: null,
          book_id: null,
          loan_date: new Date().toISOString().split('T')[0],
          due_date: new Date(new Date().setDate(new Date().getDate() + 14)).toISOString().split('T')[0],
          return_date: null
        };
      }
      return {
        id: loan.id,
        student_id: loan.student.id,
        book_id: loan.book.id,
        loan_date: loan.loan_date,
        due_date: loan.due_date,
        return_date: loan.return_date || null
      };
    },
    validateDates() {
      this.errors = this.errors.filter(error => !error.includes('date'));
      const loanDate = new Date(this.form.loan_date);
      const dueDate = new Date(this.form.due_date);
      const returnDate = this.form.return_date ? new Date(this.form.return_date) : null;

      if (this.form.loan_date && this.form.due_date && dueDate < loanDate) {
        this.errors.push('Due date must be on or after loan date.');
      }
      if (this.form.return_date && returnDate < loanDate) {
        this.errors.push('Return date must be on or after loan date.');
      }
      if (this.form.loan_date && this.form.due_date && dueDate > new Date(loanDate.getTime() + 30 * 24 * 60 * 60 * 1000)) {
        this.errors.push('Due date cannot be more than 30 days from loan date.');
      }
    },
    async validateStudentAndBook() {
      console.log('Validating student and book:', this.form.student_id, this.form.book_id);
      // Remove previous active loan errors
      this.errors = this.errors.filter(error => !error.includes('already has an active loan'));

      // Only validate if both student and book are selected
      if (!this.form.student_id || !this.form.book_id) {
        return;
      }

      // Skip validation if editing the same loan with unchanged student and book
      if (
        this.editLoan &&
        this.form.student_id &&
        this.form.book_id &&
        this.editLoan.student.id === this.form.student_id &&
        this.editLoan.book.id === this.form.book_id
      ) {
        console.log('Skipping active loan validation for unchanged edit');
        return;
      }

      try {
        const response = await window.axios.get('/api/bookloans/check_active_loan/', {
          params: {
            student: this.form.student_id,
            book: this.form.book_id
          }
        });
        if (response.data.length > 0) {
          const student = this.students.find(s => s.id === this.form.student_id);
          const book = this.books.find(b => b.id === this.form.book_id);
          this.errors.push(`${student.full_name} already has an active loan for ${book.title}.`);
        }
      } catch (error) {
        console.error('Error checking active loan:', error);
        this.errors.push('Error checking active loan status. Please try again.');
      }
    },
    validateForm() {
      this.errors = [];
      this.validateDates();

      if (!this.form.student_id) {
        this.errors.push('Please select a student.');
      }
      if (!this.form.book_id) {
        this.errors.push('Please select a book.');
      }

      const selectedBook = this.books.find(book => book.id === this.form.book_id);
      if (selectedBook && selectedBook.available_copies <= 0 && (!this.editLoan || this.editLoan.book.id !== selectedBook.id)) {
        this.errors.push(`No copies available for ${selectedBook.title}.`);
      }

      // Run async validation for active loans
      this.validateStudentAndBook();
    },
    async save(event) {
      event.preventDefault();
      const now = Date.now();
      if (this.isSubmitting || now - this.lastSubmissionTime < 1000) {
        return;
      }
      this.lastSubmissionTime = now;
      this.isSubmitting = true;
      this.errors = [];

      // Ensure async validation is complete before proceeding
      await this.validateStudentAndBook();
      this.validateForm();
      if (this.errors.length > 0) {
        this.isSubmitting = false;
        return;
      }

      try {
        if (this.editLoan) {
          // Handle update loan
          await window.axios.put(`/api/bookloans/${this.editLoan.id}/`, {
            student_id: this.form.student_id,
            book_id: this.form.book_id,
            loan_date: this.form.loan_date,
            due_date: this.form.due_date,
            return_date: this.form.return_date || null
          });
          this.$emit('save', this.form);
        } else {
          // Handle create loan by calling the createLoan prop
          await this.createLoan({
            student_id: this.form.student_id,
            book_id: this.form.book_id,
            loan_date: this.form.loan_date,
            due_date: this.form.due_date,
            return_date: this.form.return_date || null
          });
        }

        this.errors = [];
        const today = new Date();
        const defaultDueDate = new Date(today.setDate(today.getDate() + 14)).toISOString().split('T')[0];
        this.form = {
          student_id: null,
          book_id: null,
          loan_date: today.toISOString().split('T')[0],
          due_date: defaultDueDate,
          return_date: null
        };
        this.$emit('cancel'); // Close modal after successful save
      } catch (error) {
        this.errors = [];
        if (error.response?.data) {
          const errorData = error.response.data;
          if (errorData.non_field_errors) {
            this.errors.push(...errorData.non_field_errors);
          } else {
            for (const [field, messages] of Object.entries(errorData)) {
              this.errors.push(...(Array.isArray(messages) ? messages : [messages]).map(msg => `${field}: ${msg}`));
            }
          }
        } else {
          this.errors.push(`Error: ${error.message || 'An unexpected error occurred'}`);
        }
      } finally {
        this.isSubmitting = false;
      }
    },
    cancel() {
      this.errors = [];
      this.$emit('cancel');
    }
  }
};
</script>