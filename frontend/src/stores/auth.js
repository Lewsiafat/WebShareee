import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
    username: localStorage.getItem('username') || null,
    error: null
  }),
  actions: {
    async login(username, password) {
      try {
        // Clear any previous errors
        this.error = null;

        // Encode credentials for Basic Auth
        const credentials = btoa(`${username}:${password}`);

        // Make the API call
        const response = await axios.post('/api/auth/login', null, {
          headers: {
            'Authorization': `Basic ${credentials}`
          }
        });

        // Assuming success if no error is thrown and status is 200
        if (response.status === 200) {
          this.isAuthenticated = true;
          this.username = username;
          localStorage.setItem('isAuthenticated', 'true');
          localStorage.setItem('username', username);
          return true; // Login successful
        }
      } catch (err) {
        this.isAuthenticated = false;
        this.username = null;
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('username');
        if (err.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          this.error = err.response.data.detail || 'Login failed. Please check your credentials.';
        } else if (err.request) {
          // The request was made but no response was received
          this.error = 'No response from server. Please try again later.';
        } else {
          // Something happened in setting up the request that triggered an Error
          this.error = 'An unexpected error occurred.';
        }
        return false; // Login failed
      }
    },
    logout() {
      this.isAuthenticated = false;
      this.username = null;
      this.error = null;
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('username');
    }
  }
});
