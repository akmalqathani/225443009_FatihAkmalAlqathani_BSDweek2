// Menghitung rata-rata per jam per sensor
db.data_sensor.aggregate([
  { $addFields: { jam: { $hour: "$timestamp" } }},
  { $group: {
      _id: { sensor: "$sensor_id", jam: "$jam" },
      rata_rata_per_jam: { $avg: "$nilai" }
  }},
  { $project: { _id: 0, sensor_id: "$_id.sensor", jam: "$_id.jam", rata_rata: "$rata_rata_per_jam" }},
  { $sort: { sensor_id: 1, jam: 1 } }
]);