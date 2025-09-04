<template>
  <div class="page-container">
    <h1>Upload Your Content</h1>

    <el-tabs v-model="uploadMode" type="border-card" class="main-tabs">
      <!-- HTML Uploader -->
      <el-tab-pane label="HTML" name="html">
        <el-tabs v-model="activeHtmlTab" type="card">
          <el-tab-pane label="Upload HTML File" name="html-file">
            <el-form :model="htmlFileForm" label-width="120px">
              <el-form-item label="Page Title (Optional)">
                <el-input v-model="htmlFileForm.title" placeholder="Enter page title"></el-input>
              </el-form-item>
              <el-form-item label="HTML File">
                <el-upload
                  drag
                  :auto-upload="false"
                  :on-change="handleHtmlFileChange"
                  :limit="1"
                  accept=".html"
                >
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">Drop HTML file here or <em>click to upload</em></div>
                </el-upload>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitHtmlFile" :loading="loading">Upload File</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="Paste HTML Code" name="html-code">
            <el-form :model="htmlCodeForm" label-width="120px">
              <el-form-item label="Page Title (Optional)">
                <el-input v-model="htmlCodeForm.title" placeholder="Enter page title"></el-input>
              </el-form-item>
              <el-form-item label="HTML Code">
                <el-input
                  v-model="htmlCodeForm.html_content"
                  type="textarea"
                  :rows="10"
                  placeholder="Paste your HTML code here"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitHtmlCode" :loading="loading">Submit Code</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>

      <!-- Markdown Uploader -->
      <el-tab-pane label="Markdown" name="markdown">
        <el-tabs v-model="activeMarkdownTab" type="card">
          <el-tab-pane label="Upload Markdown File" name="md-file">
            <el-form :model="mdFileForm" label-width="120px">
              <el-form-item label="Page Title (Optional)">
                <el-input v-model="mdFileForm.title" placeholder="Enter page title"></el-input>
              </el-form-item>
              <el-form-item label="Markdown File">
                <el-upload
                  drag
                  :auto-upload="false"
                  :on-change="handleMdFileChange"
                  :limit="1"
                  accept=".md,.markdown"
                >
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">Drop Markdown file here or <em>click to upload</em></div>
                </el-upload>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitMdFile" :loading="loading">Upload File</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="Paste Markdown Code" name="md-code">
            <el-form :model="mdCodeForm" label-width="120px">
              <el-form-item label="Page Title (Optional)">
                <el-input v-model="mdCodeForm.title" placeholder="Enter page title"></el-input>
              </el-form-item>
              <el-form-item label="Markdown Code">
                <el-input
                  v-model="mdCodeForm.markdown_content"
                  type="textarea"
                  :rows="10"
                  placeholder="Paste your Markdown code here"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitMdCode" :loading="loading">Submit Code</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>
    </el-tabs>

    <div v-if="uploadedPageUrl" class="result-area">
      <el-alert title="Upload Successful!" type="success" show-icon :closable="false">
        <p>Your page is ready! Share this URL:</p>
        <div class="url-display">
          <el-link :href="uploadedPageUrl" target="_blank" type="primary">{{ uploadedPageUrl }}</el-link>
          <el-button @click="copyUrl" :icon="DocumentCopy" circle></el-button>
        </div>
      </el-alert>
    </div>
     <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon class="result-area" @close="errorMessage = ''"></el-alert>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { UploadFilled, DocumentCopy } from '@element-plus/icons-vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

// Tab management
const uploadMode = ref('html');
const activeHtmlTab = ref('html-file');
const activeMarkdownTab = ref('md-file');

// Form models
const htmlFileForm = ref({ title: '', file: null });
const htmlCodeForm = ref({ title: '', html_content: '' });
const mdFileForm = ref({ title: '', file: null });
const mdCodeForm = ref({ title: '', markdown_content: '' });

// State management
const loading = ref(false);
const errorMessage = ref('');
const uploadedPageUrl = ref('');

// --- File Handlers ---
const handleHtmlFileChange = (file) => { htmlFileForm.value.file = file.raw; };
const handleMdFileChange = (file) => { mdFileForm.value.file = file.raw; };

// --- Submission Logic ---
const resetState = () => {
  loading.value = true;
  errorMessage.value = '';
  uploadedPageUrl.value = '';
};

const handleSuccess = (response) => {
  uploadedPageUrl.value = new URL(response.data.url, window.location.origin).href;
  ElMessage.success('Upload successful!');
};

const handleError = (error, defaultMessage) => {
  errorMessage.value = error.response?.data?.detail || defaultMessage;
  ElMessage.error('Upload failed!');
};

// HTML File Submission
const submitHtmlFile = async () => {
  if (!htmlFileForm.value.file) return ElMessage.warning('Please select an HTML file.');
  resetState();
  const formData = new FormData();
  formData.append('file', htmlFileForm.value.file);
  if (htmlFileForm.value.title) formData.append('title', htmlFileForm.value.title);

  try {
    const response = await axios.post('/api/upload/html', formData, { headers: authStore.getAuthHeader() });
    handleSuccess(response);
  } catch (error) {
    handleError(error, 'Failed to upload HTML file.');
  } finally {
    loading.value = false;
  }
};

// HTML Code Submission
const submitHtmlCode = async () => {
  if (!htmlCodeForm.value.html_content) return ElMessage.warning('Please paste HTML code.');
  resetState();
  try {
    const response = await axios.post('/api/upload/code', htmlCodeForm.value, { headers: authStore.getAuthHeader() });
    handleSuccess(response);
    // Clear form fields
    htmlCodeForm.value.title = '';
    htmlCodeForm.value.html_content = '';
  } catch (error) {
    handleError(error, 'Failed to submit HTML code.');
  } finally {
    loading.value = false;
  }
};

// Markdown File Submission
const submitMdFile = async () => {
  if (!mdFileForm.value.file) return ElMessage.warning('Please select a Markdown file.');
  resetState();
  const formData = new FormData();
  formData.append('file', mdFileForm.value.file);
  if (mdFileForm.value.title) formData.append('title', mdFileForm.value.title);

  try {
    // The same endpoint handles HTML and MD files now
    const response = await axios.post('/api/upload/html', formData, { headers: authStore.getAuthHeader() });
    handleSuccess(response);
  } catch (error) {
    handleError(error, 'Failed to upload Markdown file.');
  } finally {
    loading.value = false;
  }
};

// Markdown Code Submission
const submitMdCode = async () => {
  if (!mdCodeForm.value.markdown_content) return ElMessage.warning('Please paste Markdown code.');
  resetState();
  try {
    const response = await axios.post('/api/upload/markdown', mdCodeForm.value, { headers: authStore.getAuthHeader() });
    handleSuccess(response);
    // Clear form fields
    mdCodeForm.value.title = '';
    mdCodeForm.value.markdown_content = '';
  } catch (error) {
    handleError(error, 'Failed to submit Markdown code.');
  } finally {
    loading.value = false;
  }
};

// URL Copy
const copyUrl = async () => {
  if (!uploadedPageUrl.value) return;
  try {
    await navigator.clipboard.writeText(uploadedPageUrl.value);
    ElMessage.success('URL copied to clipboard!');
  } catch (err) {
    ElMessage.error('Failed to copy URL.');
  }
};
</script>

<style scoped>
.main-tabs > .el-tabs__content {
  padding: 20px;
}
.result-area {
  margin-top: 20px;
}
.url-display {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}
</style>