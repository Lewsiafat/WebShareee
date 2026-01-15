<template>
  <div class="account-container">
    <div class="view-header">
       <h1>Account Settings</h1>
    </div>

    <div class="settings-grid">
      <!-- Change Username Card -->
      <div class="glass-panel settings-card">
        <div class="card-header">
          <div class="icon-box purple">
             <el-icon><User /></el-icon>
          </div>
          <h3>Change Username</h3>
        </div>
        
        <el-form
          ref="usernameFormRef"
          :model="usernameForm"
          :rules="usernameRules"
          label-position="top"
          @submit.prevent="handleChangeUsername"
        >
          <el-form-item label="New Username" prop="newUsername">
            <el-input
              v-model="usernameForm.newUsername"
              placeholder="Enter new username"
              :prefix-icon="User"
            />
          </el-form-item>
          <el-form-item label="Current Password" prop="password">
            <el-input
              v-model="usernameForm.password"
              type="password"
              show-password
              placeholder="Verify with password"
              :prefix-icon="Lock"
            />
          </el-form-item>
          <el-button type="primary" class="full-width" @click="handleChangeUsername">
            Update Username
          </el-button>
        </el-form>
      </div>

      <!-- Change Password Card -->
      <div class="glass-panel settings-card">
         <div class="card-header">
          <div class="icon-box blue">
             <el-icon><Key /></el-icon>
          </div>
          <h3>Change Password</h3>
        </div>

        <el-form
          ref="passwordFormRef"
          :model="passwordForm"
          :rules="passwordRules"
          label-position="top"
          @submit.prevent="handleChangePassword"
        >
          <el-form-item label="Old Password" prop="oldPassword">
            <el-input
              v-model="passwordForm.oldPassword"
              type="password"
              show-password
              placeholder="Current password"
              :prefix-icon="Lock"
            />
          </el-form-item>
          <el-form-item label="New Password" prop="newPassword">
            <el-input
              v-model="passwordForm.newPassword"
              type="password"
              show-password
              placeholder="New password"
              :prefix-icon="Key"
            />
          </el-form-item>
          <el-form-item label="Confirm New Password" prop="confirmPassword">
            <el-input
              v-model="passwordForm.confirmPassword"
              type="password"
              show-password
              placeholder="Confirm new password"
              :prefix-icon="Key"
            />
          </el-form-item>
          <el-button type="primary" class="full-width" @click="handleChangePassword">
            Update Password
          </el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { ElNotification } from "element-plus";
import { User, Lock, Key } from "@element-plus/icons-vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

// --- Username Change Logic ---
const usernameFormRef = ref(null);
const usernameForm = reactive({
  newUsername: "",
  password: "",
});

const usernameRules = reactive({
  newUsername: [
    { required: true, message: "Please enter the new username", trigger: "blur" },
  ],
  password: [
    { required: true, message: "Please enter your current password", trigger: "blur" },
  ],
});

const handleChangeUsername = async () => {
  if (!usernameFormRef.value) return;
  await usernameFormRef.value.validate(async (valid) => {
    if (valid) {
      const success = await authStore.changeUsername(
        usernameForm.newUsername,
        usernameForm.password,
      );
      if (success) {
        ElNotification({
          title: "Success",
          message: "Username updated successfully!",
          type: "success",
        });
        usernameForm.newUsername = "";
        usernameForm.password = "";
      } else {
        ElNotification({
          title: "Error",
          message: authStore.error || "Failed to update username.",
          type: "error",
        });
      }
    }
  });
};

// --- Password Change Logic ---
const passwordFormRef = ref(null);
const passwordForm = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const validatePass = (rule, value, callback) => {
  if (value === "") {
    callback(new Error("Please enter the new password again"));
  } else if (value !== passwordForm.newPassword) {
    callback(new Error("The two passwords don't match"));
  } else {
    callback();
  }
};

const passwordRules = reactive({
  oldPassword: [
    { required: true, message: "Please enter your current password", trigger: "blur" },
  ],
  newPassword: [
    { required: true, message: "Please enter the new password", trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: "Please enter the new password again", trigger: "blur" },
    { validator: validatePass, trigger: "blur" },
  ],
});

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return;
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      const success = await authStore.changePassword(
        passwordForm.oldPassword,
        passwordForm.newPassword,
      );
      if (success) {
        ElNotification({
          title: "Success",
          message: "Password updated successfully!",
          type: "success",
        });
        passwordForm.oldPassword = "";
        passwordForm.newPassword = "";
        passwordForm.confirmPassword = "";
      } else {
        ElNotification({
          title: "Error",
          message: authStore.error || "Failed to update password.",
          type: "error",
        });
      }
    }
  });
};
</script>

<style scoped>
.account-container {
  max-width: 1000px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: 30px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.settings-card {
  padding: 32px;
  border-radius: 20px;
  background: var(--el-bg-color);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.icon-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.icon-box.purple { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
.icon-box.blue { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.full-width {
  width: 100%;
  margin-top: 10px;
}
</style>
