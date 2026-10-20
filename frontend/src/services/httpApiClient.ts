import { ApiConfiguration } from "../config/apiConfiguration";

export class HttpApiClient {
  private readonly apiConfiguration: ApiConfiguration;

  constructor(apiConfiguration: ApiConfiguration) {
    this.apiConfiguration = apiConfiguration;
  }

  async getJson<ResponseType>(path: string): Promise<ResponseType> {
    const response = await fetch(this.buildUrl(path), {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    return this.parseResponse<ResponseType>(response);
  }

  async postJson<ResponseType>(
    path: string,
    requestBody: unknown
  ): Promise<ResponseType> {
    const response = await fetch(this.buildUrl(path), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(requestBody),
    });
    return this.parseResponse<ResponseType>(response);
  }

  private buildUrl(path: string): string {
    return `${this.apiConfiguration.baseUrl}${path}`;
  }

  private async parseResponse<ResponseType>(
    response: Response
  ): Promise<ResponseType> {
    const responsePayload = (await response.json()) as ResponseType;
    if (!response.ok) {
      throw new Error(`Backend respondeu com status ${response.status}`);
    }
    return responsePayload;
  }
}
