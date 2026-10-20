export interface ProcessedReadingData {
  station_id: string | null;
  measured_at: string | null;
  temperature_c: number | null;
  humidity_pct: number | null;
  pressure_hpa: number | null;
  air_quality_raw: number | null;
  luminosity_raw: number | null;
  rain_mm: number | null;
  received_at: string | null;
  is_valid: boolean | null;
  flags: string[] | null;
  dew_point_c: number | null;
  heat_index_c: number | null;
  air_quality_index: number | null;
}

export interface ReadingErrorData {
  error: string;
}

export interface ReadingApiResponse {
  dados: ProcessedReadingData | ReadingErrorData;
}

export class SensorReading {
  stationId: string | null;
  measuredAt: string | null;
  temperatureCelsius: number | null;
  humidityPercent: number | null;
  pressureHectopascal: number | null;
  airQualityRaw: number | null;
  luminosityRaw: number | null;
  rainMillimeters: number | null;
  receivedAt: string | null;
  isValid: boolean | null;
  validationFlags: string[];
  dewPointCelsius: number | null;
  heatIndexCelsius: number | null;
  airQualityIndex: number | null;

  constructor(readingData: ProcessedReadingData) {
    this.stationId = readingData.station_id;
    this.measuredAt = readingData.measured_at;
    this.temperatureCelsius = readingData.temperature_c;
    this.humidityPercent = readingData.humidity_pct;
    this.pressureHectopascal = readingData.pressure_hpa;
    this.airQualityRaw = readingData.air_quality_raw;
    this.luminosityRaw = readingData.luminosity_raw;
    this.rainMillimeters = readingData.rain_mm;
    this.receivedAt = readingData.received_at;
    this.isValid = readingData.is_valid;
    this.validationFlags = readingData.flags ?? [];
    this.dewPointCelsius = readingData.dew_point_c;
    this.heatIndexCelsius = readingData.heat_index_c;
    this.airQualityIndex = readingData.air_quality_index;
  }
}
