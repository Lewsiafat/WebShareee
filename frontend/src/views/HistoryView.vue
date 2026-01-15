<template>
  <div class="page-container">
    <div class="view-header">
       <h1>Upload History</h1>
       <el-button type="primary" @click="fetchPages" :icon="Refresh" circle></el-button>
    </div>

    <div class="glass-panel table-container">
      <el-table
        :data="pages"
        v-loading="loading"
        style="width: 100%"
        class="custom-table"
        :header-cell-style="{ background: 'transparent', color: 'var(--text-secondary)' }"
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="title" label="Title" min-width="180">
          <template #default="scope">
             <span class="title-text">{{ scope.row.title || 'Untitled Page' }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="Page URL" min-width="250">
          <template #default="scope">
            <el-link :href="scope.row.url" target="_blank" type="primary" class="url-link">
              {{ scope.row.url }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="view_count" label="Views" width="100" align="center">
           <template #default="scope">
             <el-tag effect="light" round size="small">{{ scope.row.view_count }}</el-tag>
           </template>
        </el-table-column>
        
        <el-table-column label="Created" width="180">
          <template #default="scope">
            <span class="date-text">{{ formatDate(scope.row.created_at) }}</span>
          </template>
        </el-table-column>
        
        <el-table-column label="Actions" width="220" fixed="right">
          <template #default="scope">
            <div class="actions-group">
              <el-tooltip content="Preview" placement="top">
                <el-button size="small" circle :icon="View" @click="viewPage(scope.row.url)" />
              </el-tooltip>
              <el-tooltip content="Edit" placement="top">
                <el-button size="small" circle :icon="Edit" type="warning" plain @click="handleEdit(scope.row)" />
              </el-tooltip>
              <el-tooltip content="Delete" placement="top">
                 <el-button size="small" circle :icon="Delete" type="danger" plain @click="confirmDelete(scope.row.id)" />
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      class="mt-4"
    />

    <!-- Delete Confirmation Dialog -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="Confirm Deletion"
      width="30%"
      center
      class="custom-dialog"
    >
      <span class="dialog-msg">Are you sure you want to delete this page? This action cannot be undone.</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">Cancel</el-button>
          <el-button type="danger" @click="deletePage">Confirm Delete</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Edit Dialog -->
    <el-dialog v-model="editDialogVisible" title="Edit Page Details" width="400px" center class="custom-dialog">
      <el-form :model="currentPageToEdit" label-position="top">
        <el-form-item label="Page ID">
          <el-input v-model="currentPageToEdit.id" disabled />
        </el-form-item>
        <el-form-item label="Title">
          <el-input v-model="currentPageToEdit.title" placeholder="Enter new title" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="saveEdit" :loading="loading">Save Changes</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
import { Refresh, View, Edit, Delete } from "@element-plus/icons-vue";
import { useAuthStore } from "../stores/auth";

const pages = ref([]);
const loading = ref(false);
const errorMessage = ref("");

// Delete related
const deleteDialogVisible = ref(false);
const pageToDeleteId = ref(null);

// Edit related
const editDialogVisible = ref(false);
const currentPageToEdit = ref({ id: "", title: "" });

const authStore = useAuthStore();

const fetchPages = async () => {
  loading.value = true;
  errorMessage.value = "";
  try {
    const response = await axios.get("/api/pages", {
      headers: authStore.getAuthHeader(),
    });
    pages.value = response.data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Failed to fetch pages.";
    ElMessage.error("Failed to load history!");
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (pageId) => {
  pageToDeleteId.value = pageId;
  deleteDialogVisible.value = true;
};

const deletePage = async () => {
  deleteDialogVisible.value = false;
  if (!pageToDeleteId.value) return;

  loading.value = true;
  errorMessage.value = "";
  try {
    await axios.delete(`/api/pages/${pageToDeleteId.value}`, {
      headers: authStore.getAuthHeader(),
    });
    ElMessage.success("Page deleted successfully!");
    fetchPages();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Failed to delete page.";
    ElMessage.error("Deletion failed!");
  } finally {
    loading.value = false;
    pageToDeleteId.value = null;
  }
};

const handleEdit = (page) => {
  currentPageToEdit.value = { ...page };
  editDialogVisible.value = true;
};

const saveEdit = async () => {
  loading.value = true;
  errorMessage.value = "";
  try {
    await axios.put(
      `/api/pages/${currentPageToEdit.value.id}`,
      { title: currentPageToEdit.value.title },
      { headers: authStore.getAuthHeader() },
    );
    ElMessage.success("Page updated successfully!");
    editDialogVisible.value = false;
    fetchPages();
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Failed to update page.";
    ElMessage.error("Update failed!");
  } finally {
    loading.value = false;
  }
};

const viewPage = (url) => {
  window.open(url, "_blank");
};

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString('en-US', { 
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
  });
};

onMounted(() => {
  fetchPages();
});
</script>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.table-container {
  border-radius: 16px;
  overflow: hidden;
  padding: 8px;
  background: var(--bg-card);
}

.custom-table {
  --el-table-border-color: transparent;
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-fill-color-light: rgba(0,0,0,0.02);
}

.title-text {
  font-weight: 600;
  color: var(--text-main);
}

.url-link {
  font-family: monospace;
  font-size: 13px;
}

.date-text {
  color: var(--text-secondary);
  font-size: 13px;
}

.actions-group {
  display: flex;
  gap: 8px;
}

.mt-4 {
  margin-top: 20px;
}

.dialog-msg {
  font-size: 16px;
  color: var(--text-main);
}
</style>
