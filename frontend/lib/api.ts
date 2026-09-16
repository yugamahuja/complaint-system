const API_URL = (process.env.NEXT_PUBLIC_API_URL || "").replace(/\/$/, "");

export type Complaint = {
  id: number;
  customer_name: string;
  customer_contact: string;
  subject: string;
  description: string;
  category_id: number;
  priority: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  assigned_employee_id: number | null;
  expected_resolution_date: string;
  status: "NEW" | "ASSIGNED" | "IN_PROGRESS" | "RESOLVED" | "CLOSED";
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
  closed_at: string | null;
  category_name?: string | null;
  assigned_employee_name?: string | null;
  activities?: ComplaintActivity[];
};
export type ComplaintActivity = { id: number; complaint_id: number; action: string; description: string; performed_by: number | null; created_at: string };

export type Category = { id: number; name: string };
export type Employee = { id: number; name: string; email: string; department: string };
export type ComplaintList = { items: Complaint[]; page: number; page_size: number; total: number };
export type DashboardSummary = {
  total: number;
  new: number;
  in_progress: number;
  resolved: number;
  overdue: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail || `Request failed (${response.status})`);
  }
  return response.json();
}

export function getComplaints(params: Record<string, string | number | undefined>) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") query.set(key, String(value));
  });
  return request<ComplaintList>(`/complaints?${query.toString()}`);
}

export const getCategories = () => request<Category[]>("/categories");
export const getEmployees = () => request<Employee[]>("/employees");
export const getDashboardSummary = () => request<DashboardSummary>("/dashboard/summary");
export const createComplaint = (data: Record<string, unknown>) =>
  request<Complaint>("/complaints", { method: "POST", body: JSON.stringify(data) });
export const getComplaint = (id: string | number) => request<Complaint>(`/complaints/${id}`);
export const assignComplaint = (id: string | number, employee_id: number, description?: string) =>
  request<Complaint>(`/complaints/${id}/assign`, { method: "POST", body: JSON.stringify({ employee_id, ...(description ? { description } : {}) }) });
export const transitionComplaint = (id: string | number, status: Complaint["status"], description?: string) =>
  request<Complaint>(`/complaints/${id}/transition`, { method: "POST", body: JSON.stringify({ status, ...(description ? { description } : {}) }) });
export const updateComplaint = (id: string | number, data: Partial<Pick<Complaint, "customer_name" | "customer_contact" | "subject" | "description" | "category_id" | "priority" | "expected_resolution_date">>) =>
  request<Complaint>(`/complaints/${id}`, { method: "PATCH", body: JSON.stringify(data) });
