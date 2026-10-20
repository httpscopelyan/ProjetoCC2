import { SensorReading } from "../models/sensorReading";

export type SensorFieldValue = string | number | boolean | string[] | null;

export interface SensorField {
  label: string;
  value: SensorFieldValue;
}

export function buildSensorFields(sensorReading: SensorReading): SensorField[] {
  return [
    { label: "station_id", value: sensorReading.stationId },
    { label: "measured_at", value: sensorReading.measuredAt },
    { label: "temperature_c", value: sensorReading.temperatureCelsius },
    { label: "humidity_pct", value: sensorReading.humidityPercent },
    { label: "pressure_hpa", value: sensorReading.pressureHectopascal },
    { label: "air_quality_raw", value: sensorReading.airQualityRaw },
    { label: "luminosity_raw", value: sensorReading.luminosityRaw },
    { label: "rain_mm", value: sensorReading.rainMillimeters },
    { label: "received_at", value: sensorReading.receivedAt },
    { label: "is_valid", value: sensorReading.isValid },
    { label: "flags", value: sensorReading.validationFlags },
    { label: "dew_point_c", value: sensorReading.dewPointCelsius },
    { label: "heat_index_c", value: sensorReading.heatIndexCelsius },
    { label: "air_quality_index", value: sensorReading.airQualityIndex },
  ];
}

export function formatDisplayValue(fieldValue: SensorFieldValue): string {
  if (fieldValue === null) {
    return "—";
  }
  if (Array.isArray(fieldValue)) {
    return fieldValue.length > 0 ? fieldValue.join(", ") : "—";
  }
  return String(fieldValue);
}
