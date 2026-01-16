const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Get JWT token from cookie
function getToken(): string | null {
  const cookies = document.cookie.split(";");
  const tokenCookie = cookies.find((c) => c.trim().startsWith("better-auth.session_token="));
  if (!tokenCookie) return null;
  return tokenCookie.split("=")[1];
}

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = getToken();
  
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  async getTasks(userId: string, status: string = "all") {
    return fetchWithAuth(`${API_URL}/api/${userId}/tasks?status=${status}`);
  },

  async createTask(userId: string, data: { title: string; description?: string }) {
    return fetchWithAuth(`${API_URL}/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async getTask(userId: string, taskId: number) {
    return fetchWithAuth(`${API_URL}/api/${userId}/tasks/${taskId}`);
  },

  async updateTask(
    userId: string,
    taskId: number,
    data: { title?: string; description?: string }
  ) {
    return fetchWithAuth(`${API_URL}/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  async deleteTask(userId: string, taskId: number) {
    return fetchWithAuth(`${API_URL}/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  },

  async toggleComplete(userId: string, taskId: number) {
    return fetchWithAuth(`${API_URL}/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  },
};
