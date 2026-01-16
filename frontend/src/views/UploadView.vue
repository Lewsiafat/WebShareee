<template>
  <div class="upload-container">
    <div class="upload-header">
      <h1>New Deployment</h1>
      <p>Choose your preferred method to publish your content.</p>
    </div>

    <div class="glass-panel upload-panel">
      <el-tabs v-model="uploadMode" class="custom-tabs">
        <!-- HTML Uploader -->
        <el-tab-pane name="html">
          <template #label>
            <span class="tab-label">
              <el-icon><Document /></el-icon>
              <span>HTML Page</span>
            </span>
          </template>
          
          <div class="tab-content">
            <el-radio-group v-model="activeHtmlTab" class="sub-tabs">
              <el-radio-button label="html-file">Upload File</el-radio-button>
              <el-radio-button label="html-code">Paste Code</el-radio-button>
            </el-radio-group>

            <!-- File Upload -->
            <transition name="fade" mode="out-in">
              <div v-if="activeHtmlTab === 'html-file'" key="file" class="upload-section">
                <el-form :model="htmlFileForm" label-position="top">
                  <el-form-item label="Page Title (Optional)">
                    <el-input v-model="htmlFileForm.title" placeholder="My Awesome Page" />
                  </el-form-item>
                  
                  <el-form-item>
                    <el-upload
                      class="upload-area"
                      drag
                      :auto-upload="false"
                      :on-change="handleHtmlFileChange"
                      :limit="1"
                      accept=".html"
                      :show-file-list="true"
                    >
                      <el-icon class="upload-icon"><upload-filled /></el-icon>
                      <div class="el-upload__text">
                        Drop HTML file here or <em>click to browse</em>
                      </div>
                    </el-upload>
                  </el-form-item>
                  
                  <el-button type="primary" size="large" @click="submitHtmlFile" :loading="loading" class="action-btn">
                    Deploy HTML File
                  </el-button>
                </el-form>
              </div>

              <!-- Code Paste -->
              <div v-else key="code" class="upload-section">
                <el-form :model="htmlCodeForm" label-position="top">
                  <el-form-item label="Page Title (Optional)">
                     <el-input v-model="htmlCodeForm.title" placeholder="My Awesome Page" />
                  </el-form-item>
                  
                  <el-form-item label="HTML Code">
                    <el-input
                      v-model="htmlCodeForm.html_content"
                      type="textarea"
                      :rows="12"
                      placeholder="<!DOCTYPE html>..."
                      class="code-editor"
                    />
                  </el-form-item>
                  
                  <el-button type="primary" size="large" @click="submitHtmlCode" :loading="loading" class="action-btn">
                     Deploy HTML Code
                  </el-button>
                </el-form>
              </div>
            </transition>
          </div>
        </el-tab-pane>

        <!-- Markdown Uploader -->
        <el-tab-pane name="markdown">
          <template #label>
             <span class="tab-label">
              <el-icon><EditPen /></el-icon>
              <span>Markdown</span>
            </span>
          </template>
          
           <div class="tab-content">
            <el-radio-group v-model="activeMarkdownTab" class="sub-tabs">
              <el-radio-button label="md-file">Upload File</el-radio-button>
              <el-radio-button label="md-code">Paste Code</el-radio-button>
            </el-radio-group>

             <transition name="fade" mode="out-in">
              <div v-if="activeMarkdownTab === 'md-file'" key="md-file" class="upload-section">
                <el-form :model="mdFileForm" label-position="top">
                  <el-form-item label="Page Title (Optional)">
                    <el-input v-model="mdFileForm.title" placeholder="My Markdown Page" />
                  </el-form-item>
                   <el-form-item>
                    <el-upload
                      class="upload-area"
                      drag
                      :auto-upload="false"
                      :on-change="handleMdFileChange"
                      :limit="1"
                      accept=".md,.markdown"
                      :show-file-list="true"
                    >
                      <el-icon class="upload-icon"><upload-filled /></el-icon>
                      <div class="el-upload__text">
                        Drop Markdown file here or <em>click to browse</em>
                      </div>
                    </el-upload>
                  </el-form-item>
                   <el-button type="primary" size="large" @click="submitMdFile" :loading="loading" class="action-btn">
                    Deploy Markdown File
                  </el-button>
                </el-form>
              </div>

               <div v-else key="md-code" class="upload-section">
                  <el-form :model="mdCodeForm" label-position="top">
                  <el-form-item label="Page Title (Optional)">
                     <el-input v-model="mdCodeForm.title" placeholder="My Markdown Page" />
                  </el-form-item>
                  
                  <el-form-item label="Markdown Code">
                    <el-input
                      v-model="mdCodeForm.markdown_content"
                      type="textarea"
                      :rows="12"
                      placeholder="# Hello World"
                      class="code-editor"
                    />
                  </el-form-item>
                  
                  <el-button type="primary" size="large" @click="submitMdCode" :loading="loading" class="action-btn">
                     Deploy Markdown Code
                  </el-button>
                </el-form>
               </div>
             </transition>
           </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- Success Result -->
    <transition name="el-zoom-in-top">
      <div v-if="uploadedPageUrl" class="result-card glass-panel success">
        <div class="result-header">
           <el-icon class="success-icon"><CircleCheckFilled /></el-icon>
           <h3>Deployment Successful!</h3>
        </div>
        <p>Your page is receiving traffic at:</p>
        <div class="url-copy-box">
          <a :href="uploadedPageUrl" target="_blank" class="url-link">{{ uploadedPageUrl }}</a>
          <el-button @click="copyUrl" :icon="DocumentCopy" circle type="primary" plain></el-button>
        </div>
      </div>
    </transition>

     <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      class="mt-4"
      @close="errorMessage = ''"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
