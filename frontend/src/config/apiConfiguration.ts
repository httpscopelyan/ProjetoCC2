export class ApiConfiguration {
  readonly baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  get healthCheckPath(): string {
    return "/health";
  }

  get readingsPath(): string {
    return "/api/v1/readings";
  }
}

const configuredBaseUrl =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const apiConfiguration = new ApiConfiguration(configuredBaseUrl);
