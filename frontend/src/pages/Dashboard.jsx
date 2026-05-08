import useAuthStore from '../store/authStore'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const { user, role, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">
          Inventory Forecast
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">
            {user?.username}
          </span>
          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium capitalize">
            {role}
          </span>
          <button
            onClick={handleLogout}
            className="text-sm text-red-500 hover:text-red-700"
          >
            Logout
          </button>
        </div>
      </nav>

      <div className="p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          Welcome, {user?.username}!
        </h2>
        <p className="text-gray-500">
          You are logged in as{' '}
          <span className="font-medium capitalize">{role}</span>
        </p>

        <div className="grid grid-cols-3 gap-6 mt-8">
          <div className="bg-white rounded-xl shadow p-6">
            <p className="text-sm text-gray-500">Role</p>
            <p className="text-2xl font-bold text-blue-600 capitalize">
              {role}
            </p>
          </div>
          <div className="bg-white rounded-xl shadow p-6">
            <p className="text-sm text-gray-500">Status</p>
            <p className="text-2xl font-bold text-green-600">Active</p>
          </div>
          <div className="bg-white rounded-xl shadow p-6">
            <p className="text-sm text-gray-500">System</p>
            <p className="text-2xl font-bold text-gray-800">Inventory</p>
          </div>
        </div>
      </div>
    </div>
  )
}
