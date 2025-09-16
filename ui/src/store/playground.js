import {
  getPlaygroundAgentsAPI,
  sendPlaygroundAgentMessageAPI,
  getPlaygroundSessionsAPI,
  getPlaygroundSessionAPI,
} from '../apis/playground'

export default {
  namespaced: true,

  state: () => ({
    agents: [],
    selectedAgent: '',
    sessions: [],
    selectedSession: '',
    messages: [],
    inResponse: false,
  }),

  mutations: {
    setAgents(state, agents) {
      state.agents = agents
    },
    setSelectedAgent(state, agentId) {
      state.selectedAgent = agentId
    },
    setSessions(state, sessions) {
      state.sessions = sessions
    },
    setSelectedSession(state, sessionId) {
      state.selectedSession = sessionId
    },
    setMessages(state, messages) {
      state.messages = messages
    },
    addMessage(state, message) {
      state.messages.push(message)
    },
    updateLastMessage(state, chunk) {
      const last = state.messages[state.messages.length - 1]
      if (last?.content) {
        if (last.content === '...') {
          last.content = chunk
        } else {
          last.content += chunk
        }
      }
    },
    changeInResponse(state, inResponse) {
      state.inResponse = inResponse
    },
  },

  actions: {
    async fetchAgents({ commit }) {
      const results = await getPlaygroundAgentsAPI()
      commit('setAgents', results)
    },
    async fetchSessions({ commit }, agentId) {
      const results = await getPlaygroundSessionsAPI(agentId)
      commit('setSessions', results)
    },
    async fetchMessages({ commit }, sessionId) {
      const results = await getPlaygroundSessionAPI(sessionId)
      commit('setMessages', results ?? [])
    },
    async sendMessage({ commit }, { agentId, sessionId, message }) {
      commit('changeInResponse', true)
      commit('addMessage', { role: 'user', content: message })
      commit('addMessage', { role: 'assistant', content: '...' })

      const response = await sendPlaygroundAgentMessageAPI(agentId, sessionId, message, (data) => {
        commit('updateLastMessage', data.content)
      })

      if (response) {
        commit('changeInResponse', false)
      }

      if (sessionId === '') {
        const results = await getPlaygroundSessionsAPI(agentId)
        commit('setSessions', results)
        commit('setSelectedSession', results[0]?.session_id ?? '')
      }
    },
  },

  getters: {
    getAgents: (state) => state.agents,
    getSelectedAgent: (state) => state.selectedAgent,
    getSessions: (state) => state.sessions,
    getSelectedSession: (state) => state.selectedSession,
    getMessages: (state) => state.messages,
  },
}
