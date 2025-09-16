import { createStore } from 'vuex'
import playground from './playground'

const store = createStore({
  modules: {
    playground,
  },
})

export default store