import { UploadFilled, DocumentCopy, Document, EditPen, CircleCheckFilled } from "@element-plus/icons-vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

// Tab management
const uploadMode = ref("html");
const activeHtmlTab = ref("html-file");
const activeMarkdownTab = ref("md-file");

// Form models
const htmlFileForm = ref({ title: "", file: null });
const htmlCodeForm = ref({ title: "", html_content: "" });
const mdFileForm = ref({ title: "", file: null });
const mdCodeForm = ref({ title: "", markdown_content: "" });

// State management
const loading = ref(false);
const errorMessage = ref("");
const uploadedPageUrl = ref("");

// --- File Handlers ---
const handleHtmlFileChange = (file) => {
  htmlFileForm.value.file = file.raw;
};
const handleMdFileChange = (file) => {
  mdFileForm.value.file = file.raw;
};

// --- Submission Logic ---
const resetState = () => {
  loading.value = true;
  errorMessage.value = "";
  uploadedPageUrl.value = "";
};

const handleSuccess = (response) => {
  uploadedPageUrl.value = new URL(
    response.data.url,
    window.location.origin,
  ).href;
  ElMessage.success("Upload successful!");
};

const handleError = (error, defaultMessage) => {
  errorMessage.value = error.response?.data?.detail || defaultMessage;
  ElMessage.error("Upload failed!");
};

// HTML File Submission
const submitHtmlFile = async () => {
  if (!htmlFileForm.value.file)
    return ElMessage.warning("Please select an HTML file.");
  resetState();
  const formData = new FormData();
  formData.append("file", htmlFileForm.value.file);
  if (htmlFileForm.value.title)
    formData.append("title", htmlFileForm.value.title);

  try {
    const response = await axios.post("/api/upload/html", formData, {
      headers: authStore.getAuthHeader(),
    });
    handleSuccess(response);
  } catch (error) {
    handleError(error, "Failed to upload HTML file.");
  } finally {
    loading.value = false;
  }
};

