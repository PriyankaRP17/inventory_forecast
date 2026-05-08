import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import ProtectedRoute from '../components/ProtectedRoute'

vi.mock('../store/authStore', () => ({
  default: vi.fn(),
}))

import useAuthStore from '../store/authStore'

describe('ProtectedRoute', () => {
  it('redirects to login when not authenticated', () => {
    useAuthStore.mockReturnValue({ user: null, role: null })
    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <ProtectedRoute>
          <div>Protected Content</div>
        </ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
  })

  it('renders children when authenticated', () => {
    useAuthStore.mockReturnValue({ user: { username: 'test' }, role: 'staff' })
    render(
      <MemoryRouter>
        <ProtectedRoute allowedRoles={['staff']}>
          <div>Protected Content</div>
        </ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })
})
