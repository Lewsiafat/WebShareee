<template>
  <div class="page-container">
    <h1>Upload History</h1>

    <div class="header-actions">
      <el-button type="primary" @click="fetchPages" :icon="Refresh">Refresh List</el-button>
    </div>

    <el-table :data="pages" v-loading="loading" style="width: 100%" border class="mt-4">
      <el-table-column prop="title" label="Title" width="180"></el-table-column>
      <el-table-column prop="id" label="Page ID" width="120"></el-table-column>
      <el-table-column label="URL" width="250">
        <template #default="scope">
          <el-link :href="scope.row.url" target="_blank" type="primary">{{ scope.row.url }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="Views" width="80"></el-table-column>
      <el-table-column label="Created At" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="Actions">
        <template #default="scope">
          <el-button size="small" @click="viewPage(scope.row.url)">View</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(scope.row.id)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon class="mt-4"></el-alert>

    <el-dialog
      v-model="dialogVisible"
      title="Confirm Deletion"
      width="30%"
      center
    >
      <span>Are you sure you want to delete this page? This action cannot be undone.</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="danger" @click="deletePage">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Refresh } from '@element-plus/icons-vue'; // Import the icon
import { useAuthStore } from '../stores/auth'; // Import auth store

const pages = ref([]);
const loading = ref(false);
const errorMessage = ref('');
const dialogVisible = ref(false);
const pageToDeleteId = ref(null);

const authStore = useAuthStore(); // Get auth store instance

const fetchPages = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const headers = {};
    if (authStore.isAuthenticated && authStore.username) {
      // Assuming password is not stored on frontend,
      // for a real app, you'd use a token or session.
      // For Basic Auth, you'd need to re-authenticate or use a token.
      // For simplicity, we'll assume a token-based auth or session is established after login.
      // If the backend requires Basic Auth for every request, you'd need to pass it here.
      // Example: headers['Authorization'] = `Basic ${btoa(`${authStore.username}:${authStore.password}`)}`;
    }
    const response = await axios.get('/api/pages', { headers });
    pages.value = response.data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to fetch pages.';
    ElMessage.error('Failed to load history!');
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (pageId) => {
  pageToDeleteId.value = pageId;
  dialogVisible.value = true;
};

const deletePage = async () => {
  dialogVisible.value = false;
  if (!pageToDeleteId.value) return;

  loading.value = true;
  errorMessage.value = '';
  try {
    const headers = {};
    if (authStore.isAuthenticated && authStore.username) {
      // Same auth considerations as fetchPages
    }
    await axios.delete(`/api/pages/${pageToDeleteId.value}`, { headers });
    ElMessage.success('Page deleted successfully!');
    fetchPages(); // Refresh the list
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to delete page.';
    ElMessage.error('Deletion failed!');
  } finally {
    loading.value = false;
    pageToDeleteId.value = null;
  }
};

const viewPage = (url) => {
  window.open(url, '_blank');
};

const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString(); // Adjust format as needed
};

onMounted(() => {
  fetchPages();
});
</script>

<style scoped>
.history-container {
  max-width: 1000px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
.header-actions {
  text-align: right;
  margin-bottom: 20px;
}
.mt-4 {
  margin-top: 20px;
}
</style>
