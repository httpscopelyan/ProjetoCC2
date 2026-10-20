import { useEffect, useState } from "react";
import { apiConfiguration } from "./config/apiConfiguration";
import { sampleStationReading } from "./config/sampleStationReading";
import { HttpApiClient } from "./services/httpApiClient";
import { ReadingApiService } from "./services/readingApiService";
import { SensorReading } from "./models/sensorReading";
import {
  buildSensorFields,
  formatDisplayValue,
} from "./views/sensorReadingPresentation";

const httpApiClient = new HttpApiClient(apiConfiguration);
const readingApiService = new ReadingApiService(httpApiClient, apiConfiguration);

const refreshIntervalMilliseconds = 15000;

export function App() {
  const [backendHealthStatus, setBackendHealthStatus] = useState<string>("");
  const [sensorReading, setSensorReading] = useState<SensorReading | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string>("");

  useEffect(() => {
    const refreshDashboardData = () => {
      readingApiService
        .checkBackendHealth()
        .then((healthStatus) => setBackendHealthStatus(healthStatus))
        .catch(() => setBackendHealthStatus("indisponível"));

      readingApiService
        .submitReadingAndGetProcessed(sampleStationReading)
        .then((processedReading) => {
          setSensorReading(processedReading);
          setFeedbackMessage("");
        })
        .catch((requestError: Error) => {
          setFeedbackMessage(`Erro: ${requestError.message}`);
        });
    };

    setFeedbackMessage("Carregando leitura do backend...");
    refreshDashboardData();

    const intervalId = window.setInterval(
      refreshDashboardData,
      refreshIntervalMilliseconds
    );

    return () => window.clearInterval(intervalId);
  }, []);

  return (
    <div>
      <div>{`Estado do backend: ${backendHealthStatus}`}</div>
      <div>{feedbackMessage}</div>
      <div>
        {sensorReading !== null &&
          buildSensorFields(sensorReading).map((sensorField) => (
            <div key={sensorField.label}>
              {`${sensorField.label}: ${formatDisplayValue(sensorField.value)}`}
            </div>
          ))}
      </div>
    </div>
  );
}
