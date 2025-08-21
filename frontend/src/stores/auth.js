import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true',
    username: localStorage.getItem('username') || null,
    basicAuthToken: localStorage.getItem('basicAuthToken') || null, // Store the base64 token
    error: null
  }),
  actions: {
    async login(username, password) {
      try {
        this.error = null;
        const credentials = btoa(`${username}:${password}`);

        const response = await axios.post('/api/auth/login', null, {
          headers: {
            'Authorization': `Basic ${credentials}`
          }
        });

        if (response.status === 200) {
          this.isAuthenticated = true;
          this.username = username;
          this.basicAuthToken = credentials; // Store the token
          localStorage.setItem('isAuthenticated', 'true');
          localStorage.setItem('username', username);
          localStorage.setItem('basicAuthToken', credentials); // Persist the token
          return true;
        }
      } catch (err) {
        this.isAuthenticated = false;
        this.username = null;
        this.basicAuthToken = null;
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('username');
        localStorage.removeItem('basicAuthToken');
        if (err.response) {
          this.error = err.response.data.detail || 'Login failed. Please check your credentials.';
        } else if (err.request) {
          this.error = 'No response from server. Please try again later.';
        } else {
          this.error = 'An unexpected error occurred.';
        }
        return false;
      }
    },
    logout() {
      this.isAuthenticated = false;
      this.username = null;
      this.basicAuthToken = null;
      this.error = null;
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('username');
      localStorage.removeItem('basicAuthToken');
    },
    getAuthHeader() {
      if (this.isAuthenticated && this.basicAuthToken) {
        return { 'Authorization': `Basic ${this.basicAuthToken}` };
      }
      return {};
    }
  }
});