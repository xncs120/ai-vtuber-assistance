<template>
  <transition name="slide">
    <div
      v-if="isDrawerOpen"
      class="fixed w-100 bg-base-100 border-r border-base-300 flex flex-col h-full transition-all duration-300"
    >
      <slot name="menuTemplate"></slot>
    </div>
  </transition>

  <slot name="contentTemplate"></slot>
  <!-- <div :class="['flex-1 transition-all duration-300', isDrawerOpen ? 'ml-100' : 'ml-0']">
    <slot name="contentTemplate"></slot>
  </div> -->
</template>

<script setup>
const props = defineProps({
  isDrawerOpen: Boolean,
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
</style>