// Pipeline: Status Batch NOT OK per Mesin per Minggu
db.inspeksi.aggregate([
  { $lookup: { from: "target_kualitas", localField: "batch_id", foreignField: "batch_id", as: "target_info" }},
  { $unwind: "$target_info" },
  { $addFields: {
      persen_cacat: { $multiply: [ { $divide: ["$cacat_ditemukan", "$jumlah_diperiksa"] }, 100 ] },
      status: { $cond: { if: { $gt: [{ $multiply: [ { $divide: ["$cacat_ditemukan", "$jumlah_diperiksa"] }, 100 ] }, "$target_info.target_maks_cacat"] }, then: "NOT OK", else: "OK" } }
  }},
  { $match: { status: "NOT OK" } },
  { $group: {
      _id: { mesin: "$mesin", minggu: { $week: "$tanggal" }, tahun: { $year: "$tanggal" } },
      jumlah_NOT_OK: { $sum: 1 }
  }},
  { $sort: { "_id.tahun": 1, "_id.minggu": 1, "_id.mesin": 1 } }
]);