<template>
  <div class="p-4 border-b border-base-300 flex justify-between items-center">
    <div class="flex items-center gap-2">
      <h2 class="text-lg font-semibold">Chat</h2>
      <span
        class="w-2 h-2 rounded-full"
        :class="playgroundStatus === 'ok' ? 'bg-green-500' : 'bg-white'"
        :title="playgroundStatus === 'ok' ? 'Playground Active' : 'Playground Inactive'"
      ></span>
    </div>

    <div class="flex justify-between items-center gap-4">
      <button @click="reloadMessages" class="text-xs cursor-pointer">
        <i class="fa fa-rotate-right"></i>
      </button>

      <label class="cursor-pointer">
        <input type="checkbox" v-model="openSettings" class="checkbox hidden" />
        <i class="fa fa-sliders"></i>
      </label>

      <button @click="emit('update:isDrawerOpen', false)" class="text-xl cursor-pointer">
        <i class="fa fa-angle-double-left"></i>
      </button>
    </div>
  </div>

  <div :class="['collapse border-b border-base-300', { 'collapse-open': openSettings }]">
    <div class="collapse-content text-sm space-y-4">
      <select v-model="selectedAgent" id="agent" class="select w-full mt-4">
        <option disabled value="">Agent</option>
        <option v-for="agent in agents" :key="agent.id" :value="agent.id">
          {{ agent.id }}
        </option>
      </select>
      
      <select v-model="selectedSession" id="session" class="select w-full" :disabled="!selectedAgent">
        <option disabled value="">Session</option>
        <option v-for="session in sessions" :key="session.session_id" :value="session.session_id">
          {{ session.session_name }}
        </option>
      </select>
    </div>
  </div>

  <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
    <div v-for="(msg, index) in messages" :key="index">
      <div
        v-if="!['system', 'tool'].includes(msg?.role)"
        :class="['chat', msg?.role === 'user' ? 'chat-end' : 'chat-start']"
        :title="dayjs(msg?.created_at).format('YYYY-MM-DD HH:mm')"
      >
        <template v-if="msg?.role === 'assistant'">
          <div class="chat-image avatar">
            <div class="w-10 rounded-full">
              <img src="/models/mao/profile.png" />
            </div>
          </div>
        </template>

        <div
          :class="[
            'chat-bubble',
            msg?.role === 'user' ? 'chat-bubble-primary' : '',
            msg?.role !== 'user' && msg?.content === '...' ? 'animating-dots' : ''
          ]"
          v-html="renderMarkdown(msg?.content)"
        ></div>
      </div>
    </div>
  </div>

  <div class="p-4 border-t border-base-300">
    <div class="flex items-center gap-2">
      <button class="btn w-10 " @click="toggleMic" :disabled="inResponse || !selectedAgent">
        <i :class="['fa fa-microphone', activeMic ? 'pulse-icon' : '' ]"></i>
      </button>

      <input
        v-model="message"
        type="text"
        placeholder="Type a message…"
        class="input input-bordered w-full"
        @keyup.enter="sendMessage"
        :disabled="inResponse || !selectedAgent"
      />

      <button class="btn btn-primary w-10" @click="sendMessage" :disabled="inResponse || !selectedAgent">
        <i class="fa fa-paper-plane"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import dayjs from 'dayjs'
import { marked } from 'marked'
import { getPlaygroundStatusAPI } from '../apis/playground'

const store = useStore()
const router = useRouter()
const route = useRoute()
const queryString = window.location.search
const urlParams = new URLSearchParams(queryString)
const props = defineProps({
  isDrawerOpen: Boolean,
})

const openSettings = ref(false)
const playgroundStatus = ref(null)
const chatContainer = ref(null)
const agents = computed(() => store.state.playground.agents)
const selectedAgent = computed({
  get: () => store.state.playground.selectedAgent,
  set: (val) => store.commit('playground/setSelectedAgent', val),
})
const sessions = computed(() => store.state.playground.sessions)
const selectedSession = computed({
  get: () => store.state.playground.selectedSession,
  set: (val) => store.commit('playground/setSelectedSession', val),
})
const messages = computed({
  get: () => store.state.playground.messages,
  set: (val) => store.commit('playground/setMessages', val),
})
const message = ref('')
const inResponse = computed(() => store.state.playground.inResponse)
const activeMic = ref(false)

const emit = defineEmits(['update:isDrawerOpen'])

const fetchPlaygroundStatus = async () => {
  try {
    const result = await getPlaygroundStatusAPI()
    playgroundStatus.value = result?.status
  } catch (error) {
    playgroundStatus.value = null
  }
}

const reloadMessages = () => {
  store.dispatch('playground/fetchMessages', selectedSession.value)
}

const toggleMic = () => {
  if (activeMic.value) {
    activeMic.value = false
  } else {
    activeMic.value = true
  }
}

const renderMarkdown = (content) => {
  return content && content !== '...' ? marked.parse(content) : ''
}

const sendMessage = () => {
  let newMessage = message.value.trim()
  if (newMessage) {
    store.dispatch('playground/sendMessage', {
      agentId: selectedAgent.value,
      sessionId: selectedSession.value,
      message: newMessage,
    })
    message.value = ''
  }
}

onMounted(() => {
  fetchPlaygroundStatus()

  store.dispatch('playground/fetchAgents')

  selectedAgent.value = urlParams.get('agent') || ''

  setTimeout(() => {
      selectedSession.value = urlParams.get('session') || ''
  }, 1000)
})

watch(selectedAgent, (agentId) => {
  messages.value = []
  selectedSession.value = ''
  if (agentId) {
    router.push({ query: { ...route.query, agent: agentId } })
    store.dispatch('playground/fetchSessions', agentId)
  }
})

watch(selectedSession, (sessionId) => {
  if (sessionId) {
    router.push({ query: { ...route.query, session: sessionId } })
    store.dispatch('playground/fetchMessages', sessionId)
  }
})

watch(messages, () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}, { deep: true })
</script>

<style scoped>
.animating-dots::after {
  content: '';
  display: inline-block;
  width: 1em;
  text-align: left;
  animation: dots 1.5s steps(3, end) infinite;
}

.pulse-icon {
  animation: pulse 1.5s infinite;
}

@keyframes dots {
  0%, 20% {content: '';}
  40% {content: '.';}
  60% {content: '..';}
  80%, 100% {content: '...';}
}

@keyframes pulse {
  0% {transform: scale(1); color: white;}
  50% {transform: scale(1.3); color: red;}
  100% {transform: scale(1); color: white;}
}
</style>
