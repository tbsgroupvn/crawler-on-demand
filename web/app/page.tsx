'use client'

import { useState, useEffect } from 'react'

interface Task {
  id: string
  url: string
  status: string
  result?: any
  error?: string
  created_at: string
  completed_at?: string
}

interface Stats {
  total_tasks: number
  pending_tasks: number
  running_tasks: number
  completed_tasks: number
  failed_tasks: number
  tasks_last_24h: number
}

export default function Home() {
  const [url, setUrl] = useState('')
  const [depth, setDepth] = useState(1)
  const [maxPages, setMaxPages] = useState(5)
  const [tasks, setTasks] = useState<Task[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(false)
  const [batchUrls, setBatchUrls] = useState('')
  const [activeTab, setActiveTab] = useState('single')

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  // Fetch tasks and stats
  const fetchData = async () => {
    try {
      const [tasksRes, statsRes] = await Promise.all([
        fetch(`${apiUrl}/tasks?limit=10`),
        fetch(`${apiUrl}/stats`)
      ])
      
      if (tasksRes.ok && statsRes.ok) {
        const tasksData = await tasksRes.json()
        const statsData = await statsRes.json()
        setTasks(tasksData.tasks)
        setStats(statsData)
      }
    } catch (error) {
      console.error('Failed to fetch data:', error)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  // Single crawl
  const handleSingleCrawl = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!url) return

    setLoading(true)
    try {
      const response = await fetch(`${apiUrl}/crawl`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, depth, max_pages: maxPages })
      })
      
      if (response.ok) {
        setUrl('')
        fetchData()
      }
    } catch (error) {
      console.error('Crawl failed:', error)
    } finally {
      setLoading(false)
    }
  }

  // Batch crawl
  const handleBatchCrawl = async (e: React.FormEvent) => {
    e.preventDefault()
    const urls = batchUrls.split('\n').filter(u => u.trim())
    if (!urls.length) return

    setLoading(true)
    try {
      const response = await fetch(`${apiUrl}/batch/crawl`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(urls)
      })
      
      if (response.ok) {
        setBatchUrls('')
        fetchData()
      }
    } catch (error) {
      console.error('Batch crawl failed:', error)
    } finally {
      setLoading(false)
    }
  }

  // Export functions
  const exportCSV = (taskId: string) => {
    window.open(`${apiUrl}/export/csv/${taskId}`, '_blank')
  }

  const exportExcel = (taskId: string) => {
    window.open(`${apiUrl}/export/excel/${taskId}`, '_blank')
  }

  // Delete task
  const deleteTask = async (taskId: string) => {
    try {
      await fetch(`${apiUrl}/tasks/${taskId}`, { method: 'DELETE' })
      fetchData()
    } catch (error) {
      console.error('Delete failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                🕷️ Crawler On Demand
              </h1>
              <p className="text-gray-600 mt-1">Công cụ crawl website mạnh mẽ với xuất Excel</p>
            </div>
            {stats && (
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-4 rounded-lg">
                <div className="text-sm opacity-90">Tổng tasks</div>
                <div className="text-2xl font-bold">{stats.total_tasks}</div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-yellow-600 text-sm font-medium">Pending</div>
              <div className="text-2xl font-bold text-gray-900">{stats.pending_tasks}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-blue-600 text-sm font-medium">Running</div>
              <div className="text-2xl font-bold text-gray-900">{stats.running_tasks}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-green-600 text-sm font-medium">Completed</div>
              <div className="text-2xl font-bold text-gray-900">{stats.completed_tasks}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-red-600 text-sm font-medium">Failed</div>
              <div className="text-2xl font-bold text-gray-900">{stats.failed_tasks}</div>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-md">
              <div className="text-purple-600 text-sm font-medium">24h</div>
              <div className="text-2xl font-bold text-gray-900">{stats.tasks_last_24h}</div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Crawl Forms */}
          <div className="space-y-6">
            {/* Tab Selector */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg mb-6">
                <button
                  onClick={() => setActiveTab('single')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'single' 
                      ? 'bg-white text-indigo-600 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  🔗 Single URL
                </button>
                <button
                  onClick={() => setActiveTab('batch')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'batch' 
                      ? 'bg-white text-indigo-600 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  📦 Batch URLs
                </button>
              </div>

              {/* Single Crawl Form */}
              {activeTab === 'single' && (
                <form onSubmit={handleSingleCrawl} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Website URL
                    </label>
                    <input
                      type="url"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      placeholder="https://example.com"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      required
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Depth
                      </label>
                      <select
                        value={depth}
                        onChange={(e) => setDepth(Number(e.target.value))}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        <option value={1}>1 Level</option>
                        <option value={2}>2 Levels</option>
                        <option value={3}>3 Levels</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Max Pages
                      </label>
                      <select
                        value={maxPages}
                        onChange={(e) => setMaxPages(Number(e.target.value))}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        <option value={1}>1 Page</option>
                        <option value={5}>5 Pages</option>
                        <option value={10}>10 Pages</option>
                        <option value={20}>20 Pages</option>
                      </select>
                    </div>
                  </div>
                  
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 px-6 rounded-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-all"
                  >
                    {loading ? '🕷️ Crawling...' : '🚀 Start Crawl'}
                  </button>
                </form>
              )}

              {/* Batch Crawl Form */}
              {activeTab === 'batch' && (
                <form onSubmit={handleBatchCrawl} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      URLs (one per line)
                    </label>
                    <textarea
                      value={batchUrls}
                      onChange={(e) => setBatchUrls(e.target.value)}
                      placeholder="https://example1.com&#10;https://example2.com&#10;https://example3.com"
                      rows={6}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
                    />
                  </div>
                  
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-green-600 to-blue-600 text-white py-3 px-6 rounded-lg hover:from-green-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-all"
                  >
                    {loading ? '📦 Processing...' : '🚀 Batch Crawl'}
                  </button>
                </form>
              )}
            </div>
          </div>

          {/* Right Panel - Tasks List */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                📋 Recent Tasks
                <span className="ml-2 bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                  {tasks.length}
                </span>
              </h3>
            </div>
            
            <div className="divide-y divide-gray-200">
              {tasks.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                  No tasks yet. Start crawling! 🕷️
                </div>
              ) : (
                tasks.map((task) => (
                  <div key={task.id} className="p-6 hover:bg-gray-50 transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            task.status === 'completed' ? 'bg-green-100 text-green-800' :
                            task.status === 'running' ? 'bg-blue-100 text-blue-800' :
                            task.status === 'failed' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}>
                            {task.status === 'completed' ? '✅' :
                             task.status === 'running' ? '🔄' :
                             task.status === 'failed' ? '❌' : '⏳'} {task.status}
                          </span>
                        </div>
                        
                        <p className="text-sm font-medium text-gray-900 truncate mb-1">
                          {task.url}
                        </p>
                        
                        <p className="text-xs text-gray-500">
                          {new Date(task.created_at).toLocaleString('vi-VN')}
                        </p>
                        
                        {task.result && (
                          <p className="text-xs text-green-600 mt-1">
                            📊 {task.result.total_pages || 0} pages crawled
                          </p>
                        )}
                      </div>
                      
                      <div className="flex space-x-1 ml-4">
                        {task.result && (
                          <>
                            <button
                              onClick={() => exportCSV(task.id)}
                              className="inline-flex items-center px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded hover:bg-green-200 transition-colors"
                              title="Export CSV"
                            >
                              📄 CSV
                            </button>
                            <button
                              onClick={() => exportExcel(task.id)}
                              className="inline-flex items-center px-2 py-1 text-xs font-medium text-blue-700 bg-blue-100 rounded hover:bg-blue-200 transition-colors"
                              title="Export Excel"
                            >
                              📊 Excel
                            </button>
                          </>
                        )}
                        <button
                          onClick={() => deleteTask(task.id)}
                          className="inline-flex items-center px-2 py-1 text-xs font-medium text-red-700 bg-red-100 rounded hover:bg-red-200 transition-colors"
                          title="Delete Task"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500 text-sm">
            🕷️ Crawler On Demand - Powered by FastAPI & Next.js
          </div>
        </div>
      </footer>
    </div>
  )
} 