// HTML Code Submission
const submitHtmlCode = async () => {
  if (!htmlCodeForm.value.html_content)
    return ElMessage.warning("Please paste HTML code.");
  resetState();
  try {
    const response = await axios.post("/api/upload/code", htmlCodeForm.value, {
      headers: authStore.getAuthHeader(),
    });
    handleSuccess(response);
    htmlCodeForm.value.title = "";
    htmlCodeForm.value.html_content = "";
  } catch (error) {
    handleError(error, "Failed to submit HTML code.");
  } finally {
    loading.value = false;
  }
};

// Markdown File Submission
const submitMdFile = async () => {
  if (!mdFileForm.value.file)
    return ElMessage.warning("Please select a Markdown file.");
  resetState();
  const formData = new FormData();
  formData.append("file", mdFileForm.value.file);
  if (mdFileForm.value.title) formData.append("title", mdFileForm.value.title);

  try {
    const response = await axios.post("/api/upload/html", formData, {
      headers: authStore.getAuthHeader(),
    });
    handleSuccess(response);
  } catch (error) {
    handleError(error, "Failed to upload Markdown file.");
  } finally {
    loading.value = false;
  }
};

// Markdown Code Submission
const submitMdCode = async () => {
  if (!mdCodeForm.value.markdown_content)
    return ElMessage.warning("Please paste Markdown code.");
  resetState();
  try {
    const response = await axios.post(
      "/api/upload/markdown",
      mdCodeForm.value,
      { headers: authStore.getAuthHeader() },
    );
    handleSuccess(response);
    mdCodeForm.value.title = "";
    mdCodeForm.value.markdown_content = "";
  } catch (error) {
    handleError(error, "Failed to submit Markdown code.");
  } finally {
    loading.value = false;
  }
};

const copyUrl = async () => {
  if (!uploadedPageUrl.value) return;
  try {
    await navigator.clipboard.writeText(uploadedPageUrl.value);
    ElMessage.success("URL copied to clipboard!");
  } catch (err) {
    ElMessage.error("Failed to copy URL.");
  }
};
</script>

<style scoped>
.upload-container {
  max-width: 100%;
  padding: 0 20px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.upload-header {
  margin-bottom: 20px;
  text-align: center;
  flex-shrink: 0;
}

.upload-header h1 {
  font-size: 2rem;
  margin-bottom: 8px;
}

.upload-header p {
  color: var(--text-secondary);
}

.upload-panel {
  padding: 0;
  overflow: hidden;
  border-radius: 16px;
  background: var(--el-bg-color);
  flex: 1;
  display: flex;
  flex-direction: column;
}

.custom-tabs {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.custom-tabs :deep(.el-tabs__content) {
  flex: 1;
  overflow-y: auto;
}

.custom-tabs :deep(.el-tabs__header) {
  margin: 0;
  background: rgba(0,0,0,0.02);
  border-bottom: 1px solid var(--border-light);
  flex-shrink: 0;
}

.custom-tabs :deep(.el-tabs__item) {
  height: 60px;
  font-size: 16px;
  font-weight: 500;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-content {
  padding: 30px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.sub-tabs {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.upload-section {
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  height: 200px;
  border: 2px dashed var(--border-light);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--el-bg-color-page);
  transition: all 0.3s ease;
}

.upload-area :deep(.el-upload-dragger:hover) {
  border-color: var(--brand-primary);
  background-color: rgba(79, 70, 229, 0.02);
}

.upload-icon {
  font-size: 48px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  transition: color 0.3s;
}

.upload-area:hover .upload-icon {
  color: var(--brand-primary);
}

.action-btn {
  width: 100%;
  margin-top: 10px;
  height: 48px;
  font-size: 16px;
}

.result-card {
  margin-top: 30px;
  padding: 24px;
  border-radius: 16px;
  text-align: center;
  border: 1px solid #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.success-icon {
  font-size: 32px;
  color: #10b981;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.result-header h3 {
  margin: 0;
  color: #065f46;
}

.url-copy-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: var(--el-bg-color);
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid var(--border-light);
  margin-top: 16px;
}

.url-link {
  color: var(--brand-primary);
  font-weight: 500;
  text-decoration: none;
}

.mt-4 {
  margin-top: 20px;
}
</style>
