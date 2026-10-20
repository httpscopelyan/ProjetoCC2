export interface StationReadingPayload {
  station_id: string;
  temperature_c: number;
  humidity_pct: number;
  pressure_hpa: number;
  air_quality_raw: number;
  luminosity_raw: number;
  rain_mm: number;
}

export const sampleStationReading: StationReadingPayload = {
  station_id: "est-01",
  temperature_c: 24.4,
  humidity_pct: 60.8,
  pressure_hpa: 1013.2,
  air_quality_raw: 415,
  luminosity_raw: 2310,
  rain_mm: 0.0,
};
