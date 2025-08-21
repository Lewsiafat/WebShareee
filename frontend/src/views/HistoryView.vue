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
          <el-button size="small" @click="handleEdit(scope.row)">Edit</el-button> <!-- New Edit Button -->
          <el-button size="small" type="danger" @click="confirmDelete(scope.row.id)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon class="mt-4"></el-alert>

    <!-- Delete Confirmation Dialog -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="Confirm Deletion"
      width="30%"
      center
    >
      <span>Are you sure you want to delete this page? This action cannot be undone.</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">Cancel</el-button>
          <el-button type="danger" @click="deletePage">Confirm</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Edit Dialog -->
    <el-dialog
      v-model="editDialogVisible"
      title="Edit Page"
      width="40%"
      center
    >
      <el-form :model="currentPageToEdit" label-width="100px">
        <el-form-item label="Page ID">
          <el-input v-model="currentPageToEdit.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="Title">
          <el-input v-model="currentPageToEdit.title"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="saveEdit" :loading="loading">Save</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Refresh } from '@element-plus/icons-vue';
import { useAuthStore } from '../stores/auth';

const pages = ref([]);
const loading = ref(false);
const errorMessage = ref('');

// Delete related
const deleteDialogVisible = ref(false); // Renamed from dialogVisible
const pageToDeleteId = ref(null);

// Edit related
const editDialogVisible = ref(false);
const currentPageToEdit = ref({ id: '', title: '' }); // Initialize with empty object

const authStore = useAuthStore();

const fetchPages = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const response = await axios.get('/api/pages', { headers: authStore.getAuthHeader() }); // Use auth header
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
  deleteDialogVisible.value = true; // Use new dialog variable
};

const deletePage = async () => {
  deleteDialogVisible.value = false;
  if (!pageToDeleteId.value) return;

  loading.value = true;
  errorMessage.value = '';
  try {
    await axios.delete(`/api/pages/${pageToDeleteId.value}`, { headers: authStore.getAuthHeader() }); // Use auth header
    ElMessage.success('Page deleted successfully!');
    fetchPages();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to delete page.';
    ElMessage.error('Deletion failed!');
  } finally {
    loading.value = false;
    pageToDeleteId.value = null;
  }
};

// New Edit methods
const handleEdit = (page) => {
  currentPageToEdit.value = { ...page }; // Create a copy to avoid direct mutation
  editDialogVisible.value = true;
};

const saveEdit = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    await axios.put(`/api/pages/${currentPageToEdit.value.id}`, {
      title: currentPageToEdit.value.title
    }, { headers: authStore.getAuthHeader() }); // Use auth header
    ElMessage.success('Page updated successfully!');
    editDialogVisible.value = false;
    fetchPages(); // Refresh the list
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to update page.';
    ElMessage.error('Update failed!');
  } finally {
    loading.value = false;
  }
};

const viewPage = (url) => {
  window.open(url, '_blank');
};

const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString();
};

onMounted(() => {
  fetchPages();
});
</script>

<style scoped>
/* No scoped styles needed here, using global .page-container */
.header-actions {
  text-align: right;
  margin-bottom: 20px;
}
.mt-4 {
  margin-top: 20px;
}
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>