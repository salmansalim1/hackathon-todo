const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

class APIClient {
  private async getToken(): Promise<string | null> {
    try {
      const response = await fetch("/api/auth/get-session");
      const data = await response.json();
      return data?.session?.token || null;
    } catch (error) {
      console.error("Failed to get token:", error);
      return null;
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getToken();
    
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async getTasks(userId: string, status?: "all" | "pending" | "completed"): Promise<Task[]> {
    const params = new URLSearchParams();
    if (status && status !== "all") {
      params.append("status", status);
    }
    const query = params.toString() ? `?${params.toString()}` : "";
    return this.request<Task[]>(`/api/${userId}/tasks${query}`);
  }

  async createTask(userId: string, task: TaskCreate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(task),
    });
  }

  async updateTask(userId: string, taskId: number, updates: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    });
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    await this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }
}

export const api = new APIClient();
