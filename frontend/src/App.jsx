import { useState, useEffect } from "react";

import {
  MapContainer,
  TileLayer,
  Circle,
  Marker,
  Popup,
  Polyline,
  useMapEvents,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "./App.css";


function MapClickHandler({ setIncidentPosition }) {
  useMapEvents({
    click(e) {
      setIncidentPosition([
        e.latlng.lat,
        e.latlng.lng,
      ]);
    },
  });

  return null;
}


// ==========================================
// DISTANCE CALCULATION
// ==========================================

function calculateDistance(point1, point2) {
  const R = 6371000;

  const lat1 = point1[0] * Math.PI / 180;
  const lat2 = point2[0] * Math.PI / 180;

  const dLat =
    (point2[0] - point1[0]) * Math.PI / 180;

  const dLon =
    (point2[1] - point1[1]) * Math.PI / 180;

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1) *
    Math.cos(lat2) *
    Math.sin(dLon / 2) ** 2;

  return (
    R *
    2 *
    Math.atan2(
      Math.sqrt(a),
      Math.sqrt(1 - a)
    )
  );
}


// ==========================================
// WORKER ZONE
// ==========================================

function getWorkerZone(
  worker,
  incident,
  redRadius,
  orangeRadius
) {
  const distance = calculateDistance(
    worker,
    incident
  );

  if (distance <= redRadius) {
    return "RED";
  }

  if (distance <= orangeRadius) {
    return "ORANGE";
  }

  return "GREEN";
}


