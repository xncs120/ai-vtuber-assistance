import { extractJSONObjects } from '../utils/parser'

const PLAYGROUND_URL = "http://localhost:7777"

export const getPlaygroundStatusAPI = async () => {
  const response = await fetch(`${PLAYGROUND_URL}/health`)
  return response.json()
}

export const getPlaygroundAgentsAPI = async () => {
  try {
    const response = await fetch(`${PLAYGROUND_URL}/agents`)

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    throw error
  }
}

export const sendPlaygroundAgentMessageAPI = async (agentId, sessionId, message, onMessage) => {
  const formData = new FormData()
  formData.append('message', message)
  formData.append('stream', 'true')
  if (sessionId !== '') {
    formData.append('session_id', sessionId)
  }

  const response = await fetch(`${PLAYGROUND_URL}/agents/${agentId}/runs`, {
    method: 'POST',
    headers: {
      ...(!(formData instanceof FormData) && {
        'Content-Type': 'application/json',
      }),
    },
    body: formData,
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw errorData
  }

  if (!response.body) {
    throw new Error('No response body')
  }

  // Stream response
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  let fullData = ''

  while (true) {
    const { value, done } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })

    const { objects, remaining } = extractJSONObjects(buffer);
    buffer = remaining;

    for (const data of objects) {
      if (data.event === 'RunContent' && data.content) {
        onMessage?.(data)
        fullData += data
      }
    }
  }

  return { success: true, fullData }
}

export const getPlaygroundSessionsAPI = async (agentId, type='agent') => {
  try {
    let url = `${PLAYGROUND_URL}/sessions?type=${type}&component_id=${agentId}&limit=100&page=1&sort_by=created_at&sort_order=desc`
    const response = await fetch(url)
    if (!response.ok) {
      return []
    }

    const json = await response.json()
    return json.data
  } catch (error) {
    return []
  }
}

export const getPlaygroundSessionAPI = async (sessionId, type='agent') => {
  try {
    let url = `${PLAYGROUND_URL}/sessions/${sessionId}?type=${type}`
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }

    const json = await response.json()
    return json.chat_history
  } catch (error) {
    throw error
  }
}

export const deletePlaygroundSessionAPI = async (agentId, sessionId) => {
  const response = await fetch(`${PLAYGROUND_URL}/v1/playground/agents/${agentId}/sessions/${sessionId}`, {
    method: 'DELETE'
  })
  return response
}
