const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface ArticleSummary {
  id: string;
  subject_name: string;
  subject_type: "person" | "company";
}

export interface Article {
  id: string;
  subject_name: string;
  subject_type: "person" | "company";
  title: string;
  source: string;
  author: string;
  published_date: string;
  content: string;
}

// Shape is intentionally loose — candidates define their own response structure
export type AnalysisResult = Record<string, unknown>;

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data?.detail ?? `Request failed with status ${res.status}`);
  }

  return data as T;
}

export async function getArticles(): Promise<ArticleSummary[]> {
  return request<ArticleSummary[]>("/articles");
}

export async function getArticle(id: string): Promise<Article> {
  return request<Article>(`/articles/${id}`);
}

export async function analyseArticle(id: string): Promise<AnalysisResult> {
  return request<AnalysisResult>(`/analyse/${id}`, { method: "POST" });
}
