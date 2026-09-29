export interface PrototypeApi {
  state<T>(initial: T): T;
  save(state: unknown): void;
  toast(message: string, kind?: "success" | "error" | "info" | "warning"): void;
  download(filename: string, contents: string, mime?: string): void;
  money(value: number): string;
  today: string;
  navigate(slug: string): void;
}
