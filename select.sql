SELECT callsign, registration, COUNT(*) OVER (PARTITION BY registration) AS flight_count
FROM opensky
WHERE callsign = 'ETD18U';