function App() {

  // ========================================
  // STATES
  // ========================================

  const [approved, setApproved] = useState(false);

  const [zoneActive, setZoneActive] =
    useState(false);

  const [remainingTime, setRemainingTime] =
    useState(180);

  const [apiMessage, setApiMessage] =
    useState("");

  const [routeMessage, setRouteMessage] =
    useState("");

  const [platformMessage, setPlatformMessage] =
    useState("");

  const [blocked, setBlocked] =
    useState(true);

  const [incident, setIncident] = useState({
    crowd: 3000,
    severity: "HIGH",
    roads: 4,
    duration: 180,
  });

  const [incidentPosition, setIncidentPosition] =
    useState([30.3165, 78.0322]);

  const [workerPosition, setWorkerPosition] =
    useState([30.3160, 78.0320]);


  // ========================================
  // FIXED LOCATIONS
  // ========================================

  const emergencyPosition =
    [30.3150, 78.0300];

  const hospitalPosition =
    [30.3200, 78.0400];


  // ========================================
  // ZONE RECOMMENDATION
  // ========================================

  const redRadius =
    incident.severity === "CRITICAL"
      ? 750
      : incident.severity === "HIGH"
      ? 500
      : incident.severity === "MEDIUM"
      ? 300
      : 150;

  const orangeRadius =
    incident.severity === "CRITICAL"
      ? 1500
      : incident.severity === "HIGH"
      ? 1000
      : incident.severity === "MEDIUM"
      ? 700
      : 400;


  // ========================================
  // WORKER ZONE
  // ========================================

  const workerZone =
    getWorkerZone(
      workerPosition,
      incidentPosition,
      redRadius,
      orangeRadius
    );


  const workerAction =
    workerZone === "RED"
      ? "STOP NEW TASKS"
      : workerZone === "ORANGE"
      ? "WARNING"
      : "NORMAL";


  // ========================================
  // TIMER
  // ========================================

  useEffect(() => {

    if (
      !zoneActive ||
      remainingTime <= 0
    ) {
      if (remainingTime <= 0) {
        setZoneActive(false);
      }

      return;
    }

    const timer =
      setInterval(() => {

        setRemainingTime(
          time => time - 1
        );

      }, 1000);

    return () =>
      clearInterval(timer);

  }, [
    zoneActive,
    remainingTime
  ]);


  // ========================================
  // SEND INCIDENT
  // ========================================

  const sendIncidentToBackend =
    async () => {

      try {

        const response =
          await fetch(
            "http://127.0.0.1:8000/api/incidents",
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json",
              },

              body: JSON.stringify({
                location:
                  "Demo Incident Area",

                latitude:
                  incidentPosition[0],

                longitude:
                  incidentPosition[1],

                crowd_size:
                  incident.crowd,

                severity:
                  incident.severity,

                duration_minutes:
                  incident.duration,

                affected_roads:
                  incident.roads,
              }),
            }
          );


        const result =
          await response.json();


        if (result.success) {

          setApiMessage(
            `✓ Backend connected — RED: ${result.data.recommended_zones.red_radius_meters}m, ORANGE: ${result.data.recommended_zones.orange_radius_meters}m`
          );

        } else {

          setApiMessage(
            "Backend returned an error."
          );

        }

      } catch (error) {

        console.error(error);

        setApiMessage(
          "❌ Backend connection failed."
        );
      }
    };


  // ========================================
  // EMERGENCY ROUTE
  // ========================================

  const calculateEmergencyRoute =
    async () => {

      try {

        const response =
          await fetch(
            "http://127.0.0.1:8000/api/routes/calculate",
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json",
              },

              body: JSON.stringify({
                start: "Ambulance-01",
                destination: "Hospital",
              }),
            }
          );


        const result =
          await response.json();


        if (result.success) {

          setRouteMessage(
            `✓ A* route calculated — blocked roads avoided: ${result.data.blocked_roads_avoided}`
          );

        }

      } catch (error) {

        setRouteMessage(
          "❌ Route API unavailable"
        );

      }
    };


  // ========================================
  // PLATFORM RESTRICTION
  // ========================================

  const sendPlatformRestriction =
    async () => {

      try {

        const response =
          await fetch(
            "http://127.0.0.1:8000/api/platform/restriction",
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json",
              },

              body: JSON.stringify({
                platform:
                  "Mock Food / Ride Platform",

                zone_id: 1,

                status:
                  "RESTRICTED",

                reason:
                  "Government-approved public safety zone",
              }),
            }
          );


        const result =
          await response.json();


        if (result.success) {

          setPlatformMessage(
            "✓ Safety restriction delivered to participating platform"
          );

        }

      } catch (error) {

        setPlatformMessage(
          "❌ Platform integration failed"
        );

      }
    };


  // ========================================
  // WORKER MOVEMENT
  // ========================================

  const moveWorkerToRed = () => {

    setWorkerPosition([
      incidentPosition[0],
      incidentPosition[1],
    ]);

  };


  const moveWorkerToOrange = () => {

    setWorkerPosition([
      incidentPosition[0] + 0.007,
      incidentPosition[1],
    ]);

  };


  const moveWorkerToGreen = () => {

    setWorkerPosition([
      incidentPosition[0] + 0.020,
      incidentPosition[1],
    ]);

  };


  // ========================================
  // BLOCKED ROADS
  // ========================================

  const blockedRoads = [
    [
      [30.3158, 78.0325],
      [30.3170, 78.0325],
    ],

    [
      [30.3170, 78.0325],
      [30.3180, 78.0340],
    ],
  ];


  // ========================================
  // EMERGENCY ROUTE
  // ========================================

  const emergencyRoute = [
    emergencyPosition,

    [30.3155, 78.0320],

    [30.3170, 78.0340],

    [30.3185, 78.0370],

    hospitalPosition,
  ];


  // ========================================
  // UI
  // ========================================

  return (

    <div className="app">

      {/* HEADER */}

      <header>

        <div>

          <h1>CivicShield</h1>

          <p>
            Public Safety & Essential-Service
            Coordination
          </p>

        </div>

        <div className="status">
          ● SYSTEM ONLINE
        </div>

      </header>


      <div className="dashboard">


        {/* ==================================
            LEFT PANEL
        ================================== */}

        <aside className="panel">

          <h2>
            Incident Control
          </h2>


          <label>
            Crowd Size
          </label>

          <input
            type="number"
            value={incident.crowd}

            onChange={(e) =>
              setIncident({
                ...incident,
                crowd:
                  Number(e.target.value),
              })
            }
          />


          <label>
            Severity
          </label>

          <select
            value={incident.severity}

            onChange={(e) =>
              setIncident({
                ...incident,
                severity:
                  e.target.value,
              })
            }
          >

            <option>LOW</option>
            <option>MEDIUM</option>
            <option>HIGH</option>
            <option>CRITICAL</option>

          </select>


          <label>
            Affected Roads
          </label>

          <input
            type="number"
            value={incident.roads}

            onChange={(e) =>
              setIncident({
                ...incident,
                roads:
                  Number(e.target.value),
              })
            }
          />


          <label>
            Duration (minutes)
          </label>

          <input
            type="number"
            value={incident.duration}

            onChange={(e) =>
              setIncident({
                ...incident,
                duration:
                  Number(e.target.value),
              })
            }
          />


          {/* AI */}

          <div className="recommendation">

            <h3>
              AI Recommendation
            </h3>

            <p>
              🔴 RED Zone:
              <b> {redRadius} m</b>
            </p>

            <p>
              🟠 ORANGE Zone:
              <b> {orangeRadius} m</b>
            </p>

            <small>
              Recommendation requires
              officer approval.
            </small>

          </div>


          {!approved ? (

            <button
              className="approve"

              onClick={async () => {

                await sendIncidentToBackend();

                setApproved(true);

                setZoneActive(true);

                setRemainingTime(
                  incident.duration * 60
                );

              }}
            >
              ✓ APPROVE SAFETY ZONE
            </button>

          ) : (

            <div className="active">

              {zoneActive ? (

                <>
                  ✓ SAFETY ZONE ACTIVE

                  <br />

                  ⏱️ Remaining:
                  {" "}
                  {Math.floor(
                    remainingTime / 60
                  )} min{" "}

                  {remainingTime % 60}
                  sec
                </>

              ) : (

                <>
                  ⚠️ SAFETY ZONE EXPIRED
                </>

              )}

            </div>

          )}


          {apiMessage && (

            <div className="api-message">
              {apiMessage}
            </div>

          )}

        </aside>


        {/* ==================================
            MAP
        ================================== */}

        <main className="map">

          <MapContainer
            center={incidentPosition}
            zoom={15}
            style={{
              height: "100%",
              width: "100%"
            }}
          >

            <MapClickHandler
              setIncidentPosition={
                setIncidentPosition
              }
            />


            <TileLayer
              attribution="&copy; OpenStreetMap"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />


            {/* ORANGE */}

            <Circle
              center={incidentPosition}
              radius={orangeRadius}

              pathOptions={{
                color: "orange",
                fillColor: "orange",
                fillOpacity: 0.15,
              }}
            />


            {/* RED */}

            <Circle
              center={incidentPosition}
              radius={redRadius}

              pathOptions={{
                color: "red",
                fillColor: "red",
                fillOpacity: 0.25,
              }}
            />


            {/* INCIDENT */}

            <Marker
              position={incidentPosition}
            >

              <Popup>

                <b>
                  ⚠️ INCIDENT
                </b>

                <br />

                Crowd:
                {" "}
                {incident.crowd}

                <br />

                Severity:
                {" "}
                {incident.severity}

                <br />

                Affected Roads:
                {" "}
                {incident.roads}

              </Popup>

            </Marker>


            {/* WORKER */}

            <Marker
              position={workerPosition}
            >

              <Popup>

                <b>
                  👷 Worker-01
                </b>

                <br />

                Zone:
                {" "}
                {workerZone}

                <br />

                Action:
                {" "}
                {workerAction}

              </Popup>

            </Marker>


            {/* AMBULANCE */}

            <Marker
              position={emergencyPosition}
            >

              <Popup>

                🚑
                <b>
                  Ambulance-01
                </b>

                <br />

                Status:
                AVAILABLE

              </Popup>

            </Marker>


            {/* HOSPITAL */}

            <Marker
              position={hospitalPosition}
            >

              <Popup>

                🏥
                <b>
                  Emergency Hospital
                </b>

              </Popup>

            </Marker>


            {/* ROUTE */}

            <Polyline
              positions={emergencyRoute}

              pathOptions={{
                color: "blue",
                weight: 5,
              }}
            />


            {/* BLOCKED ROADS */}

            {blocked &&
              blockedRoads.map(
                (road, index) => (

                  <Polyline
                    key={index}
                    positions={road}

                    pathOptions={{
                      color: "black",
                      weight: 7,
                      dashArray:
                        "10, 10",
                    }}
                  />

                )
              )
            }

          </MapContainer>


          <div className="map-legend">

            <b>Map Legend</b>

            <p>
              🔴 Red Zone — Restricted
            </p>

            <p>
              🟠 Orange Zone — Warning
            </p>

            <p>
              🔵 Blue Line — Emergency Route
            </p>

            <p>
              ⚫ Dashed Line — Blocked Road
            </p>

          </div>

        </main>


        {/* ==================================
            RIGHT PANEL
        ================================== */}

        <aside className="panel right">

          <h2>
            Live Safety Status
          </h2>


          <div className="card red">

            <b>
              RED ZONE
            </b>

            <span>
              Restricted
            </span>

          </div>


          <div className="card orange">

            <b>
              ORANGE ZONE
            </b>

            <span>
              Warning Area
            </span>

          </div>


          <div className="card green">

            <b>
              EMERGENCY SERVICES
            </b>

            <span>
              AVAILABLE
            </span>

          </div>


          {/* WORKER */}

          <h3>
            Worker Safety
          </h3>

          <p>
            👷 Worker-01
          </p>

          <p>
            Zone:
            {" "}
            <b>{workerZone}</b>
          </p>

          <p>
            Action:
            {" "}
            <b>{workerAction}</b>
          </p>


          <div className="worker-buttons">

            <button
              onClick={moveWorkerToGreen}
            >
              🟢 Move Green
            </button>

            <button
              onClick={moveWorkerToOrange}
            >
              🟠 Move Orange
            </button>

            <button
              onClick={moveWorkerToRed}
            >
              🔴 Move Red
            </button>

          </div>


          {/* EMERGENCY */}

          <h3>
            Emergency Units
          </h3>

          <p>
            🚑 Ambulance-01 —
            <b> Available</b>
          </p>

          <p>
            🚓 Police-01 —
            <b> Available</b>
          </p>

          <p>
            🚒 Fire-01 —
            <b> Available</b>
          </p>


          {/* ROUTING */}

          <button
            className="route-button"
            onClick={
              calculateEmergencyRoute
            }
          >
            🚑 Calculate A* Emergency Route
          </button>


          {routeMessage && (

            <div className="success-message">
              {routeMessage}
            </div>

          )}


          {/* BLOCKED ROAD */}

          <button
            className="block-button"

            onClick={() =>
              setBlocked(!blocked)
            }
          >

            {blocked
              ? "🚧 Remove Blocked Roads"
              : "🚧 Block Roads"}

          </button>


          {/* SERVICES */}

          <h3>
            Service Restrictions
          </h3>

          <div className="service-status">

            <p>
              🚗 Ride —
              <b>
                {zoneActive
                  ? " RESTRICTED"
                  : " NORMAL"}
              </b>
            </p>

            <p>
              🍔 Food —
              <b>
                {zoneActive
                  ? " RESTRICTED"
                  : " NORMAL"}
              </b>
            </p>

            <p>
              🛒 Grocery —
              <b>
                {zoneActive
                  ? " RESTRICTED"
                  : " NORMAL"}
              </b>
            </p>

            <p>
              📦 Logistics —
              <b>
                {zoneActive
                  ? " RESTRICTED"
                  : " NORMAL"}
              </b>
            </p>

          </div>


          <button
            className="platform-button"
            onClick={
              sendPlatformRestriction
            }
          >
            📡 Send Restriction to Platforms
          </button>


          {platformMessage && (

            <div className="success-message">
              {platformMessage}
            </div>

          )}


          {/* EMERGENCY SERVICES */}

          <h3>
            Emergency Access
          </h3>

          <p>
            🚑 Ambulance —
            <b> AVAILABLE</b>
          </p>

          <p>
            🚓 Police —
            <b> AVAILABLE</b>
          </p>

          <p>
            🚒 Fire —
            <b> AVAILABLE</b>
          </p>

        </aside>

      </div>

    </div>
  );
}

export default App;