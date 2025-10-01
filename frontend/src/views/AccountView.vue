<template>
  <div class="account-view">
    <h1>Account Settings</h1>

    <el-row :gutter="20">
      <!-- Change Username Card -->
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>Change Username</span>
            </div>
          </template>
          <el-form
            ref="usernameFormRef"
            :model="usernameForm"
            :rules="usernameRules"
            label-width="150px"
            @submit.prevent="handleChangeUsername"
          >
            <el-form-item label="New Username" prop="newUsername">
              <el-input
                v-model="usernameForm.newUsername"
                placeholder="Enter new username"
              ></el-input>
            </el-form-item>
            <el-form-item label="Current Password" prop="password">
              <el-input
                v-model="usernameForm.password"
                type="password"
                show-password
                placeholder="Enter current password"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangeUsername"
                >Update Username</el-button
              >
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Change Password Card -->
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>Change Password</span>
            </div>
          </template>
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="150px"
            @submit.prevent="handleChangePassword"
          >
            <el-form-item label="Old Password" prop="oldPassword">
              <el-input
                v-model="passwordForm.oldPassword"
                type="password"
                show-password
                placeholder="Enter old password"
              ></el-input>
            </el-form-item>
            <el-form-item label="New Password" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                show-password
                placeholder="Enter new password"
              ></el-input>
            </el-form-item>
            <el-form-item label="Confirm New Password" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                show-password
                placeholder="Enter new password again"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword"
                >Update Password</el-button
              >
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { ElNotification } from "element-plus";
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
    {
      required: true,
      message: "Please enter the new username",
      trigger: "blur",
    },
  ],
  password: [
    {
      required: true,
      message: "Please enter your current password for verification",
      trigger: "blur",
    },
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
    {
      required: true,
      message: "Please enter your current password",
      trigger: "blur",
    },
  ],
  newPassword: [
    {
      required: true,
      message: "Please enter the new password",
      trigger: "blur",
    },
  ],
  confirmPassword: [
    {
      required: true,
      message: "Please enter the new password again",
      trigger: "blur",
    },
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
.account-view {
  padding: 20px;
}
.box-card {
  height: 100%;
}
</style>
