<template>
  <div class="account-view">
    <h1>帳號設定</h1>
    
    <el-row :gutter="20">
      <!-- Change Username Card -->
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>修改使用者名稱</span>
            </div>
          </template>
          <el-form
            ref="usernameFormRef"
            :model="usernameForm"
            :rules="usernameRules"
            label-width="120px"
            @submit.prevent="handleChangeUsername"
          >
            <el-form-item label="新的使用者名稱" prop="newUsername">
              <el-input v-model="usernameForm.newUsername"></el-input>
            </el-form-item>
            <el-form-item label="目前密碼" prop="password">
              <el-input v-model="usernameForm.password" type="password" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangeUsername">更新使用者名稱</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Change Password Card -->
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>修改密碼</span>
            </div>
          </template>
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="120px"
            @submit.prevent="handleChangePassword"
          >
            <el-form-item label="目前密碼" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" show-password></el-input>
            </el-form-item>
            <el-form-item label="新密碼" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" show-password></el-input>
            </el-form-item>
            <el-form-item label="確認新密碼" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword">更新密碼</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElNotification } from 'element-plus';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

// --- Username Change Logic ---
const usernameFormRef = ref(null);
const usernameForm = reactive({
  newUsername: '',
  password: '',
});

const usernameRules = reactive({
  newUsername: [{ required: true, message: '請輸入新的使用者名稱', trigger: 'blur' }],
  password: [{ required: true, message: '請輸入目前密碼以進行驗證', trigger: 'blur' }],
});

const handleChangeUsername = async () => {
  if (!usernameFormRef.value) return;
  await usernameFormRef.value.validate(async (valid) => {
    if (valid) {
      const success = await authStore.changeUsername(
        usernameForm.newUsername,
        usernameForm.password
      );
      if (success) {
        ElNotification({
          title: '成功',
          message: '使用者名稱已成功更新！',
          type: 'success',
        });
        usernameForm.newUsername = '';
        usernameForm.password = '';
      } else {
        ElNotification({
          title: '錯誤',
          message: authStore.error || '更新使用者名稱失敗。',
          type: 'error',
        });
      }
    }
  });
};

// --- Password Change Logic ---
const passwordFormRef = ref(null);
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
});

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('請再次輸入新密碼'));
  } else if (value !== passwordForm.newPassword) {
    callback(new Error("兩次輸入的密碼不一致"));
  } else {
    callback();
  }
};

const passwordRules = reactive({
  oldPassword: [{ required: true, message: '請輸入目前密碼', trigger: 'blur' }],
  newPassword: [{ required: true, message: '請輸入新密碼', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '請再次輸入新密碼', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' },
  ],
});

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return;
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      const success = await authStore.changePassword(
        passwordForm.oldPassword,
        passwordForm.newPassword
      );
      if (success) {
        ElNotification({
          title: '成功',
          message: '密碼已成功更新！',
          type: 'success',
        });
        passwordForm.oldPassword = '';
        passwordForm.newPassword = '';
        passwordForm.confirmPassword = '';
      } else {
        ElNotification({
          title: '錯誤',
          message: authStore.error || '更新密碼失敗。',
          type: 'error',
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
