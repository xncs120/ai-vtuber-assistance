<template>
  <div class="flex h-screen overflow-hidden">
    <PushDrawer :isDrawerOpen="isDrawerOpen">
      <template #menuTemplate>
        <ChatRoom v-model:isDrawerOpen="isDrawerOpen" />
      </template>

      <template #contentTemplate>
        <div class="p-4">
          <button
            @click="toggleScreenCapture"
            v-if="!isDrawerOpen"
            class="btn btn-primary w-10 rounded-full fixed bottom-16 left-4 z-50"
          >
            <i class="fa fa-desktop"></i>
          </button>

          <button
            @click="isDrawerOpen = true"
            v-if="!isDrawerOpen"
            class="btn btn-primary w-10 rounded-full fixed bottom-4 left-4 z-50"
          >
            <i class="fa fa-comment"></i>
          </button>

          <Live2DViewer :isStreamOn="isStreamOn" />
        </div>
      </template>
    </PushDrawer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PushDrawer from './components/customs/PushDrawer.vue'
import ChatRoom from './components/ChatRoom.vue'
import Live2DViewer from './components/Live2DViewer.vue'

const isDrawerOpen = ref(false)
const isStreamOn = ref(false)

const toggleScreenCapture = () => {
  if (isStreamOn.value) {
    console.log(111)
    isStreamOn.value = false
  } else {
    console.log(221)
    isStreamOn.value = true
  }
}
</script>

