import { ApiConfiguration } from "../config/apiConfiguration";
import { HttpApiClient } from "./httpApiClient";
import { StationReadingPayload } from "../config/sampleStationReading";
import { HealthCheckResponse } from "../models/healthStatus";
import {
  ProcessedReadingData,
  ReadingApiResponse,
  ReadingErrorData,
  SensorReading,
} from "../models/sensorReading";

export class ReadingApiService {
  private readonly httpApiClient: HttpApiClient;
  private readonly apiConfiguration: ApiConfiguration;

  constructor(httpApiClient: HttpApiClient, apiConfiguration: ApiConfiguration) {
    this.httpApiClient = httpApiClient;
    this.apiConfiguration = apiConfiguration;
  }

  async checkBackendHealth(): Promise<string> {
    const responsePayload =
      await this.httpApiClient.getJson<HealthCheckResponse>(
        this.apiConfiguration.healthCheckPath
      );
    return responsePayload.status;
  }

  async submitReadingAndGetProcessed(
    readingPayload: StationReadingPayload
  ): Promise<SensorReading> {
    const responsePayload =
      await this.httpApiClient.postJson<ReadingApiResponse>(
        this.apiConfiguration.readingsPath,
        readingPayload
      );
    if (this.isErrorData(responsePayload.dados)) {
      throw new Error(responsePayload.dados.error);
    }
    return new SensorReading(responsePayload.dados);
  }

  private isErrorData(
    data: ProcessedReadingData | ReadingErrorData
  ): data is ReadingErrorData {
    return (data as ReadingErrorData).error !== undefined;
  }

  // back não tem essas funções ainda.
  async listStations(): Promise<void> {}

  // back não tem essas funções ainda.
  async getLatestReading(stationId: string): Promise<void> {}

  // back não tem essas funções ainda.
  async getReadingSeries(
    stationId: string,
    fromDate: string,
    toDate: string,
    interval: string
  ): Promise<void> {}

  // back não tem essas funções ainda.
  async getReadingStatistics(stationId: string, period: string): Promise<void> {}

  // back não tem essas funções ainda.
  async listActiveAlerts(): Promise<void> {}

  // back não tem essas funções ainda.
  async getNearestStation(latitude: number, longitude: number): Promise<void> {}

  // back não tem essas funções ainda.
  async getRecentReadings(stationId: string, limit: number): Promise<void> {}

  // back não tem essas funções ainda.
  async downloadReadingsCsv(stationId: string, period: string): Promise<void> {}
}
