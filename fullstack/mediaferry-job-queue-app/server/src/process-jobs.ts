import { db } from "./db";

export const processJobs = async () => {
  const pending = await db.query(
    "SELECT * FROM jobs WHERE status = 'pending' OR status = 'processing' LIMIT 1",
  );
  if (!pending.rows.length) return;

  const job = pending.rows[0];
  console.log("Processing job", job.id, job.file_name);

  await db.query("UPDATE jobs SET status = 'processing' WHERE id = $1", [
    job.id,
  ]);

  // Simulate processing time
  const delay = Math.floor(Math.random() * 5000) + 5000;
  setTimeout(async () => {
    // Simulate a 20% fail rate
    const status = Math.random() < 0.2 ? "failed" : "completed";
    await db.query("UPDATE jobs SET status = $1 WHERE id = $2", [
      status,
      job.id,
    ]);
  }, delay);
};
