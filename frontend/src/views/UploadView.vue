<template>
  <div class="page-container">
    <h1>Upload Your Web Page</h1>

    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="Upload HTML File" name="file">
        <el-form :model="fileForm" label-width="120px">
          <el-form-item label="Page Title (Optional)">
            <el-input v-model="fileForm.title" placeholder="Enter page title"></el-input>
          </el-form-item>
          <el-form-item label="HTML File">
            <el-upload
              class="upload-demo"
              drag
              :auto-upload="false"
              :on-change="handleFileChange"
              :limit="1"
              accept=".html"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                Drop HTML file here or <em>click to upload</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  HTML files only, max 10MB.
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitHtmlFile" :loading="loading">Upload File</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="Paste HTML Code" name="code">
        <el-form :model="codeForm" label-width="120px">
          <el-form-item label="Page Title (Optional)">
            <el-input v-model="codeForm.title" placeholder="Enter page title"></el-input>
          </el-form-item>
          <el-form-item label="HTML Code">
            <el-input
              v-model="codeForm.html_content"
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

    <el-alert v-if="successMessage" :title="successMessage" type="success" show-icon class="mt-4"></el-alert>
    <el-alert v-if="errorMessage" :title="errorMessage" type="error" show-icon class="mt-4"></el-alert>

    <div v-if="uploadedPageUrl" class="mt-4">
      <p>Your page is ready! Share this URL:</p>
      <el-link :href="uploadedPageUrl" target="_blank" type="primary">{{ uploadedPageUrl }}</el-link>
      <el-button type="text" @click="copyUrl" icon="el-icon-copy-document">Copy URL</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { UploadFilled } from '@element-plus/icons-vue'; // Import the icon

const activeTab = ref('file');
const fileForm = ref({
  title: '',
  file: null,
});
const codeForm = ref({
  title: '',
  html_content: '',
});

const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');
const uploadedPageUrl = ref('');

const handleFileChange = (file) => {
  fileForm.value.file = file.raw;
};

const submitHtmlFile = async () => {
  if (!fileForm.value.file) {
    ElMessage.warning('Please select an HTML file to upload.');
    return;
  }

  loading.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  uploadedPageUrl.value = '';

  const formData = new FormData();
  formData.append('file', fileForm.value.file);
  if (fileForm.value.title) {
    formData.append('title', fileForm.value.title);
  }

  try {
    const response = await axios.post('/api/upload/html', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        // Add Authorization header if user is logged in
        // 'Authorization': `Basic ${btoa(`${username}:${password}`)}`
      },
    });
    successMessage.value = 'HTML file uploaded successfully!';
    uploadedPageUrl.value = response.data.url;
    ElMessage.success('Upload successful!');
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to upload HTML file.';
    ElMessage.error('Upload failed!');
  } finally {
    loading.value = false;
  }
};

const submitHtmlCode = async () => {
  if (!codeForm.value.html_content) {
    ElMessage.warning('Please paste HTML code.');
    return;
  }

  loading.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  uploadedPageUrl.value = '';

  try {
    const response = await axios.post('/api/upload/code', codeForm.value, {
      headers: {
        'Content-Type': 'application/json',
        // Add Authorization header if user is logged in
        // 'Authorization': `Basic ${btoa(`${username}:${password}`)}`
      },
    });
    successMessage.value = 'HTML code submitted successfully!';
    uploadedPageUrl.value = response.data.url;
    ElMessage.success('Submission successful!');
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to submit HTML code.';
    ElMessage.error('Submission failed!');
  } finally {
    loading.value = false;
  }
};

const copyUrl = async () => {
  try {
    await navigator.clipboard.writeText(uploadedPageUrl.value);
    ElMessage.success('URL copied to clipboard!');
  } catch (err) {
    ElMessage.error('Failed to copy URL.');
  }
};
</script>

<style scoped>
/* No scoped styles needed here, using global .page-container */
</style>
