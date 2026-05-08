// 1. Menghitung OEE per bulan
db.produksi_harian.aggregate([
  { $group: {
      _id: { mesin: "$mesin", bulan: { $month: "$tanggal" }, tahun: { $year: "$tanggal" } },
      total_target: { $sum: "$target" },
      total_ok: { $sum: "$actual_ok" },
      total_reject: { $sum: "$actual_reject" },
      total_op: { $sum: "$durasi_operasi_menit" },
      total_avail: { $sum: "$durasi_tersedia_menit" }
  }},
  { $project: {
      _id: 0, mesin: "$_id.mesin", bulan: "$_id.bulan", tahun: "$_id.tahun",
      availability: { $divide: ["$total_op", "$total_avail"] },
      performance: { $divide: ["$total_ok", "$total_target"] },
      quality: { $divide: ["$total_ok", { $add: ["$total_ok", "$total_reject"] } ] },
      OEE: { $multiply: [
          { $divide: ["$total_ok", "$total_target"] },
          { $divide: ["$total_op", "$total_avail"] },
          { $divide: ["$total_ok", { $add: ["$total_ok", "$total_reject"] } ] }
      ]}
  }},
  { $sort: { OEE: 1 } }
]); 

// 2. Distribusi Produksi per Shift (Bucket)
db.produksi_harian.aggregate([
  { $facet: {
      "shift1": [
        { $match: { shift: 1 } },
        { $bucket: { groupBy: "$actual_ok", boundaries: [0, 200, 300, 400, 600], default: "600+", output: { count: {$sum: 1} } }}
      ],
      "shift2": [
        { $match: { shift: 2 } },
        { $bucket: { groupBy: "$actual_ok", boundaries: [0, 200, 300, 400, 600], default: "600+", output: { count: {$sum: 1} } }}
      ],
      "shift3": [
        { $match: { shift: 3 } },
        { $bucket: { groupBy: "$actual_ok", boundaries: [0, 200, 300, 400, 600], default: "600+", output: { count: {$sum: 1} } }}
      ]
  }}
]);