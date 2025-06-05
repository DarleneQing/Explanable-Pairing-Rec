<template>
    <div class="blob-container">
      <img src="@/assets/blobs/blob-1.svg" alt="Blob 1" class="blob" />
      <img src="@/assets/blobs/blob-2.svg" alt="Blob 2" class="blob" />
      <img src="@/assets/blobs/blob-3.svg" alt="Blob 3" class="blob" />
      <img src="@/assets/blobs/blob-4.svg" alt="Blob 4" class="blob" />
      <img src="@/assets/blobs/blob-5.svg" alt="Blob 5" class="blob" />
    </div>
  </template>
  
  <script setup>
  // Component logic can be added here if needed
  </script>
  
  <style scoped>
  .blob-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.8rem;
    padding: 0.7rem;
    background-color: none;
  }
  
  .blob {
    width: 40px;
    height: auto;
    transition: transform 0.3s ease;
  }
  
  .blob:hover {
    transform: scale(1.1);
  }
  </style> 