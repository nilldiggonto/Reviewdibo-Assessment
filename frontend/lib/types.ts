export interface ProductListItem {
  id: number;
  title: string;
  description: string;
  image_url: string | null;
  average_rating: number | null;
  review_count: number;
}

export interface Review {
  id: number;
  product_id: number;
  user_id: number;
  user: string;
  rating: number;
  comment: string;
  created_at: string;
}

export interface ProductDetail {
  id: number;
  title: string;
  description: string;
  image_url: string | null;
  average_rating: number | null;
  review_count: number;
  reviews: Review[];
}

export interface User {
  id: number;
  name: string;
  email: string;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}