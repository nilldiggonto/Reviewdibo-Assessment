import { PaginatedResponse, ProductDetail, ProductListItem, Review, User } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export async function getProducts(
  page: number = 1,
  pageSize: number = 9
): Promise<PaginatedResponse<ProductListItem>> {
  return fetchApi<PaginatedResponse<ProductListItem>>(
    `/api/products?page=${page}&page_size=${pageSize}`
  );
}

export async function getProduct(id: number): Promise<ProductDetail> {
  return fetchApi<ProductDetail>(`/api/products/${id}`);
}

export async function createReview(data: {
  product_id: number;
  user_id: number;
  rating: number;
  comment: string;
}): Promise<Review> {
  return fetchApi<Review>("/api/reviews", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getOrCreateUser(data: {
  name: string;
  email: string;
}): Promise<User> {
  const res = await fetch(`${API_URL}/api/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (res.status === 400) {
    const users = await fetchApi<User[]>("/api/users");
    const existing = users.find((u) => u.email === data.email);
    if (existing) return existing;
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export async function deleteReview(id: number): Promise<void> {
  return fetchApi<void>(`/api/reviews/${id}`, { method: "DELETE" });
}

export async function updateReview(
  id: number,
  data: { rating?: number; comment?: string }
): Promise<Review> {
  return fetchApi<Review>(`/api/reviews/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}