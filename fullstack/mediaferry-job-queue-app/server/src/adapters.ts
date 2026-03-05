import { JobsRepository, Job, UserJob, TotalJob } from "./ports";
import { db } from "./db";

export class PgJobsRepo implements JobsRepository {
  async getAllJobs(): Promise<UserJob[]> {
    const jobs = await db.query(
      `SELECT jobs.*, users.name FROM jobs JOIN users ON jobs.submitted_by = users.email`,
    );

    return jobs.rows;
  }

  async getTotalJobs(): Promise<TotalJob[]> {
    const totalJobs = await db.query(
      "SELECT users.name, COUNT(jobs.id) AS total_jobs, BOOL_OR(jobs.status = 'failed') AS has_failed_jobs, COUNT(jobs.id) FILTER (WHERE jobs.status = 'failed') AS total_failed_jobs FROM users LEFT JOIN jobs ON jobs.user_id = users.id GROUP BY users.id, users.name",
    );

    return totalJobs.rows as TotalJob[];
  }

  async uploadJob(data: {
    file_name: string | undefined;
    job_type: any;
    submitted_by: any;
  }): Promise<Job> {
    const row = await db.query(
      "INSERT INTO jobs (file_name, job_type, submitted_by, user_id) VALUES ($1, $2, $3::text, (SELECT id FROM users WHERE email = $3::text)) RETURNING *",
      [data.file_name, data.job_type, data.submitted_by],
    );

    return row.rows[0];
  }
}
