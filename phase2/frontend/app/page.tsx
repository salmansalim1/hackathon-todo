"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<"all" | "pending" | "completed">("all");
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDesc, setNewTaskDesc] = useState("");
  const [editingTask, setEditingTask] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDesc, setEditDesc] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const userId = "demo-user";

  useEffect(() => {
    fetchTasks();
  }, [filter]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/${userId}/tasks?status=${filter}`);
      if (!response.ok) throw new Error("Failed to fetch tasks");
      const data = await response.json();
      setTasks(data);
      setError("");
    } catch (err: any) {
      setError(err.message || "Failed to fetch tasks");
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: newTaskTitle,
          description: newTaskDesc || undefined,
        }),
      });

      if (!response.ok) throw new Error("Failed to create task");

      setNewTaskTitle("");
      setNewTaskDesc("");
      fetchTasks();
    } catch (err: any) {
      setError(err.message || "Failed to create task");
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}/complete`, {
        method: "PATCH",
      });
      if (!response.ok) throw new Error("Failed to toggle task");
      fetchTasks();
    } catch (err: any) {
      setError(err.message || "Failed to toggle task");
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete task");
      fetchTasks();
    } catch (err: any) {
      setError(err.message || "Failed to delete task");
    }
  };

  const startEditing = (task: Task) => {
    setEditingTask(task.id);
    setEditTitle(task.title);
    setEditDesc(task.description || "");
  };

  const handleUpdateTask = async (taskId: number) => {
    try {
      const response = await fetch(`${API_URL}/api/${userId}/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: editTitle,
          description: editDesc || undefined,
        }),
      });

      if (!response.ok) throw new Error("Failed to update task");

      setEditingTask(null);
      fetchTasks();
    } catch (err: any) {
      setError(err.message || "Failed to update task");
    }
  };

  const cancelEditing = () => {
    setEditingTask(null);
    setEditTitle("");
    setEditDesc("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📝 My Todo List
          </h1>
          <p className="text-gray-600">
            Phase II - Full-Stack Web Application
          </p>
        </div>

        <div className="bg-white shadow-xl rounded-2xl overflow-hidden">
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 m-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <span className="text-red-500 text-xl">⚠️</span>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="p-6 bg-gradient-to-r from-blue-500 to-indigo-600">
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div>
                <input
                  type="text"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  placeholder="What needs to be done?"
                  className="w-full px-4 py-3 border-0 rounded-lg focus:ring-2 focus:ring-white text-gray-900 placeholder-gray-500"
                  required
                />
              </div>
              <div>
                <textarea
                  value={newTaskDesc}
                  onChange={(e) => setNewTaskDesc(e.target.value)}
                  placeholder="Add description (optional)..."
                  rows={2}
                  className="w-full px-4 py-2 border-0 rounded-lg focus:ring-2 focus:ring-white text-gray-900 placeholder-gray-500"
                />
              </div>
              <button
                type="submit"
                className="w-full bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-all duration-200 transform hover:scale-105 shadow-lg"
              >
                ➕ Add Task
              </button>
            </form>
          </div>

          <div className="flex border-b border-gray-200 bg-gray-50">
            {(["all", "pending", "completed"] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`flex-1 px-6 py-4 text-sm font-semibold capitalize transition-all ${
                  filter === f
                    ? "bg-white border-b-2 border-blue-600 text-blue-600"
                    : "text-gray-500 hover:text-gray-700 hover:bg-gray-100"
                }`}
              >
                {f === "all" && "📋 "}
                {f === "pending" && "⏳ "}
                {f === "completed" && "✅ "}
                {f}
              </button>
            ))}
          </div>

          <div className="divide-y divide-gray-200">
            {loading ? (
              <div className="p-12 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-500">Loading tasks...</p>
              </div>
            ) : tasks.length === 0 ? (
              <div className="p-12 text-center">
                <div className="text-6xl mb-4">📝</div>
                <p className="text-gray-500 text-lg">No tasks yet!</p>
                <p className="text-gray-400 text-sm mt-2">
                  Create your first task above
                </p>
              </div>
            ) : (
              tasks.map((task) => (
                <div
                  key={task.id}
                  className="p-6 hover:bg-gray-50 transition-colors"
                >
                  {editingTask === task.id ? (
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <textarea
                        value={editDesc}
                        onChange={(e) => setEditDesc(e.target.value)}
                        rows={2}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleUpdateTask(task.id)}
                          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition-colors"
                        >
                          💾 Save
                        </button>
                        <button
                          onClick={cancelEditing}
                          className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 font-medium transition-colors"
                        >
                          ❌ Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-start gap-4">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => handleToggleComplete(task.id)}
                        className="mt-1.5 h-5 w-5 text-blue-600 rounded cursor-pointer focus:ring-2 focus:ring-blue-500"
                      />
                      <div className="flex-1 min-w-0">
                        <h3
                          className={`text-lg font-semibold ${
                            task.completed
                              ? "line-through text-gray-400"
                              : "text-gray-900"
                          }`}
                        >
                          {task.title}
                        </h3>
                        {task.description && (
                          <p
                            className={`mt-1 text-sm ${
                              task.completed
                                ? "text-gray-400"
                                : "text-gray-600"
                            }`}
                          >
                            {task.description}
                          </p>
                        )}
                        <p className="mt-2 text-xs text-gray-400">
                          🕐 Created: {new Date(task.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => startEditing(task)}
                          className="px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg font-medium transition-colors"
                        >
                          ✏️ Edit
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors"
                        >
                          🗑️ Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {tasks.length > 0 && (
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
              <div className="flex justify-between text-sm text-gray-600">
                <span>
                  Total: <strong>{tasks.length}</strong> tasks
                </span>
                <span>
                  Completed:{" "}
                  <strong>
                    {tasks.filter((t) => t.completed).length}
                  </strong>
                </span>
                <span>
                  Pending:{" "}
                  <strong>
                    {tasks.filter((t) => !t.completed).length}
                  </strong>
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="mt-8 text-center text-sm text-gray-600">
          <p>
            Hackathon Phase II - Full-Stack Todo App
          </p>
          <p className="mt-1">
            Next.js + FastAPI + Neon PostgreSQL
          </p>
        </div>
      </div>
    </div>
  );
}
