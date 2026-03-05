export interface JobsRepository {
  getAllJobs(): Promise<UserJob[]>;
  getTotalJobs(): Promise<TotalJob[]>;
  uploadJob(data: {
    file_name: string | undefined;
    job_type: string;
    submitted_by: string;
  }): Promise<Job>;
}

export interface Job {
  id: number;
  file_name: string;
  job_type: string;
  status: string;
  submitted_by: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface UserJob extends Job {
  name: string;
}

export interface TotalJob {
  name: string;
  total_jobs: string;
  has_failed_jobs: boolean;
  total_failed_jobs: string;
}
