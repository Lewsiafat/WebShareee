<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="badge">Static Web Hosting</div>
        <h1 class="hero-title">
          Share your web creations <br/>
          <span class="gradient-text">instantly & securely</span>
        </h1>
        <p class="hero-description">
          The simplest way to host static HTML pages. Drag, drop, and get a shareable link in seconds. No complex setup required.
        </p>
        <div class="cta-group">
          <el-button type="primary" size="large" @click="$router.push('/upload')" class="cta-btn primary">
            Start Uploading
            <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
          <el-button size="large" @click="$router.push('/login')" class="cta-btn secondary">
            Admin Login
          </el-button>
        </div>
      </div>
      
      <div class="hero-visual glass-panel">
         <!-- Abstract decoration or preview placeholder -->
         <div class="code-preview">
           <div class="window-controls">
             <span class="dot red"></span>
             <span class="dot yellow"></span>
             <span class="dot green"></span>
           </div>
           <div class="code-content">
             <div class="line"><span class="tag">&lt;html&gt;</span></div>
             <div class="line indent"><span class="tag">&lt;body&gt;</span></div>
             <div class="line indent-2"><span class="tag">&lt;h1&gt;</span>Hello World<span class="tag">&lt;/h1&gt;</span></div>
             <div class="line indent"><span class="tag">&lt;/body&gt;</span></div>
             <div class="line"><span class="tag">&lt;/html&gt;</span></div>
           </div>
         </div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="features-section">
      <div class="feature-card glass-panel">
        <div class="feature-icon-wrapper blue">
          <el-icon><Upload /></el-icon>
        </div>
        <h3>Instant Upload</h3>
        <p>Drag and drop your HTML files or paste code directly. Your page is live in milliseconds.</p>
      </div>

      <div class="feature-card glass-panel">
        <div class="feature-icon-wrapper purple">
          <el-icon><Link /></el-icon>
        </div>
        <h3>Short Links</h3>
        <p>Get a clean, short URL for every page you upload. Perfect for sharing on social media.</p>
      </div>

      <div class="feature-card glass-panel">
        <div class="feature-icon-wrapper green">
          <el-icon><Lock /></el-icon>
        </div>
        <h3>Secure Hosting</h3>
        <p>Your content is served securely. Manage your uploads with a simple admin interface.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ArrowRight, Upload, Link, Lock } from "@element-plus/icons-vue";
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  min-height: 500px;
  margin-bottom: 80px;
}

.badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(79, 70, 229, 0.1);
  color: var(--brand-primary);
  border-radius: 30px;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 24px;
}

.hero-title {
  font-size: 3.5rem;
  line-height: 1.1;
  margin-bottom: 24px;
  font-weight: 800;
}

.gradient-text {
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 40px;
  max-width: 500px;
}

.cta-group {
  display: flex;
  gap: 16px;
}

.cta-btn {
  padding: 12px 28px;
  height: auto;
  font-size: 1rem;
}

/* Hero Visual */
.hero-visual {
  padding: 30px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.4);
  transform: perspective(1000px) rotateY(-5deg) rotateX(5deg);
  transition: transform 0.3s ease;
}

.hero-visual:hover {
  transform: perspective(1000px) rotateY(0) rotateX(0);
}

.code-preview {
  background: #1e293b;
  border-radius: 12px;
  padding: 20px;
  font-family: 'Fira Code', monospace;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.window-controls {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ef4444; }
.dot.yellow { background: #f59e0b; }
.dot.green { background: #22c55e; }

.code-content {
  color: #e2e8f0;
  font-size: 14px;
  line-height: 1.6;
}

.tag { color: #f472b6; }
.indent { padding-left: 20px; }
.indent-2 { padding-left: 40px; }

/* Features Grid */
.features-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.feature-card {
  padding: 32px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-bottom: 24px;
}

.feature-icon-wrapper.blue { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.feature-icon-wrapper.purple { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
.feature-icon-wrapper.green { background: rgba(16, 185, 129, 0.1); color: #10b981; }

.feature-card h3 {
  font-size: 1.25rem;
  margin-bottom: 12px;
  color: var(--text-main);
}

.feature-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* Responsive */
@media (max-width: 900px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-description {
    margin-left: auto;
    margin-right: auto;
  }

  .cta-group {
    justify-content: center;
  }
  
  .hero-visual {
    display: none;
  }
  
  .features-section {
    grid-template-columns: 1fr;
  }
}
</style>
