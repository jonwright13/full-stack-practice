import { JobsRepository } from "./ports";

export class UserJobsService {
  constructor(private repo: JobsRepository) {}

  async getJobs() {
    const [jobs, totalJobs] = await Promise.all([
      this.repo.getAllJobs(),
      this.repo.getTotalJobs(),
    ]);
    return { jobs, totalJobs };
  }

  async uploadJob(data: {
    file_name: string | undefined;
    job_type: any;
    submitted_by: any;
  }) {
    return this.repo.uploadJob(data);
  }
}
