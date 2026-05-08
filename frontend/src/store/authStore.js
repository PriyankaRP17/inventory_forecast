import { create } from 'zustand'

const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user')) || null,
  accessToken: localStorage.getItem('access_token') || null,
  role: localStorage.getItem('role') || null,

  login: (userData, access, refresh) => {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('role', userData.role)
    set({
      user: userData,
      accessToken: access,
      role: userData.role,
    })
  },

  logout: () => {
    localStorage.clear()
    set({ user: null, accessToken: null, role: null })
  },
}))

export default useAuthStore
