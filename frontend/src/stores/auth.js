import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: localStorage.getItem("isAuthenticated") === "true",
    username: localStorage.getItem("username") || null,
    basicAuthToken: localStorage.getItem("basicAuthToken") || null, // Store the base64 token
    error: null,
  }),
  actions: {
    async login(username, password) {
      try {
        this.error = null;
        const credentials = btoa(`${username}:${password}`);

        const response = await axios.post("/api/auth/login", null, {
          headers: {
            Authorization: `Basic ${credentials}`,
          },
        });

        if (response.status === 200) {
          this.isAuthenticated = true;
          this.username = username;
          this.basicAuthToken = credentials; // Store the token
          localStorage.setItem("isAuthenticated", "true");
          localStorage.setItem("username", username);
          localStorage.setItem("basicAuthToken", credentials); // Persist the token
          return true;
        }
      } catch (err) {
        this.isAuthenticated = false;
        this.username = null;
        this.basicAuthToken = null;
        localStorage.removeItem("isAuthenticated");
        localStorage.removeItem("username");
        localStorage.removeItem("basicAuthToken");
        if (err.response) {
          this.error =
            err.response.data.detail ||
            "Login failed. Please check your credentials.";
        } else if (err.request) {
          this.error = "No response from server. Please try again later.";
        } else {
          this.error = "An unexpected error occurred.";
        }
        return false;
      }
    },
    logout() {
      this.isAuthenticated = false;
      this.username = null;
      this.basicAuthToken = null;
      this.error = null;
      localStorage.removeItem("isAuthenticated");
      localStorage.removeItem("username");
      localStorage.removeItem("basicAuthToken");
    },

    async changePassword(oldPassword, newPassword) {
      if (!this.isAuthenticated) {
        this.error = "User is not authenticated.";
        return false;
      }
      try {
        this.error = null;
        const response = await axios.put(
          "/api/admin/password",
          { old_password: oldPassword, new_password: newPassword },
          { headers: this.getAuthHeader() },
        );

        if (response.status === 200) {
          // Update the stored token with the new password
          const newCredentials = btoa(`${this.username}:${newPassword}`);
          this.basicAuthToken = newCredentials;
          localStorage.setItem("basicAuthToken", newCredentials);
          return true;
        }
      } catch (err) {
        this.error = err.response?.data?.detail || "Failed to change password.";
        return false;
      }
    },

    async changeUsername(newUsername, password) {
      if (!this.isAuthenticated) {
        this.error = "User is not authenticated.";
        return false;
      }
      try {
        this.error = null;
        const response = await axios.put(
          "/api/admin/username",
          { new_username: newUsername, password: password },
          { headers: this.getAuthHeader() },
        );

        if (response.status === 200) {
          // Update username and token
          const newCredentials = btoa(`${newUsername}:${password}`);
          this.username = newUsername;
          this.basicAuthToken = newCredentials;
          localStorage.setItem("username", newUsername);
          localStorage.setItem("basicAuthToken", newCredentials);
          return true;
        }
      } catch (err) {
        this.error = err.response?.data?.detail || "Failed to change username.";
        return false;
      }
    },
    getAuthHeader() {
      if (this.isAuthenticated && this.basicAuthToken) {
        return { Authorization: `Basic ${this.basicAuthToken}` };
      }
      return {};
    },
  },
});
